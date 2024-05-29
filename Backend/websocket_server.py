import websocket
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

    async def handler(self, websocket, path):
        print("Path: "+path)

        async for message in websocket:
            data = json.loads(message)
            await self.process_message(webocket, data)
    async def process_message(self, websocket ,data):
        player_type = data["type"]
        player_count = data["players"]
        mode = data["mode"]

        if player_type == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(player_count, mode, conn)
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
            self.start_game(self.waiting_players)
        else:
            print("Game is not ready to start")

    def send_ticks(self, websocket, batch:Batch):
        time.sleep(1)
        while True:
            batch.tick()
            for i, connection in enumerate(batch.connections):
                if batch.send_ready(i):
                    batch_json = batch.tick_repr_json(i)
                    batch_tick = batch_json.encode()
                    await websocket.send(batch_tick)
            time.sleep(0.1)


    def threaded_client(self, conn):
        ...

    def start_game(self, batch:Batch):
        ...

    def threaded_client_in_game(self, player, websocket, batch: Batch):
        await websocket.send(batch.start_repr_json(player))


    def problem(self, player, conn, batch:Batch):
        ...

    def run(self):
        ...
 