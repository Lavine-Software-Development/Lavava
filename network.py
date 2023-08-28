import socket
import pickle
import threading

class Network:

    def __init__(self, action_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.9.109"
        self.port = 5555
        self.addr = (self.server, self.port)
        print(self.addr)
        printed = self.connect()
        self.player, self.board = printed
        self.action_callback = action_callback

        threading.Thread(target=self.listen_for_data).start()

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(10*1024*1024)
            return pickle.loads(data)
        except:
            return "Connection failed"

    def getPlayer(self):
        return self.player
    
    def getBoard(self):
        return self.board

    def send(self, data):
        try:
            message = ','.join(map(str, data))
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def listen_for_data(self):
        while True:
            try:
                response = self.client.recv(32).decode()
                if response:
                    data_tuple = tuple(map(int, response.split(',')))
                    if len(data_tuple) == 3:
                        self.action_callback(*data_tuple)
                    else:
                        print(f"Unexpected data format: {data_tuple}")
            except socket.error as e:
                print(e)
                break
