import socket
import pickle
import threading
from board import Board
from node import Node
from edge import Edge
import re

node_dict = {}

def board_unrepr(s):

    print("began")
    num = int(s[0])
    s = s[1:] 

    print("got num")

    # Extract nodes
    nodes = []
    node_matches = re.findall(r"Node\((\d+), (-?\d+\.?\d*), (-?\d+\.?\d*)\)", s)
    print(len(node_matches))
    for match in node_matches:
        print(match)
        id, x, y = int(match[0]), int(match[1]), int(match[2])
        abe = Node(id, (x, y))
        node_dict[id] = abe
        nodes.append(abe)

    print("got nodes")

    # Extract edges
    edges = []
    edge_matches = re.findall(r"Edge\((\d+), (\d+), (\d+), (True|False)\)", s)
    print(len(edge_matches))
    for match in edge_matches:
        print(match)
        id1, id2, id3 = int(match[0]), int(match[1]), int(match[2])
        boolean = True if match[3] == "True" else False
        print(boolean)
        edges.append(Edge(node_dict[id1], node_dict[id2], id3, boolean))

    print("got edges")

    return (num, Board(2, nodes, edges))

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
            print("connecting")
            self.client.connect(self.addr)
            print("connected")
            data = self.client.recv(100*1024*1024)
            print(data)
            print("received")
            # return pickle.loads(data)
            return board_unrepr(data.decode())
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
