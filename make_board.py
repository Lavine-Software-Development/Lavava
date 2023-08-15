import pygame as p
import numpy as np
import random
from collections import defaultdict
from node import Node
from edge import Edge
from player import Player
 

NODE_COUNT = 80

EDGE_COUNT = 100

SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 1000





p.init()

 

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

nodes = []
edges = []

####################
 

edge_set = set()

edgeDict = defaultdict(set)

 

#####################

 

def orientation(p, q, r):

    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:

        return 0  # Collinear

    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

 

def on_segment(p, q, r):

    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and

            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

 

def do_intersect(p1, q1, p2, q2):

    o1 = orientation(p1, q1, p2)

    o2 = orientation(p1, q1, q2)

    o3 = orientation(p2, q2, p1)

    o4 = orientation(p2, q2, q1)

 

    if o1 != o2 and o3 != o4:

        return True

 

    if o1 == 0 and on_segment(p1, p2, q1):

        return True

 

    if o2 == 0 and on_segment(p1, q2, q1):

        return True

 

    if o3 == 0 and on_segment(p2, p1, q2):

        return True

 

    if o4 == 0 and on_segment(p2, q1, q2):

        return True

 

    return False

 

def overlap(edge1,edge2):

    return do_intersect(nodes[edge1[0]].pos,nodes[edge1[1]].pos,nodes[edge2[0]].pos,nodes[edge2[1]].pos)

   

 

def check_all_overlaps(edge):

    for key in edgeDict:

        for val in edgeDict[key]:

            if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:

                if overlap(edge, (key, val)):

                    return False

    return True

 

def nearby(edge):

    return np.sqrt((nodes[edge[0]].pos[0]-nodes[edge[1]].pos[0])**2+(nodes[edge[0]].pos[1]-nodes[edge[1]].pos[1])**2) < 6 * min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5)

def make_nodes():  #assumes global list nodes is empty
    count = 0
    while count < NODE_COUNT:
        
        spot = [random.randint(int(SCREEN_WIDTH/10),int(9*SCREEN_WIDTH/10)),random.randint(int(SCREEN_HEIGHT/10),int(9*SCREEN_HEIGHT/10))]

        works=True

        for node in nodes:

            if np.sqrt((spot[0]-node.pos[0])**2+(spot[1]-node.pos[1])**2) < 3*min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5):

                works=False

        if works:
            nodes.append(Node(count, spot))
            count += 1

def make_edges():   #assumes global list edges is empty

    edge_set = set()

    count = 0

    while count < EDGE_COUNT:

        num1 = random.randint(0, NODE_COUNT-1)
        num2 = random.randint(0, NODE_COUNT-1)

        while num2 == num1:

            num2 = random.randint(0, NODE_COUNT-1)
 

        combo = (min(num1, num2), max(num1, num2))

        if combo not in edge_set and nearby(combo) and check_all_overlaps(combo):

            edge_set.add(combo)
            edgeDict[num1].add(num2)
            edgeDict[num2].add(num1)
            edges.append(Edge(nodes[num1], nodes[num2]))

            count += 1

##########################

def blit_edges():

    for edge in edges:

        # linelength = np.sqrt((edge.nodes[0].pos[0]-edge.nodes[1].pos[0])**2+(edge.nodes[0].pos[1]-edge.nodes[1].pos[1])**2)

        p.draw.line(screen,(50,50,50), edge.nodes[0].pos, edge.nodes[1].pos,2)

            #int(min(SCREEN_HEIGHT,SCREEN_WIDTH)/(linelength))

 

def blit_nodes():

    for spot in nodes:

        p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)

    p.display.update()

######################




make_nodes()
make_edges()

running=True

blit_edges()

# This is a demonstration of clicking. First node can be selected, others only work if they're neighbor has
# been selected. \/
player = Player(BLUE)
owned = []

for spot in nodes:
    if spot.click(player):
        owned.append(spot)

print(len(owned))

while running:

    for event in p.event.get():

        if event.type == p.QUIT:

            running= False

        elif event.type == p.MOUSEBUTTONDOWN:
            nodes = [] #reset
            edges = [] #reset
            edge_set = set()

            edgeDict = defaultdict(set)
            position=event.pos
            screen.fill(WHITE)
            make_nodes()
            make_edges()
            blit_edges()
            blit_nodes()

            # call click on the node which is in the range

        # p.draw.circle(screen, BLACK, (position[0],position[1]), 20, 0)
    for spot in owned:
        spot.grow()

    # p.display.update()
    blit_nodes()