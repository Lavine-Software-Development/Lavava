from collections import defaultdict
import numpy as np
from constants import *
from helpers import *
from randomGenerator import RandomGenerator
from node import Node
from edge import Edge
from dynamicEdge import DynamicEdge

class MapBuilder:

    def __init__(self, generator):
        self.nodes = []
        self.edges = []
        self.node_objects = []
        self.edge_objects = []
        self.edgeDict = defaultdict(set)
        self.generator = generator

        self.make_nodes()
        self.make_edges()
        self.convert_to_objects()

    def make_nodes(self):  #assumes global list nodes is empty
        count = 0
        while count < NODE_COUNT:
            
            spot = [self.generator.randint(int(SCREEN_WIDTH/10),int(9*SCREEN_WIDTH/10)),self.generator.randint(int(SCREEN_HEIGHT/10),int(9*SCREEN_HEIGHT/10))]

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

            num1 = self.generator.randint(0, NODE_COUNT-1)
            num2 = self.generator.randint(0, NODE_COUNT-1)

            while num2 == num1:

                num2 =self.generator.randint(0, NODE_COUNT-1)
    

            combo = (min(num1, num2), max(num1, num2))

            if combo not in edge_set and self.nearby(combo) and self.check_all_overlaps(combo) and self.check_angle_constraints(combo):
                checklist.append(combo)
                edge_set.add(combo)
                self.edgeDict[num1].add(num2)
                self.edgeDict[num2].add(num1)
                myedge = (self.nodes[num1][0], self.nodes[num2][0], len(self.edges) + NODE_COUNT, count >= ONE_WAY_COUNT)
                self.edges.append(myedge)

                count += 1
        #print(self.is_valid_map(checklist))
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

    def starter_mines(nodes: dict[int: Node]):
        return_nodes = []
        island_mines = 0
        network_mines = 0
        for node in nodes.values():
            if len(node.edges) == 0:
                if island_mines < ISLAND_RESOURCE_COUNT:
                    node.set_state('mine', True)
                    return_nodes.append(node)
                    island_mines += 1
            else:
                if sum(1 for edge in node.incoming if edge.state == 'one-way') and \
                    network_mines < NETWORK_RESOURCE_COUNT and \
                    not any(1 for neigh in node.neighbors if neigh.state_name == 'mine'):
                        node.set_state('mine', False)
                        network_mines += 1
                return_nodes.append(node)

        return return_nodes

    def starter_capitals(nodes: dict[int: Node]):
        return_nodes = []
        capitals = 0
        for node in nodes.values():
            if len(node.edges) != 0:
                if sum(1 for edge in node.incoming if edge.state == 'one-way') and \
                    capitals < CAPITAL_START_COUNT and \
                    not any(1 for neigh in node.neighbors if neigh.state_name == 'capital'):
                        node.set_state('capital')
                        capitals += 1
                return_nodes.append(node)
        return return_nodes         

    def convert_to_objects(self):
        node_to_edge = {}
        dynamic_edges = {}
        nodes = {}
        edges = []

        for node in self.nodes:
            nodes[node[0]] = Node(node[0], node[1])

        for edge in self.edges:
            id1, id2, id3, dynamic = edge[0], edge[1], edge[2], edge[3]
            if dynamic:
                edges.append(DynamicEdge(nodes[id1], nodes[id2], id3))
            else:
                edges.append(Edge(nodes[id1], nodes[id2], id3))

        if CONTEXT['mode']['name'] == MONEY:
            nodes = self.starter_mines(nodes)

        elif CONTEXT['mode']['name'] == RELOAD:
            nodes = self.starter_capitals(nodes)

        self.edge_objects = edges
        self.node_objects = nodes