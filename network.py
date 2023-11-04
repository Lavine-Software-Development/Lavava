import socket
import threading
from constants import *
import ast

class Network:
    def __init__(self, action_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.port = 5555
        self.action_callback = action_callback
        self.running = True

        self.get_user_input_and_connect()

    def get_user_input_and_connect(self):
        while self.running:
            self.get_user_input_for_game()
            if self.connect_and_receive_board():
                threading.Thread(target=self.listen_for_data).start()
                break

    def get_user_input_for_game(self):
        server_keys = '/'.join(SERVERS.keys())
        self.server = input(f"Input Server IP Address ({server_keys} for DEFAULT): ")
        if self.server in SERVERS:
            self.server = SERVERS[self.server]
        self.addr = (self.server, self.port)
        while True:
            user_input = input("Do you want to HOST or JOIN a game? (h/j): ").strip()
            if user_input in ["h", "j"]:
                break
            else:
                print("Invalid input. Please enter 'h' or 'j'.")

        if user_input == "h":
            player_count = input("Enter the number of players for the game: ")
            game_type = input("Enter game type. MONEY - 1, RELOAD - 2: ")
            self.init_data = f"HOST,{player_count},{game_type}"
        else:
            self.init_data = f"JOIN,{0},{0}"

    def connect_and_receive_board(self):
        if self.establish_connection():
            return self.receive_board_data()

    def establish_connection(self):
        try:
            self.client.connect(self.addr)
            self.client.send(self.init_data.encode())
            data = self.client.recv(1024)
            response = data.decode()
            if response == "FAIL":
                print("Failed to join the game: No one is currently hosting.")
                return False
            else:
                print("Connected to game", response)
                return True
        except:
            print("Connection failed.")
            return False

    def receive_board_data(self):
        try:
            data = self.client.recv(1024)
            self.data = data.decode()
            return True
        except:
            print("Failed to receive board data.")
            return False

    def send(self, data):
        try:
            head = data[:2]
            tail = data[2:]
            message = '(' + ','.join(map(str, head)) + ',[' + ','.join(map(str, tail)) + '])'
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def listen_for_data(self):
        buffer = ''
        while self.running:
            try:
                chunk = self.client.recv(32).decode()
                buffer += chunk

                while '(' in buffer and ')' in buffer:
                    start_index = buffer.find('(')
                    end_index = buffer.find(')') + 1 
                    response = buffer[start_index:end_index]

                    data_tuple = ast.literal_eval(response)
                    head = data_tuple[:2]
                    tail = list(data_tuple[2])
                    self.action_callback(*head, tail)

                    buffer = buffer[end_index:]

            except socket.error as e:
                print(e)
                break

    def stop(self):
        self.running = False
        self.client.close()

if __name__ == "__main__":
    # replace with your actual callbacks
    def action_callback(): pass 
    def tick_callback(): pass 

    Network(action_callback, tick_callback)
