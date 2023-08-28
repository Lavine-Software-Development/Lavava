from collections import defaultdict
import random
import numpy as np
from constants import *
from helpers import *

class MapBuilder:

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.edgeDict = defaultdict(set)

        self.make_nodes()
        self.make_edges()

    def make_nodes(self):  #assumes global list nodes is empty
        count = 0
        while count < NODE_COUNT:
            
            spot = [random.randint(int(SCREEN_WIDTH/10),int(9*SCREEN_WIDTH/10)),random.randint(int(SCREEN_HEIGHT/10),int(9*SCREEN_HEIGHT/10))]

            works=True

            for node in self.nodes:

                if np.sqrt((spot[0]-node[1][0])**2+(spot[1]-node[1][1])**2) < 3*min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5):

                    works=False

            if works:
                self.nodes.append((count, spot))
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
                myedge = (self.nodes[num1][0], self.nodes[num2][0], len(self.edges) + NODE_COUNT, count%3!=0)
                self.edges.append(myedge)

                count += 1

    def overlap(self, edge1,edge2):
        return do_intersect(self.nodes[edge1[0]][1],self.nodes[edge1[1]][1],self.nodes[edge2[0]][1],self.nodes[edge2[1]][1])

    def check_all_overlaps(self, edge):

        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def nearby(self, edge):
        return np.sqrt((self.nodes[edge[0]][1][0]-self.nodes[edge[1]][1][0])**2+(self.nodes[edge[0]][1][1]-self.nodes[edge[1]][1][1])**2) < 6 * min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5)

    def repr(self, num) -> str:
        node_strs = []
        for node in self.nodes:
            node_strs.append(f"Node({node[0]}, {node[1][0]}, {node[1][1]})")

        edge_strs = []
        for edge in self.edges:
            edge_strs.append(f"Edge({edge[0]}, {edge[1]}, {edge[2]}, {edge[3]})")

        return f"{num}Board(Nodes: [{', '.join(node_strs)}], Edges: [{', '.join(edge_strs)}])"