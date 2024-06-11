import socket
import threading
import json
from json_helpers import convert_keys_to_int, split_json_objects

class Network:
    def __init__(self, setup, update, data, abilities, server):
        self.setup_callback = setup
        self.update_callback = update

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = str(server)
        self.port = 5553
        self.addr = (self.server, self.port)

        self.setup_user(data, abilities)

        while True:
            if self.establish_connection():
                break

    def setup_user(self, data, abilities):
        if data[0] == "HOST":
            self.init_data = json.dumps(
                {"type": "HOST", "players": data[1], "mode": data[2], "abilities": abilities}
            )
        else:
            self.init_data = json.dumps({"type": "JOIN", "players": 0, "mode": 0, "abilities": abilities})

    def first_send(self):
        self.client.send(self.init_data.encode())

    def establish_connection(self):
        try:
            self.client.connect(self.addr)
            self.first_send()
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
        data = self.client.recv(15000).decode()

        data_dict = convert_keys_to_int(json.loads(data))
        self.setup_callback(data_dict)
        threading.Thread(target=self.listen).start()

    def simple_send(self, code):
        self.send({"code": code, "items": {}})

    def send(self, data):
        print(data)
        try:
            self.client.send(json.dumps(data).encode())
        except socket.error as e:
            print(e)

    def listen(self):
        while True:
            try:
                data = self.client.recv(
                    15000
                ).decode()  # Adjust buffer size if necessary

                # Split the data string into individual JSON objects
                # print(data)
                json_objects = split_json_objects(data)
                for (
                    obj_str
                ) in json_objects:  # Exclude the last, likely incomplete, object
                    data_dict = convert_keys_to_int(obj_str)

                    self.update_callback(data_dict)

            except socket.error as e:
                break

    def stop(self):
        self.running = False
        self.client.close()


class PrintNetwork(Network):

    def first_send(self):
        with open("client.txt", "a") as file:
            file.write(self.init_data)
            file.write("\n")
        super().first_send()

    def send(self, data):
        print(data)
        with open("client.txt", "a") as file:
            file.write(json.dumps(data))
            file.write("\n")
        try:
            self.client.send(json.dumps(data).encode())
        except socket.error as e:
            print(e)