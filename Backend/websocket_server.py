import websockets
import asyncio
from batch import Batch
import sys
import time
import json

class WebSocketServer():
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.waiting_players = None
        self.games = {}  # Stores the active games with the game code as the key
        self.locks = {}

    async def handler1(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            await self.process_message(websocket, data)
    async def handler(self, websocket, path):
        self.locks[websocket] = asyncio.Lock()
        try:
            async for message in websocket:
                async with self.locks[websocket]:
                    data = json.loads(message)
                    await self.process_message(websocket, data)
        finally:
            del self.locks[websocket]

    async def process_message(self, websocket,data):
        player_type = data["type"]
        if player_type == "test":
            await websocket.send("test received!")
            return
        player_count = data["players"]
        mode = data["mode"]
       
        if player_type == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(1, mode, websocket)
            await websocket.send("Players may join")
        elif player_type == "JOIN":
            if self.waiting_players:
                await websocket.send("JOINED")
                self.waiting_players.add_player(websocket)
            else:
                await websocket.send("FAILED")
                return
        if self.waiting_players.is_ready():
            print("Game is ready to start")
            self.waiting_players.build()
            await self.start_game(self.waiting_players)
        else:
            print("Game is not ready to start")

    async def send_ticks(self, batch:Batch):
        while True:
            await asyncio.sleep(1)
            batch.tick()
            print("tick")
            for i, websocket in enumerate(batch.connections):
                print(batch.send_ready(i))
                # if batch.send_ready(i):
                if True:
                    batch_json = batch.tick_repr_json(i)
                    await websocket.send(batch_json)
            await asyncio.sleep(0.1)
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
        
    async def start_game(self, batch):
        tasks = []
        print("start game")
        tasks.append(asyncio.create_task(self.send_test_ticks(batch)))
        for i, websocket in enumerate(batch.connections):
            tasks.append(asyncio.create_task(self.threaded_client_in_game(i, websocket, batch)))
        
        # Wait for all tasks to complete and handle exceptions
        for task in tasks:
            try:
                await task
            except Exception as e:
                print(f"An exception occurred: {e}")

    async def threaded_client_in_game(self, player, websocket, batch: Batch):
        print("hereio")
        await websocket.send(batch.start_repr_json(player))
        print("Sent start data to player")
        while True:
            try:
                data = await websocket.recv()
                if not data:
                    print("Disconnected")
                    break
                else:
                    data = json.loads(data)
                    print("Received: ", data)
                    if message := batch.process(player, data):
                        await self.problem(websocket, message)
            except websockets.ConnectionClosed as e:
                print(e)
                break
        print("Lost connection")
        await websocket.close()

    async def problem(self, player, conn, batch:Batch):
        await websocket.send(json.dumps({"COB": message}))
    def run(self):
        start_server = websockets.serve(self.handler, self.server, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print("Websocket server running")
        asyncio.get_event_loop().run_forever()
server = WebSocketServer(5553)
server.run() 