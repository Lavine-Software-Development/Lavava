import socket
import threading
import time
from constants import MODES
from server_constants import SERVERS
import ast
import random
import requests

class SoloNetwork:
    def __init__(self, action_callback, data):
        self.action_callback = action_callback
        self.running = True
        self.data = data

        self.get_user_input_and_board()

    def get_user_input_and_board(self):
        while self.running:
            self.get_user_input_for_game()
            if self.receive_board():
                threading.Thread(target=self.listen).start()
                break

    def get_user_input_for_game(self):
        self.game_type = int(self.data[0])

    def receive_board(self):
        self.board_generator_value = int(random.randint(0, 10000))
        return True

    def send(self, data):
        self.action_callback(*data[:2], data[2:])

    def listen(self):
        time.sleep(1)
        while self.running:
            self.action_callback(0, 0, 0)
            time.sleep(0.1)

    def stop(self):
        self.running = False
            

class Network(SoloNetwork):
    def __init__(self, action_callback, data, server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        if server is None:
            response = requests.get('https://httpbin.org/ip')
            self.server = response.json()['origin']
        self.port = 5555

        super().__init__(action_callback, data)

    def get_user_input_for_game(self):
        self.addr = (self.server, self.port)

        if self.data[0] == "HOST":
            self.init_data = f"HOST,{self.data[1]},{self.data[2]}"
        else:
            self.init_data = f"JOIN,{0},{0}"

    def receive_board(self):
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
            message = (
                "(" + ",".join(map(str, head)) + ",[" + ",".join(map(str, tail)) + "])"
            )
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def listen(self):
        buffer = ""
        while self.running:
            try:
                chunk = self.client.recv(32).decode()
                buffer += chunk

                while "(" in buffer and ")" in buffer:
                    start_index = buffer.find("(")
                    end_index = buffer.find(")") + 1
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
        super().stop()
        self.client.close()

