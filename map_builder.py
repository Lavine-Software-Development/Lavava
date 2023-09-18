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


    def find(self, x, parent):
        if parent[x] != x:
            parent[x] = self.find(parent[x], parent)
        return parent[x]

    def union(self, x, y, parent, rank):
        root_x = self.find(x, parent)
        root_y = self.find(y, parent)
        
        if root_x != root_y:
            if rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                if rank[root_x] == rank[root_y]:
                    rank[root_y] += 1

    def is_valid_map(self,edges):
        nodes = set()
        for x, y in edges:
            nodes.add(x)
            nodes.add(y)
        
        parent = {node: node for node in nodes}
        rank = {node: 0 for node in nodes}
        component_size = {node: 1 for node in nodes}
        
        for x, y in edges:
            root_x = self.find(x, parent)
            root_y = self.find(y, parent)
            
            if root_x != root_y:
                component_size[root_x] -= 1
                component_size[root_y] += 1
                self.union(x, y, parent, rank)
        
        islands = set()
        for node in parent.keys():
            islands.add(self.find(node, parent))
        
        if len(islands) != ISLAND_COUNT:
            return False
        
        for island in islands:
            if component_size[island] < ISLAND_MIN_NODES:
                return False
        
        return True

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

        checklist=[]
        edge_set = set()

        count = 0

        while count < EDGE_COUNT:

            num1 = random.randint(0, NODE_COUNT-1)
            num2 = random.randint(0, NODE_COUNT-1)

            while num2 == num1:

                num2 = random.randint(0, NODE_COUNT-1)
    

            combo = (min(num1, num2), max(num1, num2))

            if combo not in edge_set and self.nearby(combo) and self.check_all_overlaps(combo) and self.check_angle_constraints(combo):
                checklist.append(combo)
                edge_set.add(combo)
                self.edgeDict[num1].add(num2)
                self.edgeDict[num2].add(num1)
                myedge = (self.nodes[num1][0], self.nodes[num2][0], len(self.edges) + NODE_COUNT, count%3!=0)
                self.edges.append(myedge)

                count += 1
        print(self.is_valid_map(checklist))
    def overlap(self, edge1,edge2):
        return do_intersect(self.nodes[edge1[0]][1],self.nodes[edge1[1]][1],self.nodes[edge2[0]][1],self.nodes[edge2[1]][1])

    def check_all_overlaps(self, edge):

        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def check_angle_constraints(self, new_edge):
        p1 = self.nodes[new_edge[0]][1]
        p2 = self.nodes[new_edge[1]][1]
        
        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if new_edge[0] == key or new_edge[0] == val:
                    q1 = self.nodes[key][1]
                    q2 = self.nodes[val][1]
                    angle = angle_between_edges((p1, p2), (q1, q2))
                    if angle < MIN_ANGLE:
                        return False
                if new_edge[1] == key or new_edge[1] == val:
                    q1 = self.nodes[key][1]
                    q2 = self.nodes[val][1]
                    angle = angle_between_edges((p1, p2), (q1, q2))
                    if angle < MIN_ANGLE:
                        return False
        return True

    def nearby(self, edge):
        return np.sqrt((self.nodes[edge[0]][1][0]-self.nodes[edge[1]][1][0])**2+(self.nodes[edge[0]][1][1]-self.nodes[edge[1]][1][1])**2) < MAX_EDGE_LENGTH * min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5)

    def repr(self, player, player_count) -> str:
        node_strs = []
        for node in self.nodes:
            node_strs.append(f"Node({node[0]}, {node[1][0]}, {node[1][1]})")

        edge_strs = []
        for edge in self.edges:
            edge_strs.append(f"Edge({edge[0]}, {edge[1]}, {edge[2]}, {edge[3]})")

        return f"{player},{player_count}Board(Nodes: [{', '.join(node_strs)}], Edges: [{', '.join(edge_strs)}])"