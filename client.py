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
    if id in board.id_dict:
        board.id_dict[id].click(players[acting_player], button)
    else:
        board.check_new_edge(id, acting_player, button)

def tick():
    board.update()

n = Network(action, tick)
print("network done")
player = n.player
board = Board(*(n.board))
players = board.player_dict
clock = p.time.Clock()
d = Draw(board.edges, board.nodes, players[player], [players[0], players[1]])

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
                    
                    if edge_id := board.check_new_edge(id, closest.id):
                        n.send((edge_id, id, closest.id))
                    d.edges=board.edges
                    edge_build=False
                    closest=None
                    active=False

            elif button==1 and not edge_build and active:
                if closest.owner == d.player:
                    edge_build=True
            else:
                if id := board.find_node(position):
                    n.send((id, player, button))
                elif id := board.find_edge(position):
                    n.send((id, player, button))

        elif event.type == p.MOUSEMOTION:
            hovering = False
            position=event.pos
            active=False
            if not edge_build:
                closest=None
                if players[player].money >= 500:
                    distc = 1000000
                    for node in board.nodes:
                        dist = (position[0]-node.pos[0])**2 + (position[1]-node.pos[1])**2
                        if dist < (node.size+60) ** 2:
                            if dist<distc:
                                distc=dist
                                closest=node
                            if dist < (node.size+10) ** 2:
                                hovering = True

                    if closest:
                        if hovering:
                            d.highlight_node(closest)
                            print("hovering")
                        elif closest.owner == players[player]:
                            d.blit_close(closest,position)
                            active=True
            else:
                d.edge_build(closest,position)

    d.blit()