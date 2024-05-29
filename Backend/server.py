import socket
from _thread import start_new_thread
from threading import Thread
from batch import Batch
import sys
import time
import json
import asyncio
class Server:
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_players = (
            None  # Stores the waiting players with the game code as the key
        )
        self.games = {}  # Stores the active games with the game code as the key

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.s.listen(10)
        print("Waiting for a connection, Server Started")
    async def handler(websocket):
        while True: 
            message = await websocket.recv()
            print(message)
    

    def send_ticks(self, batch: Batch):
        time.sleep(1)
        while True:

            batch.tick()

            for i, connection in enumerate(batch.connections):
                # try:
                if batch.send_ready(i):
                    # print("Sending tick")
                    batch_json = batch.tick_repr_json(i)
                    batch_tick = batch_json.encode()
                    connection.sendall(batch_tick)
                    # print(i, 'sent tick')
                # except OSError as e:
                #     print(f"Error on connection {i}: {e}")
                #     del batch.connections[i]
            time.sleep(0.1)

    def threaded_client(self, conn):

        data = conn.recv(1024).decode()
        json_data = json.loads(data)
        is_host = json_data["type"]
        player_count = json_data["players"]
        mode = json_data["mode"]

        if is_host == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(player_count, mode, conn)
            conn.sendall("Players may JOIN".encode())
        elif is_host == "JOIN":
            if self.waiting_players:
                conn.sendall("JOINED".encode())
                self.waiting_players.add_player(conn)
            else:
                conn.sendall("FAIL".encode())
                return

        if self.waiting_players.is_ready():
            print("Game is ready to start")
            self.waiting_players.build()
            self.start_game(self.waiting_players)
        else:
            print("Game is not ready to start")
            

    def start_game(self, batch):

        tick_thread = Thread(target=self.send_ticks, args=(batch,))
        tick_thread.daemon = True
        tick_thread.start()

        for i, conn in enumerate(batch.connections):
            start_new_thread(self.threaded_client_in_game, (i, conn, batch))

    def threaded_client_in_game(self, player, conn, batch: Batch):
        conn.send(batch.start_repr_json(player).encode())
        print("Sent start data to player")
        while True:
            try:
                data = json.loads(conn.recv(1000).decode())
                if not data:
                    print("Disconnected")
                    break
                else:

                    print("Received: ", data)
                    # for connection in batch.connections:
                    #     connection.sendall(data)
                    if message := batch.process(player, data):
                        self.problem(conn, message)
            except socket.error as e:
                print(e)

        print("Lost connection")
        conn.close()

    def problem(self, conn, message="Problem"):
        conn.send(json.dumps({"COB": message}).encode())

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn,))


server = Server(5553)
server.run()