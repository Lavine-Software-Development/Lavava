from collections import defaultdict
from Server.constants import (
    EDGE,
    DYNAMIC_EDGE,
    GREY,
    SCREEN_WIDTH,
    HORIZONTAL_ABILITY_GAP,
    NODE_COUNT,
    EDGE_COUNT,
    CONTEXT,
    NODE,
    PORT_NODE,
)
from Server.helpers import distance_point_to_segment
from edge import Edge
from dynamicEdge import DynamicEdge
from Server.gameStateEnums import GameStateEnum as GSE
from Server.tracker import Tracker


class Board:
    def __init__(self, gs):
        self.gs = gs
        self.nodes = []
        self.edges = []
        self.edge_dict = defaultdict(set)
        self.id_dict = {}
        self.extra_edges = 2
        self.highlighted = None
        self.highlighted_color = None
        self.tracker = Tracker()
        self.player_capitals = defaultdict(set)

    def reset(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edge_dict = defaultdict(set)
        self.expand_nodes()
        # Gross. Mode Ports as a boolean could be used in multiple places
        self.set_all_ports()
        if self.nodes[0].item_type == PORT_NODE:
            for node in self.nodes:
                node.set_port_angles()
        self.id_dict = {node.id: node for node in self.nodes} | {
            edge.id: edge for edge in self.edges
        }
        self.extra_edges = 2
        self.tracker.reset()
        self.player_capitals.clear()
        self.track_starting_states()

    def set_all_ports(self):
        if self.nodes[0].item_type == PORT_NODE:
            for node in self.nodes:
                node.set_port_angles()

    ## Gross code. Needs to be refactored

    ## Gross code ends here (I hope)

    def click_edge(self):
        if self.highlighted and self.highlighted.type == EDGE:
            return self.highlighted.id
        return False

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

    def find_node(self, position):
        for node in self.nodes:
            if (
                (position[0] - node.pos[0]) ** 2 + (position[1] - node.pos[1]) ** 2
            ) <= (node.size) ** 2 + 3:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if (
                distance_point_to_segment(
                    position[0],
                    position[1],
                    edge.from_node.pos[0],
                    edge.from_node.pos[1],
                    edge.to_node.pos[0],
                    edge.to_node.pos[1],
                )
                < 5
            ):
                return edge.id
        return None

    def new_edge_id(self, node_from):
        return (
            NODE_COUNT
            + EDGE_COUNT
            + self.extra_edges
            + self.id_dict[node_from].owner.id
        )

    def buy_new_edge(self, id, node_from, node_to, edge_type):
        if edge_type == DYNAMIC_EDGE:
            newEdge = DynamicEdge(self.id_dict[node_to], self.id_dict[node_from], id)
        else:
            newEdge = Edge(self.id_dict[node_to], self.id_dict[node_from], id)

        newEdge.check_status()
        newEdge.popped = True
        newEdge.switch(True)
        self.edges.append(newEdge)
        self.id_dict[newEdge.id] = newEdge
        self.extra_edges += 5

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

    @property
    def percent_energy(self):
        self_energy = 0
        energy = 0.01
        for node in self.nodes:
            if node.owner == CONTEXT["main_player"]:
                self_energy += node.value
            if node.owned_and_alive():
                energy += node.value
        return int(self_energy * 100 / energy)
