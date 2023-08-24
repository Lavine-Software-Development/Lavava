import socket
import pickle

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.9.109"
        self.port = 5555
        self.addr = (self.server, self.port)
        printed = self.connect()
        print(printed)
        self.player, self.board = printed

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(10*1024*1024))
        except:
            return "Connection failed"

    def getPlayer(self):
        return self.player
    
    def getBoard(self):
        return self.board

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)