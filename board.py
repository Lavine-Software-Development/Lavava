from collections import defaultdict
from constants import *
from helpers import *
from edge import Edge
from dynamicEdge import DynamicEdge

class Board:

    def __init__(self, player_dict, nodes, edges):

        self.nodes = nodes
        self.edges = edges
        self.player_dict = player_dict

        self.player_count = len(self.player_dict)
        self.edgeDict = defaultdict(set)
        self.expand_nodes()
        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.extra_edges = 2

        self.remaining = {i for i in range(self.player_count)}
        self.victor = None

        self.timer = 60

    def eliminate(self, player):
        self.remaining.remove(player)
        for edge in self.edges:
            if edge.owned_by(self.player_dict[player]):
                edge.switch(False)
        self.player_dict[player].eliminate()

    def check_over(self):
        if len(self.remaining) == 1:
            self.win_and_end(self.player_dict[list(self.remaining)[0]])
        else:
            self.check_capital_win()

    def check_capital_win(self):
        winner = None
        for player in self.player_dict.values():
            if player.check_capital_win():
                winner = player
                break
        if winner:
            for player in self.remaining.copy():
                if player != winner.id:
                    self.eliminate(player)
            self.win_and_end(winner)

    def win_and_end(self, player):
        self.victor = player
        self.victor.win()
        self.display_ranks()

    def display_ranks(self):

        sorted_by_score = sorted(self.player_dict.values(), key=lambda p: p.points, reverse=True)

        print("New Scores")
        print("-----------------")
        for player in sorted_by_score:
            player.display()
        print()

    def expand_nodes(self):

        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH *  (1 - ABILITY_GAP)
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)
            node.set_pos_per()

    def update(self):

        self.check_over()

        if self.timer > 0:
            self.timer -= 0.1

            if self.timer > 3 and self.opening_moves == len(self.remaining):
                self.timer = 3

        else:
            for spot in self.nodes:
                if spot.owned_and_alive():
                    spot.grow()

            for edge in self.edges:
                edge.update()
            
            for player in self.player_dict.values():
                player.update()
                if player.count == 0:
                    self.eliminate(player.id)

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) <= (node.size) ** 2+3:
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
        newEdge = Edge(self.id_dict[node_to], self.id_dict[node_from], id)
        newEdge.check_status()
        newEdge.popped = True
        newEdge.switch(True)
        self.edges.append(newEdge)
        self.id_dict[newEdge.id] = newEdge
        self.extra_edges += self.player_count

    def safe_remove(self, lst, value):
        try:
            lst.remove(value)
        except ValueError:
            pass

    def remove_node(self, node_id):
        node = self.id_dict[node_id]
        node.owner.count -= 1
        for edge in node.outgoing + node.incoming:
            opp = edge.opposite(node)
            self.safe_remove(opp.incoming, edge)
            self.safe_remove(opp.incoming, edge)
            if edge.id in self.id_dict:
                self.id_dict.pop(edge.id)
                self.edges.remove(edge)
        self.id_dict.pop(node_id)
        self.nodes.remove(node)

    @property
    def opening_moves(self):
        return sum([player.count for player in self.player_dict.values()])