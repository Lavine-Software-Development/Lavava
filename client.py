import pygame as p
import math
from network import Network
from draw import Draw

p.init()

WHITE = (255, 255, 255)

running = True
counter = 0
clicked_node = None

def action(id, acting_player, button):
    if button:
        if board.id_dict[id].click(players[acting_player], button):
            global clicked_node
            clicked_node = id
    else:
        board.id_dict[id].pressed = False

n = Network(action)
print("network done")
player = n.getPlayer()
board = n.getBoard()
players = board.player_dict
clock = p.time.Clock()
d = Draw(board.edges, board.nodes, players[player])

while running:

    for event in p.event.get():

        if event.type == p.QUIT:
            running = False

        if event.type == p.MOUSEBUTTONDOWN:
            position=event.pos
            button = event.button
            if id := board.find_node(position):
                n.send((id, player, button))
            elif id := board.find_edge(position):
                n.send((id, player, button))

        elif event.type == p.MOUSEMOTION:
            position=event.pos
            if clicked_node:
                if board.stray_from_node(clicked_node, position):
                    n.send((clicked_node, player, 0))
                    
        elif event.type == p.MOUSEBUTTONUP:
            if clicked_node:
                n.send((clicked_node, player, 0))
                clicked_node = None

    d.blit()
    clock.tick()

    counter += 1
    if counter % 10 == 0:

        board.update()