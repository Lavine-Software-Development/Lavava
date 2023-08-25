import socket
from _thread import *
import sys
from make_board import new_board
import pickle

server = "100.71.29.117"
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

    start_new_thread(threaded_client, (conns, 0, board))
    start_new_thread(threaded_client, (conns, 1, board))

def threaded_client(conns, player, board):
    conns[player].send(pickle.dumps((player, board)))
    while True:
        try:
            data = conns[player].recv(32)
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data.decode())
                for conn in conns:
                    conn.sendall(data)
        except socket.error as e:
            print(e)

    print("Lost connection")
    conn.close()

conns = []
while True:
    conn, addr = s.accept()
    conns.append(conn)
    print("Connected to:", addr)
    if len(conns) % 2 == 0 and len(conns) > 0:
        create_game(conns)