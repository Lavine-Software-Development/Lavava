import math
from collections import defaultdict
from player import Player
from constants import *
import re
from helpers import *

class Board:

    def __init__(self, player_count, nodes, edges):
        self.nodes = nodes
        self.edges = edges

        self.edgeDict = defaultdict(set)

        self.nodes = self.remove_excess_nodes()

        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.player_dict = {i: Player(COLOR_DICT[i], i) for i in range(player_count)}

    def remove_excess_nodes(self):
        return [node for node in self.nodes if len(node.incoming) + len(node.outgoing) > 0]

    def update(self):
        for spot in self.nodes:
            if spot.owner:
                spot.grow()
        for edge in self.edges:
            edge.update()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) < 14:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
                return edge.id
        return None
    def add_edge(self,nodefrom,nodeto):
        edge_set = set()
        combo = (nodefrom.id,nodeto.id)
        #if combo not in edge_set and self.nearby(combo) and self.check_all_overlaps(combo):
        edge_set.add(combo)
        self.edgeDict[nodefrom.id].add(nodeto.id)
        self.edgeDict[nodeto.id].add(nodefrom.id)
        nodefrom.outgoing.append(nodeto.id)
        nodeto.incoming.append(nodefrom.id)
        myedge = Edge(nodefrom, nodeto, len(self.edges) + NODE_COUNT)
        self.id_dict[len(self.edges) + NODE_COUNT]=myedge
        self.edges.append(myedge)

