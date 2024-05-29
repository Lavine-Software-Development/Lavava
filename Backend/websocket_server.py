import websockets
import asyncio
from _thread import start_new_thread
from threading import Thread
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

    async def handler(self, websocket):
        async for message in websocket:
            print("message")
            print(message)
            data = json.loads(message)
            await self.process_message(websocket, data)
    async def process_message(self, websocket ,data):
        player_type = data["type"]
        player_count = data["players"]
        mode = data["mode"]
        if player_type == "test":
            return
        if player_type == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(player_count, mode, websocket)
            await websocket.send("Players may join")
        elif player_type == "JOIN":
            if self.waiting_players:
                await websocket.send("JOINED")
                self.waiting_players.add(websocket)
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
            for i, websocket in enumerate(batch.connections):
                if batch.send_ready(i):
                    batch_json = batch.tick_repr_json(i)
                    await websocket.send(batch_json)
            await asyncio.sleep(0.1)

    async def start_game(self, batch):
        print("start game")
        asyncio.create_task(self.send_ticks(batch))
        for i, websocket in enumerate(batch.connections):
            asyncio.create_task(self.threaded_client_in_game(i, websocket, batch))

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