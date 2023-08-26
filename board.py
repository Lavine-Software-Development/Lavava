import math
import random
import numpy as np
from collections import defaultdict
from node import Node
from edge import Edge
from player import Player

EDGE_COUNT = 100
NODE_COUNT = 80
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

color_dict = {0: (255,0,0), 1: (0,0,255), 2: (0,255,0)}

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq))
    
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    return distance

def size_factor(x):
    if x<5:
        return 0
    if x>=200:
        return 1
    return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

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

class Board:

    def __init__(self, player_count):
        self.nodes = []
        self.edges = []

        self.edgeDict = defaultdict(set)

        self.make_nodes()
        self.make_edges()
        self.nodes = self.remove_excess_nodes()

        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.player_dict = {i: Player(color_dict[i], i) for i in range(player_count)}

    def remove_excess_nodes(self):
        return [node for node in self.nodes if len(node.incoming) + len(node.outgoing) > 0]

    def make_nodes(self):  #assumes global list nodes is empty
        count = 0
        while count < NODE_COUNT:
            
            spot = [random.randint(int(SCREEN_WIDTH/10),int(9*SCREEN_WIDTH/10)),random.randint(int(SCREEN_HEIGHT/10),int(9*SCREEN_HEIGHT/10))]

            works=True

            for node in self.nodes:

                if np.sqrt((spot[0]-node.pos[0])**2+(spot[1]-node.pos[1])**2) < 3*min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5):

                    works=False

            if works:
                self.nodes.append(Node(count, spot))
                count += 1

    def make_edges(self):

        edge_set = set()

        count = 0

        while count < EDGE_COUNT:

            num1 = random.randint(0, NODE_COUNT-1)
            num2 = random.randint(0, NODE_COUNT-1)

            while num2 == num1:

                num2 = random.randint(0, NODE_COUNT-1)
    

            combo = (min(num1, num2), max(num1, num2))

            if combo not in edge_set and self.nearby(combo) and self.check_all_overlaps(combo):

                edge_set.add(combo)
                self.edgeDict[num1].add(num2)
                self.edgeDict[num2].add(num1)
                myedge = Edge(self.nodes[num1], self.nodes[num2], len(self.edges) + NODE_COUNT)
                if count%3==0:
                    myedge = Edge(self.nodes[num1], self.nodes[num2], len(self.edges) + NODE_COUNT, False)
                self.edges.append(myedge)

                count += 1

    def overlap(self, edge1,edge2):
        return do_intersect(self.nodes[edge1[0]].pos,self.nodes[edge1[1]].pos,self.nodes[edge2[0]].pos,self.nodes[edge2[1]].pos)

    def check_all_overlaps(self, edge):

        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def nearby(self, edge):
        return np.sqrt((self.nodes[edge[0]].pos[0]-self.nodes[edge[1]].pos[0])**2+(self.nodes[edge[0]].pos[1]-self.nodes[edge[1]].pos[1])**2) < 6 * min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5)

    def update(self):
        for spot in self.nodes:
            if spot.owner:
                spot.grow()
                spot.calculate_threatened_score()
            if spot.pressed == 1:
                spot.absorb()
            elif spot.pressed == 3:
                spot.expel()
        for edge in self.edges:
            if edge.pressed:
                edge.flow()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) < 10:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
                return edge.id
        return None

    def stray_from_node(self, node_id, position):
        node = self.id_dict[node_id]
        if math.sqrt((position[0]-node.pos[0])**2 + (position[1]-node.pos[1])**2) >= int(5+size_factor(node.value)*18)+1:
            return True
        return False
