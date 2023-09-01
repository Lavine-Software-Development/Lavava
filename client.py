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
        board.buy_new_edge(id, acting_player, button)

def tick():
    board.update()

n = Network(action, tick)
print("network done")
player = n.player
board = Board(*(n.board))
players = board.player_dict
clock = p.time.Clock()
d = Draw(board, players[player], [players[0], players[1]])

in_draw= False
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
            if players[player].drawing:
                if button == 3:
                    in_draw = not in_draw
                    d.set_highlight(None)
                    d.set_close(None)
                    active=False
                    closest=None
                    players[player].drawing=False
                if id := board.find_node(position):
                    
                    if edge_id := board.check_new_edge(id, closest.id):
                        n.send((edge_id, id, closest.id))
                    d.edges=board.edges
                    players[player].drawing=False
                    closest=None
                    active=False

            elif button==1 and not players[player].drawing and active:
                if closest.owner == players[player]:
                    players[player].drawing=True
            elif id := board.find_node(position):
                n.send((id, player, button))
            elif id := board.find_edge(position):
                n.send((id, player, button))
            else:
                in_draw = not in_draw
                d.set_highlight(None)
                d.set_close(None)
                active=False
                closest=None
                players[player].drawing=False


        elif event.type == p.MOUSEMOTION and in_draw:
            hovering = False
            position=event.pos
            active=False
            d.set_highlight(None)
            d.set_close(None)
            if not players[player].drawing:
                closest=None
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
                        d.set_highlight(closest)
                    elif closest.owner == players[player] and players[player].money >= 500:
                        d.set_close((closest.pos,position))
                        active=True
            else:
                d.set_close((closest.pos,position))

    d.blit()