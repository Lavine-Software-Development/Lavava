import socket
from _thread import start_new_thread
from queue import Queue
from game import Game
import sys
import time
from threading import Thread
from constants import *
import random
import string

class Server:
    def __init__(self, port):
        self.server = '50.64.20.3'
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_players = {}  # Stores the waiting players with the game code as the key
        self.games = {}  # Stores the active games with the game code as the key

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.s.listen(10)
        print("Waiting for a connection, Server Started")

    def generate_game_code(self):
        """Generate a unique game code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_ticks(self, game):
        time.sleep(1)
        tick_message = "0,0,0,"
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
        is_host, player_count_or_code = data.split(",")

        if is_host == "HOST":
            player_count = int(player_count_or_code)
            game_code = self.generate_game_code() # Generate a unique game code for the new game
            self.waiting_players[game_code] = Game(player_count, game_code, conn)
            conn.sendall(game_code.encode())
        elif is_host == "JOIN":
            code = player_count_or_code
            if player_count_or_code in self.waiting_players:
                conn.sendall(player_count_or_code.encode())
                self.waiting_players[code].add_player(conn)
                
                if self.waiting_players[code].is_ready():
                    print("Game is ready to start")
                    self.waiting_players[code].build()
                    self.start_game(self.waiting_players[code])
                else:
                    print("Game is not ready to start")
            else:
                conn.sendall("INVALID_CODE".encode())

    def start_game(self, game):
        tick_thread = Thread(target=self.send_ticks, args=(game,))
        tick_thread.daemon = True
        tick_thread.start()

        for i, conn in enumerate(game.connections):
            start_new_thread(self.threaded_client_in_game, (i, conn, game))

    def restart_game(self, game):
        # Reset the game state
        game.build()  # You might need to implement this method in your Game class

            # Now, iterate over all connections (players) and send the updated board data
        for i, conn in enumerate(game.connections):
            try:
                # You would send the new representation of the board here
                new_board_data = game.graph.repr(i, game.player_count)  # Get the new board representation
                conn.sendall(new_board_data.encode())  # Send the new board data
            except Exception as e:
                print(f"Failed to send new board data to player {i}: {e}") 

    def threaded_client_in_game(self, player, conn, game):
        conn.send(game.graph.repr(player, game.player_count).encode())
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
                    data_list = list(filter(None, data.decode().split(',')))
                    data_tuple = tuple(map(int, data_list))
                    if data_tuple == (-2, -2, -2):
                        self.restart_game(game)
            except socket.error as e:
                print(e)
        
        print("Lost connection")
        conn.close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            
            start_new_thread(self.threaded_client, (conn,))

if __name__ == "__main__":
    server = Server(5555)
    server.run()
