import socket
from _thread import start_new_thread
from batch import Batch
import sys
import time
from threading import Thread


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

    def send_ticks(self, game):
        time.sleep(1)
        tick_message = "(0,0,[])"
        while True:
            for i, connection in enumerate(game.connections):
                try:
                    connection.sendall(tick_message.encode())
                except OSError as e:
                    print(f"Error on connection {i}: {e}")
                    del game.connections[i]
            time.sleep(0.1)

    def threaded_client(self, conn):
        data = conn.recv(1024).decode()
        is_host, player_count, mode = data.split(",")

        if is_host == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(player_count, mode, conn)
            conn.sendall("Players may JOIN".encode())
        elif is_host == "JOIN":
            if self.waiting_players:
                conn.sendall("JOINED".encode())
                self.waiting_players.add_player(conn)

                if self.waiting_players.is_ready():
                    print("Game is ready to start")
                    self.waiting_players.build()
                    self.start_game(self.waiting_players)
                else:
                    print("Game is not ready to start")
            else:
                conn.sendall("FAIL".encode())

    def start_game(self, game):
        tick_thread = Thread(target=self.send_ticks, args=(game,))
        tick_thread.daemon = True
        tick_thread.start()

        for i, conn in enumerate(game.connections):
            start_new_thread(self.threaded_client_in_game, (i, conn, game))

    def threaded_client_in_game(self, player, conn, game):
        conn.send(game.repr(player).encode())
        while True:
            try:
                data = conn.recv(32)
                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Received: ", data.decode())
                    for connection in game.connections:
                        connection.sendall(data)
            except socket.error as e:
                print(e)

        print("Lost connection")
        conn.close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn,))


def start_server():
    server = Server(5555)
    server.run()