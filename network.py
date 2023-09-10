import socket
import threading
from helpers import unwrap_board
from constants import *

class Network:
    def __init__(self, action_callback, tick_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = NETWORK
        self.port = 5555
        self.addr = (self.server, self.port)
        
        # Get user input for hosting or joining a game
        while True:
            while True:
                user_input = input("Do you want to HOST or JOIN a game? (HOST/JOIN): ").strip().upper()
                if user_input in ["HOST", "JOIN"]:
                    break
                else:
                    print("Invalid input. Please enter 'HOST' or 'JOIN'.")
            
            if user_input == "HOST":
                player_count = input("Enter the number of players for the game: ")
                self.init_data = f"HOST,{player_count}"
            else:
                game_code = input("Enter the game code to join: ")
                self.init_data = f"JOIN,{game_code}"
            
            if vals := self.connect():
                self.player, self.board = vals
                self.action_callback = action_callback
                self.tick_callback = tick_callback 

                threading.Thread(target=self.listen_for_data).start()
                break

    def connect(self):
        try:
            self.client.connect(self.addr)
            
            # Send initial data for hosting/joining the game
            self.client.send(self.init_data.encode())

            data = self.client.recv(1024)  # First receive success or failure message
            response = data.decode()
            
            # Check if the response is a failure message
            if response == "INVALID_CODE":
                print("Failed to join the game: Invalid game code.")
                return False
            else:
                print("Connected to game", response)
                
                # Wait for the board data
                data = self.client.recv(100*1024*1024)
                return unwrap_board(data.decode())  # Now we expect the board data

        except:
            print("Connection failed.")
            return False


    def send(self, data):
        try:
            message = ','.join(map(str, data)) + ','
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def listen_for_data(self):
        while True:
            try:
                response = self.client.recv(32).decode()
                if response:
                    data_list = list(filter(None, response.split(',')))
                    data_tuple = tuple(map(int, data_list))
                    while len(data_tuple) >= 3:
                        sub = (data_tuple[0], data_tuple[1], data_tuple[2])
                        new_data = tuple(data_tuple[x] for x in range(3, len(data_tuple)))
                        data_tuple = new_data
                        if sub == (0, 0, 0):
                            self.tick_callback()
                        else:
                            print(sub)
                            self.action_callback(*sub)
            except socket.error as e:
                print(e)
                break
