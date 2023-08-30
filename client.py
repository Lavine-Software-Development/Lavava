import pygame as p
from board import Board
from draw import Draw
from map_builder import MapBuilder
from helpers import unwrap_board
from player import Player

p.init()

WHITE = (255, 255, 255)

running = True
counter = 0
hovered_node = None

player_swap = {1: 0, 0: 1}

def action(id, acting_player, button):
    board.id_dict[id].click(players[acting_player], button)     

graph = MapBuilder()
str_graph = graph.repr(0)
player, board_un = unwrap_board(str_graph)
board = Board(*board_un)

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
                action(id, player, button)
            elif id := board.find_edge(position):
                action(id, player, button)

        # if a is pressed
        if event.type == p.KEYDOWN:
            if event.key == p.K_a:
                player = player_swap[player]
                d.player = players[player]

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
    clock.tick()

    counter += 1
    if counter % 10 == 0:

        board.update()