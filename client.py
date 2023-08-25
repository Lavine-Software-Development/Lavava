import pygame as p
import math
from network import Network
from draw import Draw

p.init()

WHITE = (255, 255, 255)

n = Network()
player = n.getPlayer()
board = n.getBoard()
nodes = board.nodes
edges = board.edges
clock = p.time.Clock()
d = Draw(edges, nodes, player)

running = True
shitcount = 0

while running:

    for event in p.event.get():

        if event.type == p.QUIT:
            running = False

    d.blit()
    clock.tick()
    shitcount+=1
    if shitcount %10==0:
        for spot in nodes:
            if spot.owner:
                spot.grow()
                spot.calculate_threatened_score()
            if spot.pressed == 1:
                spot.absorb()
            elif spot.pressed == 3:
                spot.expel()