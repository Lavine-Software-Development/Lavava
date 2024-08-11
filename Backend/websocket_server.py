import random
import websockets
import asyncio
from batch import Batch
import json
import signal
import ssl 
import logging
from config import config
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebSocketServer():
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.waiting_players: dict[str, Batch] = {}
        self.running_games: dict[str, Batch] = {}  # Stores the active games with the game code as the key
        logger.info(f"WebSocketServer initialized on port {port}")

    async def handler(self, websocket, path):
        logger.info(f"New connection established from {websocket.remote_address}")
        try:
            async for message in websocket:
                logger.debug(f"Received message: {message}")
                data = json.loads(message)
                await self.process_message(websocket, data)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for {websocket.remote_address}")
        # except json.JSONDecodeError:
        #     logger.error(f"Invalid JSON received: {message}")
        # except Exception as e:
        #     logger.exception(f"Error in handler: {str(e)}")

    def waiting_ladder_count(self, player_count, mode):
        settings_add_on = mode[0] + str(player_count)
        logger.debug(f"Checking for waiting ladder with player count: {player_count}")
        for code in self.waiting_players:
            if len(code) == 6 and code.startswith(settings_add_on):
                logger.info(f"Found waiting ladder: {code}")
                return code
        logger.info(f"No waiting ladder found for player count: {player_count}")
        return settings_add_on + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=4))

    async def process_message(self, websocket, data):
        logger.debug(f"Processing message: {data}")

        token = data.get("token")
        game_code = data.get("game_id")

        if 'items' in data:
            logger.info(f"Processing items for game {game_code}")
            try:
                self.running_games[game_code].process(token, data)
            except KeyError:
                logger.error(f"Game {game_code} not found in running games")
        elif 'action' in data:
            action = data['action']
            logger.info(f"Processing action: {action}")
            if action == 'cancel_match':
                await self.handle_cancel_match(token, game_code)
            elif action == 'bot_request':
                await self.handle_bot_request(game_code)
            elif action == 'reconnect':
                await self.handle_reconnect(websocket, token, game_code)
        else:
            await self.handle_game_setup(websocket, data)

    async def handle_bot_request(self, game_id):
        logger.info(f"Handling bot request for game {game_id}")
        if game_id in self.waiting_players:
            batch = self.waiting_players[game_id]
            batch.add_bots()
            await self.check_game_ready(game_id)
        else:
            logger.warning(f"Game {game_id} not found. Can't create bot")

    async def handle_cancel_match(self, token, game_id):
        logger.info(f"Handling cancel match for game {game_id}")
        if game_id in self.waiting_players:
            batch = self.waiting_players[game_id]
            if len(batch.token_ids) == 1:
                self.waiting_players.pop(game_id)
                print("cancelled game")
                logger.info(f"Removed game {game_id} from waiting players")
            else:
                batch.remove_player_from_lobby(token)
                logger.info(f"Removed player {token} from game {game_id}")
        else:
            logger.warning(f"Game {game_id} not found. Can't be cancelled")

    async def handle_reconnect(self, websocket, token, game_code):
        logger.info(f"Handling reconnect for player {token} in game {game_code}")
        if game_code in self.running_games:
            batch = self.running_games[game_code]
            catch_me_up_json = batch.reconnect_player(token, websocket)
            await websocket.send(catch_me_up_json)
            logger.info(f"Player {token} reconnected to game {game_code}")
        else:
            logger.warning(f"Reconnection rejected for game {game_code}. Game has ended")
            await websocket.send(json.dumps({"action": "leave_game"}))

    async def handle_game_setup(self, websocket, data):
        player_type = data.get("type")
        player_count = data.get("players") # will be null for player_type JOIN
        abilities = data.get("abilities")
        token = data.get("token")
        mode = data.get("mode")

        logger.info(f"Setting up game: Type={player_type}, Players={player_count}")

        if player_type == "LADDER":
            game_code = self.waiting_ladder_count(str(player_count), mode)
        elif player_type == "HOST":
            game_code = str(random.randint(1000, 9999))
        else:
            game_code = data.get("game_id")

        if player_type in ("HOST", "LADDER") and game_code not in self.waiting_players:
            self.waiting_players[game_code] = Batch(int(player_count), player_type == "LADDER", mode, token, websocket, abilities)
            logger.info(f"Created new game: {game_code}")
        elif player_type in ("JOIN", "LADDER") and game_code in self.waiting_players:
            if message := self.waiting_players[game_code].add_player(token, websocket, abilities):
                await self.problem(message)
                logger.warning(f"Problem adding player to game {game_code}: {message}")
            else:
                logger.info(f"Added player {token} to game {game_code}")
        else:
            message = json.dumps({"game_id": "INVALID", "player_count": 0})
            await websocket.send(message)
            logger.warning(f"Invalid game setup attempt: Type={player_type}, Code={game_code}")
            return

        message = json.dumps({"game_id": game_code, "player_count": self.waiting_players[game_code].player_count, "mode": mode})
        await websocket.send(message)

        await self.check_game_ready(game_code)

    async def check_game_ready(self, game_code):
        if self.waiting_players[game_code].is_ready():
            self.running_games[game_code] = self.waiting_players.pop(game_code)
            logger.info(f"Game {game_code} is ready to start")
            await self.start_game(game_code)
        else:
            logger.info(f"Game {game_code} is not ready to start")

    async def send_ticks(self, batch_code: str):
        logger.info(f"Starting tick sending for game {batch_code}")
        batch = self.running_games[batch_code]
        while not batch.done():
            batch.tick()
            for id in list(batch.id_sockets.keys()):
                if id in batch.id_sockets:
                    websocket = batch.id_sockets[id]
                    if batch.still_send(id):
                        try:
                            batch_json = batch.tick_repr_json(id)
                            await websocket.send(batch_json)
                        except websockets.exceptions.ConnectionClosed:
                            # logger.warning(f"Connection closed for player {id} in game {batch_code}")
                            batch.did_not_respond(id)
                    else:
                        logger.info(f"Removing player {id} from game {batch_code}")
                        batch.remove_player_from_game(id)
                else:
                    logger.warning(f"Player {id} has left game {batch_code}, but key remains")
            batch.post_tick()
            await asyncio.sleep(0.1)
        
        logger.info(f"Game {batch_code} has ended. Removing from running games.")
        self.running_games.pop(batch_code, None)

    async def start_game(self, batch_code):
        logger.info(f"Starting game {batch_code}")
        batch = self.running_games[batch_code]
        batch.start()
        asyncio.create_task(self.send_ticks(batch_code))

        for id, websocket in batch.id_sockets.items():
             await websocket.send(batch.start_repr_json(id))
        logger.info(f"Sent start data to all players in game {batch_code}")

    async def problem(self, message):
        logger.error(f"Problem occurred: {message}")

    def run(self):
        loop = asyncio.get_event_loop()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        certfile = "fullchain.pem"
        keyfile = "privkey.pem"
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        
        start_server = websockets.serve(self.handler, self.server, self.port, ssl=ssl_context)
        server = loop.run_until_complete(start_server)

        logger.info(f"Websocket server running on {self.server}:{self.port}")

        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame),
                                    lambda: asyncio.ensure_future(self.shutdown(server, signame)))
        try:
            loop.run_forever()
        except Exception as e:
            logger.exception(f"Error in server main loop: {str(e)}")
        finally:
            loop.close()
            logger.info("Server shutdown complete")

    async def shutdown(self, server, signame):
        logger.info(f"Received signal {signame}... shutting down")
        server.close()
        await server.wait_closed()
        asyncio.get_event_loop().stop()

if __name__ == "__main__":
    port_number = 5554 if config.ENV == 'STAGING' else 5553
    server = WebSocketServer(port_number)
    server.run()