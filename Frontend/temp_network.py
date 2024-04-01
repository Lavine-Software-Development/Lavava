from asyncio import DatagramProtocol
import socket
import threading
import json
from json_helpers import convert_keys_to_int, split_json_objects

class SoloNetwork:

    def __init__(self, setup, update, data):
        self.setup_callback = setup
        self.update_callback = update

        self.running = True
        self.data = data

        self.get_user_input_and_board()

    def get_user_input_and_board(self):
        while self.running:
            self.get_user_input_for_game()
            if self.receive_board():
                threading.Thread(target=self.listen).start()
                break

    # def get_user_input_for_game(self):
    #     self.game_type = int(self.data[0])

    # def receive_board(self):
    #     self.board_generator_value = int(random.randint(0, 10000))
    #     return True

    # def send(self, data):
    #     self.action_callback(*data[:2], data[2:])

    # def listen(self):
    #     time.sleep(1)
    #     while self.running:
    #         self.action_callback(0, 0, 0)
    #         time.sleep(0.1)
            

class Network():
    def __init__(self, setup, update, data, server):

        self.setup_callback = setup
        self.update_callback = update

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = str(server)
        self.port = 5555
        self.addr = (self.server, self.port)

        self.setup_user(data)

        while True:
            if self.establish_connection():
                break

    def setup_user(self, data):
        if data[0] == "HOST":
            self.init_data = json.dumps({"type": "HOST", "players": data[1], "mode": data[2]})
        else:
            self.init_data = json.dumps({"type": "JOIN", "players": 0, "mode": 0})

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
        data = self.client.recv(10000).decode()
        data_dict = convert_keys_to_int(json.loads(data))
        self.setup_callback(data_dict)
        threading.Thread(target=self.listen).start()
            
    def simple_send(self, code):
        self.send({'code': code, 'items': {}})

    def send(self, data):
        print(data)
        try:
            self.client.send(json.dumps(data).encode())
        except socket.error as e:
            print(e)

    def listen(self):
        while True:
            try:
                data = self.client.recv(15000).decode()  # Adjust buffer size if necessary
                
                # Split the data string into individual JSON objects
                # print(data)
                json_objects = split_json_objects(data)
                for obj_str in json_objects:  # Exclude the last, likely incomplete, object
                    data_dict = convert_keys_to_int(obj_str)
                    
                    self.update_callback(data_dict)

            except socket.error as e:
                break


    def stop(self):
        self.running = False
        self.client.close()

