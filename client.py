import pygame as p
from network import Network
from board import Board
from draw import Draw

p.init()

WHITE = (255, 255, 255)

running = True
counter = 0
hovered_node = None

def action(id, acting_player, button):
    board.id_dict[id].click(players[acting_player], button)

def tick():
    board.update()

n = Network(action, tick)
print("network done")
player = n.player
board = Board(*(n.board))
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

        # elif event.type == p.MOUSEMOTION:
        #     position=event.pos
        #     if id:= board.find_node_surround(position):
        #         hovered_node = id
        #         board.id_dict[id].hover(True)
        #     else:
        #         if hovered_node:
        #             board.id_dict[hovered_node].hover(False)
        #             hovered_node = None
                
        #     position=event.pos
        #     if clicked_node:
        #         if board.stray_from_node(clicked_node, position):
        #             n.send((clicked_node, player, 0))

    d.blit()