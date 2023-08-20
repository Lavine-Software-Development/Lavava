from node import Node 
from edge import Edge
import time
from make_board import board
import pygame as p


nodes, edges = board()

p.init()


SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 1000

size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = p.display.set_mode(size)


p.display.set_caption("Lavava")

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

YELLOW = (255,255,51)


screen.fill(WHITE)
p.display.update()
clock = p.time.Clock()

def blit_edges():

    for edge in edges:

        # linelength = np.sqrt((edge.nodes[0].pos[0]-edge.nodes[1].pos[0])**2+(edge.nodes[0].pos[1]-edge.nodes[1].pos[1])**2)

        p.draw.line(screen,(50,50,50), edge.to_node.pos, edge.from_node.pos,2)

            #int(min(SCREEN_HEIGHT,SCREEN_WIDTH)/(linelength))
 

def blit_nodes():

    for spot in nodes:

        p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)

    p.display.update()


running=True


while running:

    for event in p.event.get():

        if event.type == p.QUIT:

            running = False

        # if a click is detected, check if it's on a node. If it is, call click() on that node.

    blit_edges()
    blit_nodes()
    p.display.update()
    clock.tick(40)




# This is a demonstration of clicking. First node can be selected, others only work if they're neighbor has
# been selected. \/
# player = Player(BLUE)
# owned = []

# for spot in nodes:
#     if spot.click(player):
#         owned.append(spot)

# print(len(owned))


#         # p.draw.circle(screen, BLACK, (position[0],position[1]), 20, 0)
# for spot in owned:
#     spot.grow()