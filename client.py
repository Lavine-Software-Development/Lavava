import pygame as p
from network import Network
from board import Board
from draw import Draw

p.init()

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
    for play in players:
        players[play].money += players[play].tick_production

n = Network(action, tick)
print("network done")
player_num = n.player
board = Board(*(n.board))
players = board.player_dict
player = players[player_num]
clock = p.time.Clock()
d = Draw(board, player_num, [players[0], players[1]])

in_draw= False
active=False
closest=None
position = None

while running:

    for event in p.event.get():
        d.wipe()
    
        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:
            if event.key == p.K_a:
                player.switch_considering()

        if event.type == p.MOUSEBUTTONDOWN:
            position = event.pos
            button = event.button
            if id := board.find_node(position):
                if player.considering_edge:
                    if player.new_edge_started():
                        if new_edge_id := board.check_new_edge(player.new_edge_start.id, id):
                            n.send((new_edge_id, player.new_edge_start.id, id))
                            player.switch_considering()
                    else:
                        if board.id_dict[id].owner == player:
                            player.new_edge_start = board.id_dict[id]
                else:
                    n.send((id, player_num, button))
            elif id := board.find_edge(position):
                n.send((id, player_num, button))
            elif player.considering_edge:
                player.new_edge_start = None

        if event.type == p.MOUSEMOTION:
            position=event.pos
            if id := board.find_node(position):
                player.highlighted_node = board.id_dict[id]
            else:
                player.highlighted_node = None

    d.blit(position)