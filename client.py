import pygame as p
import math
from network import Network
from draw import Draw

p.init()

WHITE = (255, 255, 255)

n = Network()
player = n.getPlayer()
board = n.getBoard()
clock = p.time.Clock()
d = Draw(board.edges, board.nodes, player)

running = True
counter = 0
clicked_node = None

while running:

    for event in p.event.get():

        if event.type == p.QUIT:
            running = False

        if event.type == p.MOUSEBUTTONDOWN:
            position=event.pos
            button = event.button
            if id := board.find_node(position):
                n.send(id, player, button)
            elif id := board.find_edge(position):
                n.send(id, player, button)

        elif event.type == p.MOUSEMOTION:
            position=event.pos
            if clicked_node:
                if board.stray_from_node(clicked_node, position):
                    n.send(clicked_node, player, None)
                    
        elif event.type == p.MOUSEBUTTONUP:
            if clicked_node:
                n.send(clicked_node, player, None)

    d.blit()
    clock.tick()

    counter += 1
    if counter % 10 == 0:

        board.update()