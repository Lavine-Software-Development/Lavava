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
        # print(self.players)
        # print("Received message in process: ", data)
        if 'game_id' and 'items' in data:
            # print("yoooooo")
            try:
                self.running_games[data["game_id"]].process(websocket, data)
            except KeyError:
                print("Game key not found. Server needs better handling!")
        elif 'action' in data:
            if data['action'] == 'cancel_match':
                await self.handle_cancel_match(websocket, data['game_id'])
        else:
            player_type = data["type"]
            player_count = data["players"]
            mode = data["mode"]
            abilities = data["abilities"]
            userToken = data["userToken"]

            player_code = data["code"]
            if player_type == "LADDER":
                # player_count + 4 random letters
                if ladder_code := self.waiting_ladder_count(str(player_count)):
                    player_code = ladder_code
                else:
                    player_code = str(player_count) + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=4))
            elif player_type == "HOST":
                player_code = str(random.randint(1000, 9999))
                
            if player_type in ("HOST", "LADDER") and player_code not in self.waiting_players:
                self.waiting_players[player_code] = Batch(int(player_count), player_type, websocket, abilities, userToken)
            elif player_type in ("JOIN", "LADDER") and player_code in self.waiting_players:
                if message := self.waiting_players[player_code].add_player(websocket, abilities, userToken):
                    await self.problem(message)
            else:
                message = json.dumps({"game_id": "INVALID", "player_count": 0})
                await websocket.send(message)
                return
            message = json.dumps({"game_id": player_code, "player_count": self.waiting_players[player_code].player_count})
            await websocket.send(message)
            
            if self.waiting_players[player_code].is_ready():
                print("Game is ready to start")
                self.running_games[player_code] = self.waiting_players.pop(player_code)
                print("created game with code ----------------------", player_code)
                await self.start_game(player_code)
            else:
                print("Game is not ready to start")

    async def handle_cancel_match(self, websocket, game_id):
        if game_id in self.waiting_players:
            batch = self.waiting_players[game_id]
            if len(batch.connections) == 1:
                self.waiting_players.pop(game_id)
            else:
                batch.remove_player(websocket)
        else:
            await websocket.send(json.dumps({"action": "match_cancel_failed", "reason": "Game not found"}))

    async def send_ticks(self, batch_code: str):
        batch = self.running_games[batch_code]
        while not batch.done():
            # await asyncio.sleep(1)
            # print("tick")
            batch.tick()
            for websocket in batch.connections:
                try:
                    batch_json = batch.tick_repr_json(websocket)
                    await websocket.send(batch_json)
                except websockets.exceptions.ConnectionClosed:
                    print(f"Error sending tick to websocket")
                except Exception as e:
                    # Handle other potential exceptions
                    print(f"Error sending tick to websocket: {e}")
            await asyncio.sleep(0.1)
        
        # should be its own delete function, but leaving for now due to async complexity
        self.running_games.pop(batch_code)

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
        tasks = []
        print("start game", len(batch.connections))
        batch.start()
        tasks.append(asyncio.create_task(self.send_ticks(batch_code)))

        for websocket in batch.connections:
             await websocket.send(batch.start_repr_json(websocket))
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