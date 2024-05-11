from collections import defaultdict

from event import Event
from jsonable import JsonableTracked
from constants import (
    CANNON_SHOT_CODE,
    DYNAMIC_EDGE,
    GROWTH_STOP,
    MINIMUM_TRANSFER_VALUE,
    SCREEN_WIDTH,
    HORIZONTAL_ABILITY_GAP,
    NODE_COUNT,
    EDGE_COUNT,
)
from helpers import do_intersect
from edge import Edge
from dynamicEdge import DynamicEdge
from tracker import Tracker
from tracking_decorator.track_changes import track_changes


@track_changes("nodes_r", "edges_r")
class Board(JsonableTracked):
    def __init__(self, gs):
        self.gs = gs
        self.nodes = []
        self.edges = []
        self.events = self.make_events_dict()
        self.edge_dict = defaultdict(set)
        self.extra_edges = 0
        self.tracker = Tracker()
        self.player_capitals = defaultdict(set)

        recurse_values = {"nodes", "edges"}
        super().__init__("board", recurse_values, recurse_values)


    def board_wide_effect(self, player, effect):
        for node in self.nodes:
            if node.owner == player:
                node.set_state(effect)

    def track_starting_states(self):
        for node in self.nodes:
            if node.state_name != "default":
                self.tracker.node(node)

    def track_state_changes(self, nodes):

        self.player_capitals.clear()

        for node in nodes:
            self.tracker.node(node)
            node.updated = False

        for id in self.tracker.tracked_id_states:
            node = self.id_dict[id]
            if node.state_name == "capital" and node.owner:
                self.player_capitals[node.owner].add(node)

    def reset(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edge_dict = defaultdict(set)
        self.expand_nodes()
        # Gross. Mode Ports as a boolean could be used in multiple places
        self.id_dict = {node.id: node for node in self.nodes} | {
            edge.id: edge for edge in self.edges
        }
        self.extra_edges = 0
        self.tracker.reset()
        self.player_capitals.clear()
        self.track_starting_states()

    def eliminate(self, player):
        for edge in self.edges:
            if edge.controlled_by(player):
                edge.switch(False)

    def expand_nodes(self):
        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH * (1 - HORIZONTAL_ABILITY_GAP)
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)
            node.set_pos_per()

    def update(self):
        updated_nodes = []

        for spot in self.nodes:
            if spot.owned_and_alive():  # keep
                spot.grow()
            if spot.updated:
                updated_nodes.append(spot)

        for edge in self.edges:
            edge.update()

        if updated_nodes:
            self.track_state_changes(updated_nodes)

        for player in self.player_capitals:
            player.full_capital_count = len([n for n in self.player_capitals[player] if n.full()])

    def check_new_edge(self, node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in self.edges}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not self.check_all_overlaps((node_to, node_from)):
            return False
        return True

    def new_edge_id(self):
        return (
            NODE_COUNT
            + EDGE_COUNT
            + self.extra_edges
        )

    def check_all_overlaps(self, edge):
        edgeDict = defaultdict(set)
        self.nodeDict = {node.id: (node.pos) for node in self.nodes}
        for e in self.edges:
            edgeDict[e.to_node.id].add(e.from_node.id)
            edgeDict[e.from_node.id].add(e.to_node.id)

        for key in edgeDict:
            for val in edgeDict[key]:
                if (
                    edge[0] != val
                    and edge[0] != key
                    and edge[1] != val
                    and edge[1] != key
                ):
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def overlap(self, edge1, edge2):
        return do_intersect(
            self.nodeDict[edge1[0]],
            self.nodeDict[edge1[1]],
            self.nodeDict[edge2[0]],
            self.nodeDict[edge2[1]],
        )

    def buy_new_edge(self, node_from, node_to, edge_type):
        new_id = self.new_edge_id()
        if edge_type == DYNAMIC_EDGE:
            newEdge = DynamicEdge(node_to, node_from, new_id)
        else:
            newEdge = Edge(node_to, node_from, new_id)

        newEdge.check_status()
        newEdge.popped = True
        newEdge.switch(True)
        self.edges.append(newEdge)
        self.id_dict[newEdge.id] = newEdge
        self.extra_edges += 1

        newEdge.tracked_attributes.update(newEdge.start_values)

    def remove_node(self, node):
        node.owner.count -= 1
        for edge in node.outgoing | node.incoming:
            opp = edge.opposite(node)
            opp.incoming.discard(edge)
            opp.outgoing.discard(edge)
            if edge.id in self.id_dict:
                self.id_dict.pop(edge.id)
                self.edges.remove(edge)
        self.id_dict.pop(node.id)
        self.nodes.remove(node)

    def click(self, id, player, key):
        self.id_dict[id].click(player, key)

    def cannon_shot_check(self, player, data):
        cannon, target = self.id_dict[data[0]], self.id_dict[data[1]]
        can_shoot = cannon.state_name == "cannon" and cannon.owner == player
        can_accept = cannon.value > MINIMUM_TRANSFER_VALUE and (target.owner != player or not target.full)
        return can_shoot and can_accept

    def cannon_shot(self, player, data):
        cannon, target = self.id_dict[data[0]], self.id_dict[data[1]]
        if target.owner == player:
            transfer = min(cannon.value - MINIMUM_TRANSFER_VALUE, GROWTH_STOP - target.value)
        else:
            transfer = cannon.value - MINIMUM_TRANSFER_VALUE
        cannon.value -= transfer
        target.delivery(transfer, player)
    

    def make_events_dict(self):
        return {
            CANNON_SHOT_CODE: Event(self.cannon_shot_check, self.cannon_shot)
        }
