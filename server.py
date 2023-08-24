import socket
from _thread import *
import sys
from make_board import new_board
from player import Player
import pickle

server = "192.168.9.109"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    sys.exit()

s.listen(2)
print("Waiting for a connection, Server Started")


def create_game(conns):
    board = new_board()
    player1 = Player((255,0,0))
    player2 = Player((0,0,255))
    board.nodes[0].click(player1)
    board.nodes[5].click(player2)

    start_new_thread(threaded_client, (conns[0], player1, board))
    start_new_thread(threaded_client, (conns[1], player2, board))

def threaded_client(conn, player, board):
    conn.send(pickle.dumps((player, board)))
    reply = None
    while True:
        try:
            data = pickle.loads(conn.recv(10*1024*1024))
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            # conn.sendall(str.encode(reply))
        except:
            break
    
    print("Lost connection")
    conn.close()

conns = []
while True:
    conn, addr = s.accept()
    conns.append(conn)
    print("Connected to:", addr)
    if len(conns) % 2 == 0 and len(conns) > 0:
        create_game(conns)
        conns = []