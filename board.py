import math
from collections import defaultdict
from player import Player
from constants import COLOR_DICT
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

    def stray_from_node(self, node_id, position):
        node = self.id_dict[node_id]
        if math.sqrt((position[0]-node.pos[0])**2 + (position[1]-node.pos[1])**2) >= int(5+size_factor(node.value)*18)+1:
            return True
        return False
