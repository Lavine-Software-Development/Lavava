from node import Node 
from edge import Edge

nodes = []
captured = []

def clicked():
    pass

while True:
    for cap in captured:
        cap.grow()

    if capture := clicked():
        captured.append(capture)