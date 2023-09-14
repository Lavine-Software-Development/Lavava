from collections import defaultdict
from player import Player
from constants import *
from helpers import *

class Board:

    def __init__(self, player_count, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.player_count = player_count

        self.edgeDict = defaultdict(set)

        self.expand_nodes()

        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.player_dict = {i: Player(COLOR_DICT[i], i) for i in range(player_count)}

        self.extra_edges = 2

        self.remaining = {i for i in range(player_count)}
        self.victor = None

    def eliminate(self, player):
        self.remaining.remove(player)
        for edge in self.edges:
            if edge.owned_by(self.player_dict[player]):
                edge.switch(False)
        self.player_dict[player].eliminate()

    def check_over(self):
        if len(self.remaining) == 1:
            self.victor = self.player_dict[list(self.remaining)[0]]
            self.victor.win()

    def expand_nodes(self):

        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH - 50
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)

    def update(self):
        for spot in self.nodes:
            if spot.owned_and_alive():
                spot.grow()

        for edge in self.edges:
            edge.update()
        
        for player in self.player_dict.values():
            out = player.update()
            if out:
                self.eliminate(player.id)

        self.check_over()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) < (node.size) ** 2:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
                return edge.id
        return None

    def check_new_edge(self, node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in self.edges}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not self.check_all_overlaps((node_to, node_from)):
            return False
        return NODE_COUNT + EDGE_COUNT + self.extra_edges + self.id_dict[node_from].owner.id

    def check_all_overlaps(self, edge):

        edgeDict = defaultdict(set)
        self.nodeDict = {node.id: (node.pos) for node in self.nodes}
        for e in self.edges:
            edgeDict[e.to_node.id].add(e.from_node.id)
            edgeDict[e.from_node.id].add(e.to_node.id)

        for key in edgeDict:
            for val in edgeDict[key]:
                if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def overlap(self, edge1,edge2):
        
        return do_intersect(self.nodeDict[edge1[0]],self.nodeDict[edge1[1]],self.nodeDict[edge2[0]],self.nodeDict[edge2[1]])
        
    def buy_new_edge(self, id, node_from, node_to):
        if self.id_dict[node_from].owner is None:
            print("ERROR: node_from has no owner", node_from.id, node_to.pos)
        elif self.id_dict[node_from].owner.buy_edge():
            print("edge building with id: ", id)
            newEdge = Edge(self.id_dict[node_to], self.id_dict[node_from], id)
            newEdge.check_status()
            self.edges.append(newEdge)
            self.id_dict[newEdge.id] = newEdge
            self.extra_edges += self.player_count