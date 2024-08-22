from collections import defaultdict

from node import Node
from jsonable import JsonableTracked
from constants import (
    DYNAMIC_EDGE,
    SCREEN_WIDTH,
    HORIZONTAL_ABILITY_GAP,
    NODE_COUNT,
    EDGE_COUNT,
    CAPITALS_NEEDED_FOR_WIN,
    STRUCTURE_RANGES,
)
from helpers import do_intersect
from edge import Edge
from dynamicEdge import DynamicEdge

# from tracker import Tracker
from capital_tracker import CapitalTracker
from tracking_decorator.track_changes import track_changes


@track_changes("nodes_r", "edges_r", "full_player_capitals")
class Board(JsonableTracked):
    def __init__(self, gs, track_capitals):
        self.gs = gs
        self.nodes: list[Node] = []
        self.edges = []
        self.edge_dict = defaultdict(set)
        self.extra_edges = 0
        # self.tracker = Tracker()
        self.tracker = CapitalTracker()
        self.player_capitals = defaultdict(set)
        self.full_player_capitals = [0] * 4
        self.track_capitals = track_capitals

        recurse_values = {"nodes", "edges"}
        super().__init__("board", recurse_values, recurse_values, recurse_values)

    def board_wide_effect(self, effect, player):
        for node in self.nodes:
            if (not player) or node.owner == player:
                node.set_state(effect)

    @property
    def accessible_nodes(self):
        return {node for node in self.nodes if node.accessible}

    @property
    def unclaimed_nodes(self):
        return {node for node in self.nodes if not node.owner}

    def find_edge(self, from_node_id, to_node_id):
        from_node, to_node = self.id_dict[from_node_id], self.id_dict[to_node_id]
        for edge in from_node.edges:
            if edge.opposite(from_node) == to_node:
                return edge
        return False

    def make_accessible(self):
        for node in self.nodes:
            node.make_accessible()

    def track_starting_states(self):
        for node in self.nodes:
            # if node.state_name != "default":
            #     self.tracker.node(node)
            if node.state_name == "capital" and node.owner:
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

    def get_player_structures(self, player):
        return {
            node
            for node in self.nodes
            if node.state_name in STRUCTURE_RANGES and node.owner == player
        }

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
        for node in self.nodes:
            if node.owner == player:
                node.set_state("default")

    def expand_nodes(self):
        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        experimental_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH * (1 - HORIZONTAL_ABILITY_GAP)
        scaling_factor = (
            new_width / experimental_width if experimental_width != 0 else 1
        )

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)
            node.set_pos_per()

    def end_game(self):
        for node in self.nodes:
            node.apply_modifications()

    def update(self):
        updated_nodes = []

        for spot in self.nodes:
            if spot.owned_and_alive():  # keep
                spot.tick()
            if spot.updated:
                updated_nodes.append(spot)

        for edge in self.edges:
            edge.update()

        if updated_nodes:
            self.track_state_changes(updated_nodes)

        if self.track_capitals:
            self.full_player_capitals = [
                0
            ] * 4  ## Should not be hard coded. This stores extra 0's
            for player in self.player_capitals:
                for node in self.player_capitals[player]:
                    self.full_player_capitals[player.id] += int(node.full())

    def check_new_edge(self, node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in self.edges}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not self.check_all_overlaps((node_to, node_from)):
            return False
        return True

    def victory_check(self):
        return self.track_capitals and any(
            count >= CAPITALS_NEEDED_FOR_WIN for count in self.full_player_capitals
        )

    def new_edge_id(self):
        return NODE_COUNT + EDGE_COUNT + self.extra_edges

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
        try:
            return do_intersect(
                self.nodeDict[edge1[0]],
                self.nodeDict[edge1[1]],
                self.nodeDict[edge2[0]],
                self.nodeDict[edge2[1]],
            )
        except KeyError:
            return False

    def buy_new_edge(
        self, node_from, node_to, edge_type, only_to_node_port, destroy_ports
    ):
        new_id = self.new_edge_id()
        if edge_type == DYNAMIC_EDGE:
            newEdge = DynamicEdge(node_to, node_from, new_id)
        else:
            newEdge = Edge(node_to, node_from, new_id)

        # if not mini bridge, then destroy ports
        if destroy_ports:
            node_to.is_port = False
            if not only_to_node_port:
                node_from.is_port = False

        newEdge.check_status()
        newEdge.popped = True
        newEdge.switch(True)
        self.edges.append(newEdge)
        self.id_dict[newEdge.id] = newEdge
        self.extra_edges += 1

        newEdge.tracked_attributes.update(newEdge.start_values)

    def remove_node(self, node):
        if node.owner:
            node.owner.count -= 1
        for edge in node.edges:
            opp = edge.opposite(node)
            opp.edges.discard(edge)
            if edge.id in self.id_dict:
                self.id_dict.pop(edge.id)
                self.edges.remove(edge)
        self.id_dict.pop(node.id)
        self.nodes.remove(node)

    def player_energy_count(self, player_energy):
        for node in self.nodes:
            if node.owner:
                player_energy[node.owner.id] += node.value
        return player_energy
