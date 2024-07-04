import random
import websockets
import asyncio
import ssl
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

    async def process_message(self, websocket, data):
        if 'game_id' and 'items' in data:
            # print("yoooooo")
            self.running_games[data["game_id"]].process(websocket, data)
        else:
            player_type = data["type"]
            player_count = data["players"]
            mode = data["mode"]
            abilities = data["abilities"]

            player_code = data["code"]
            if player_type == "LADDER":
                player_code = str(player_count)
            elif player_type == "HOST":
                player_code = str(random.randint(1000, 9999))
                
            if player_type in ("HOST", "LADDER") and player_code not in self.waiting_players:
                self.waiting_players[player_code] = Batch(int(player_count), player_type, websocket, abilities)
            elif player_type in ("JOIN", "LADDER") and player_code in self.waiting_players:
                if message := self.waiting_players[player_code].add_player(websocket, abilities):
                    await self.problem(message)
            else:
                await websocket.send("FAILED")
                return
            message = json.dumps({"game_id": player_code})
            await websocket.send(message)
            
            if self.waiting_players[player_code].is_ready():

                print("Game is ready to start")
                self.running_games[player_code] = self.waiting_players.pop(player_code)
                print("created game with code ----------------------", player_code)
                await self.start_game(player_code)
            else:
                print("Game is not ready to start")


    async def send_ticks(self, batch_code: str):
        batch = self.running_games[batch_code]
        while not batch.done():

            batch.tick()
            for websocket in batch.connections:
                batch_json = batch.tick_repr_json(websocket)
                await websocket.send(batch_json)
            await asyncio.sleep(0.1)
 
        # should be its own delete function, but leaving for now due to async complexity
        self.running_games.pop(batch_code)

    async def send_test_ticks(self, batch):
        json_list = []
        file_path = "/Users/akashilangovan/ian_game/Lavava/Backend/server_json.txt"
        with open(file_path, 'r') as file:
            for line in file:
                json_object = json.loads(line.strip())
                json_list.append(json_object)
        idx = 0
        while True:
            await asyncio.sleep(0.1)
            for i, websocket in enumerate(batch.connections):
                if True:
                    batch_json = json_list[idx] if idx < len(json_list) else json_list[1]
                    idx += 1
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

    async def problem(self, message):
        pass

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Create an SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile="/Users/akashilangovan/ian_game/server.crt", keyfile="/Users/akashilangovan/ian_game/private.key")
        print(ssl_context)
        # Starting the server with SSL
        start_server = websockets.serve(self.handler, self.server, self.port, ssl=ssl_context)
        server = loop.run_until_complete(start_server)

        # Print server running
        print("WebSocket server running on {}:{} with SSL".format(self.server, self.port))

        try:
            loop.run_forever()
        finally:
            loop.close()

# Instantiate and run the server
server = WebSocketServer(5553)
server.run()
