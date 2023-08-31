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
edge_build=False
active=False
closest=None
while running:
    for event in p.event.get():
        d.wipe()
        if event.type == p.QUIT:
            running = False

        if event.type == p.MOUSEBUTTONDOWN:
            position=event.pos
            button = event.button
            if edge_build:
                if id := board.find_node(position):
                    
                    board.add_edge(closest,board.id_dict[id])
                    d.edges=board.edges
                    edge_build=False
                    closest=None
                    active=False

            elif button==1 and not edge_build and active:
                if closest.owner == d.player:
                    edge_build=True
            else:
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
        elif event.type == p.MOUSEMOTION:
            hovering = False
            position=event.pos
            active=False
            if not edge_build:
                closest=None
                if board.player_dict[player].score >=1000:
                    distc = 1000000
                    for n in board.nodes:
                        dist = (position[0]-n.pos[0])**2 + (position[1]-n.pos[1])**2
                        if dist < (n.size+60) ** 2:
                            if dist<distc:
                                distc=dist
                                closest=n
                            if dist < (n.size+10) ** 2:
                                hovering = True

                    if closest:
                        if hovering:
                            d.highlight_node(closest)
                        elif closest.owner == players[player]:
                            d.blit_close(closest,position)
                            active=True
            else:
                d.edge_build(closest,position)
    d.blit()
    clock.tick()

    counter += 1
    if counter % 5 == 0:

        board.update()