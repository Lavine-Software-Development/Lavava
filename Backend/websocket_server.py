import random
import websockets
import asyncio
from batch import Batch
import json
import signal

class WebSocketServer():
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.waiting_players: dict[str, Batch] = {}
        self.running_games: dict[str, Batch] = {}  # Stores the active games with the game code as the key

    async def handler(self, websocket, path):
        async for message in websocket:
            print("message", message)
            data = json.loads(message)
            await self.process_message(websocket, data)

    def waiting_ladder_count(self, player_count):
        # return the existence of a ladder code starting with player_count and 5 characters overall
        # within self.waiting_players, or false if it doesn't exist
        for code in self.waiting_players:
            if len(code) == 5 and code.startswith(player_count):
                return code
        return False

    async def process_message(self, websocket, data):

        token = data["token"]
        game_code = data["game_id"]

        if 'items' in data:
            # print("yoooooo")

            try:
                self.running_games[game_code].process(token, data)
            except KeyError:
                print("Game key not found. Server needs better handling!")
        elif 'action' in data:
            if data['action'] == 'cancel_match':
                await self.handle_cancel_match(token, game_code)
            elif data['action'] == 'reconnect':
                batch = self.running_games[game_code]
                catch_me_up_json = batch.reconnect_player(token, websocket)
                await websocket.send(catch_me_up_json)
        else:
            player_type = data["type"]
            player_count = data["players"]
            abilities = data["abilities"]

            game_code = data["game_id"]
            if player_type == "LADDER":
                # player_count + 4 random letters
                if ladder_code := self.waiting_ladder_count(str(player_count)):
                    game_code = ladder_code
                else:
                    game_code = str(player_count) + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=4))
            elif player_type == "HOST":
                game_code = str(random.randint(1000, 9999))
                
            if player_type in ("HOST", "LADDER") and game_code not in self.waiting_players:
                self.waiting_players[game_code] = Batch(int(player_count), player_type, token, websocket, abilities)
            elif player_type in ("JOIN", "LADDER") and game_code in self.waiting_players:
                if message := self.waiting_players[game_code].add_player(token, websocket, abilities):
                    await self.problem(message)
            else:
                message = json.dumps({"game_id": "INVALID", "player_count": 0})
                await websocket.send(message)
                return
            message = json.dumps({"game_id": game_code, "player_count": self.waiting_players[game_code].player_count})
            await websocket.send(message)
            
            if self.waiting_players[game_code].is_ready():
                print("Game is ready to start")
                self.running_games[game_code] = self.waiting_players.pop(game_code)
                print("created game with code ----------------------", game_code)
                await self.start_game(game_code)
            else:
                print("Game is not ready to start")

    async def handle_cancel_match(self, token, game_id):
        if game_id in self.waiting_players:
            batch = self.waiting_players[game_id]
            if len(batch.token_ids) == 1:
                self.waiting_players.pop(game_id)
            else:
                batch.remove_player(token)
        else:
            print("Game not found. Can't be cancelled")

    async def send_ticks(self, batch_code: str):
        batch = self.running_games[batch_code]
        to_remove = []
        while not batch.done():
            batch.tick()
            for id, websocket in batch.id_sockets.items():
                if not batch.return_player_has_left(id):
                    try:
                        batch_json = batch.tick_repr_json(id)
                        await websocket.send(batch_json)
                    except websockets.exceptions.ConnectionClosed:
                        pass
                        # print(f"Error sending tick to websocket")
                        # if batch.40 connections not connected still then 
                else:
                    print("Player has left")
                    await websocket.send(json.dumps({"action": "player_left"}))
                    to_remove.append(id)
            for i in to_remove:
                batch.id_sockets.pop(i)  # Use pop with default to avoid KeyError

            to_remove.clear()  # Clear the list for the next loop iteration

            await asyncio.sleep(0.1)
        
        # should be its own delete function, but leaving for now due to async complexity
        self.running_games.pop(batch_code,None)

    async def send_test_ticks(self, batch):
        json_list = []
        file_path = "/Users/akashilangovan/ian_game/Lavava/Backend/server_json.txt"
        # Open the file and read line by line
        with open(file_path, 'r') as file:
            for line in file:
                json_object = json.loads(line.strip())
                json_list.append(json_object)
        idx = 0
        while True:


            await asyncio.sleep(0.1)
            # batch.tick()
            for i, websocket in enumerate(batch.connections):
                if True:
                    batch_json = json_list[idx] if idx < len(json_list) else json_list[1]
                    idx += 1
                    # print(json.dumps(batch_json))
                    await websocket.send(json.dumps(batch_json))
            await asyncio.sleep(0.1)
        
    async def start_game(self, batch_code):
        batch = self.running_games[batch_code]
        batch.start()
        asyncio.create_task(self.send_ticks(batch_code))

        for id, websocket in batch.id_sockets.items():
             await websocket.send(batch.start_repr_json(id))
        print("Sent start data to player")
            # tasks.append(asyncio.create_task(self.threaded_client_in_game(i, websocket, batch)))
        
        # Wait for all tasks to complete and handle exceptions
        # for task in tasks:
        #     try:
        #         await task
        #     except Exception as e:
        #         print(f"An exception occurred: {e}")

    async def problem(self, message):
        pass

    def run(self):
        loop = asyncio.get_event_loop()

        # Starting the server
        start_server = websockets.serve(self.handler, self.server, self.port)
        server = loop.run_until_complete(start_server)

        # Print server running
        print("Websocket server running on {}:{}".format(self.server, self.port))

        # Setup graceful shutdown
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame),
                                    lambda: asyncio.ensure_future(self.shutdown(server, signame)))

        try:
            loop.run_forever()
        finally:
            loop.close()

    async def shutdown(self, server, signame):
        print(f"Received signal {signame}... shutting down")
        server.close()
        await server.wait_closed()
        asyncio.get_event_loop().stop()
    

server = WebSocketServer(5553)
server.run() 