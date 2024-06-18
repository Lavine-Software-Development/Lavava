import websockets
import asyncio
from batch import Batch
import sys
import time
import json
import signal
class WebSocketServer():
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.waiting_players = None
        self.games = {}  # Stores the active games with the game code as the key
        self.locks = {}
        self.players = {}

    async def handler(self, websocket, path):
        # self.locks[websocket] = asyncio.Lock()
        print("handler called for socket", websocket)
        if len(self.players) >= 2: 
            self.players = {}
        curr_players = len(self.players)
        self.players[websocket] = curr_players
        # try:
        async for message in websocket:
            print(f"message {message} from {websocket}")
            # async with self.locks[websocket]:
            data = json.loads(message)
            await self.process_message(websocket, data)
        # except Exception as e:
        #     print(f"Error processing message from {websocket}: {e}")

    async def process_message(self, websocket,data):
        print(self.players)
        print("Received message in process: ", data)
        if 'code' and 'items' in data:
            print("yoooooo")
            self.waiting_players.process(self.players[websocket], data)
        else:
            player_type = data["type"]
            player_count = data["players"]
            mode = data["mode"]
            abilities = data["abilities"]
        
            if player_type == "HOST":
                player_count = int(player_count)
                self.waiting_players = Batch(player_count, mode, websocket, abilities)
                message = json.dumps({"msg": "Players may join"})
            elif player_type == "JOIN":
                if self.waiting_players:
                    message = json.dumps({"msg": "JOINED"})
                    await websocket.send(message)
                    if message := self.waiting_players.add_player(websocket, abilities):
                        await self.problem(websocket, message)
                else:
                    await websocket.send("FAILED")
                    return
            if self.waiting_players.is_ready():
                print("Game is ready to start")
                await self.start_game(self.waiting_players)
            else:
                print("Game is not ready to start")

    async def send_ticks(self, batch:Batch):
        while True:
            await asyncio.sleep(1)
            # print("tick")
            batch.tick()
            for i, websocket in enumerate(batch.connections):
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
        print("start game", len(batch.connections))
        tasks.append(asyncio.create_task(self.send_ticks(batch)))

        for i, websocket in enumerate(batch.connections):
             await websocket.send(batch.start_repr_json(i))
        print("Sent start data to player")
            # tasks.append(asyncio.create_task(self.threaded_client_in_game(i, websocket, batch)))
        
        # Wait for all tasks to complete and handle exceptions
        # for task in tasks:
        #     try:
        #         await task
        #     except Exception as e:
        #         print(f"An exception occurred: {e}")

    async def threaded_client_in_game(self, player, websocket, batch: Batch):
        await websocket.send(batch.start_repr_json(player))
        print("Sent start data to player")
        # while True:
        #     print("hi")
        #     try:
        #         data = await websocket.recv()
        #         if not data:
        #             print("Disconnected")
        #             break
        #         else:
        #             data = json.loads(data)
        #             print("Received here: ", data)
        #             print("player", player)
        #             batch.process(player, data)  
        #     except websockets.ConnectionClosed as e:
        #         print(e)
        #         break
        # print("Lost connection")
        # await websocket.close()

    async def problem(self, player, conn, batch:Batch):
        await websocket.send(json.dumps({"COB": message}))
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