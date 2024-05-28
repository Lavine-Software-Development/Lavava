from constants import SPAWN_CODE, BRIDGE_CODE, D_BRIDGE_CODE, POISON_CODE, NUKE_CODE, CAPITAL_CODE, BURN_CODE, FREEZE_CODE, RAGE_CODE, ZOMBIE_CODE, CANNON_CODE, MINIMUM_TRANSFER_VALUE, CANNON_SHOT_CODE, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK
from collections import defaultdict


def no_click(data):
    return False

def standard_port_node(data):
    node = data[0]
    return node.owner is not None and node.is_port and node.state_name not in ["mine"]

def unowned_node(data):
    node = data[0]
    return node.owner is None and node.state_name == "default"

def capital_validator(player, edges):

    def neighbors(node):
        neighbors = []
        for edge in edges.values():
            try:
                neighbor = edge.other(node)
                neighbors.append(neighbor)
            except ValueError:
                continue
        return neighbors

    def capital_logic(data):
        node = data[0]
        if (
            node.owner == player
            and node.state_name != "capital"
            and node.full
        ):
            neighbor_capital = False
            for neighbor in neighbors(node):
                if neighbor.state_name == "capital":
                    neighbor_capital = True
                    break
            if not neighbor_capital:
                return True
        return False
    return capital_logic


def player_validators(player):
    
    def standard_node_attack(data):
        node = data[0]
        return (
            node.owner != player
            and node.owner is not None
            and node.state_name not in ["capital", "mine"]
        )

    def my_node(data):
        node = data[0]
        return node.owner == player

    def dynamic_edge_own_either(data):
        edge = data[0]
        return edge.dynamic and (edge.from_node.owner == player)

    
    return {
        POISON_CODE: standard_node_attack,
        NUKE_CODE: standard_node_attack,
        FREEZE_CODE: dynamic_edge_own_either,
        ZOMBIE_CODE: my_node,
        CANNON_CODE: my_node,
    }


def new_edge_validator(player, nodes, edges):

    def on_segment(p, q, r):
        return (
            q[0] <= max(p[0], r[0])
            and q[0] >= min(p[0], r[0])
            and q[1] <= max(p[1], r[1])
            and q[1] >= min(p[1], r[1])
        )

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise

    def do_intersect(p1, q1, p2, q2):
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True
        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True
        return False

    def overlap(edge1, edge2):
        return do_intersect(
            nodes[edge1[0]].pos,
            nodes[edge1[1]].pos,
            nodes[edge2[0]].pos,
            nodes[edge2[1]].pos,
        )

    def check_all_overlaps(edge):
        edgeDict = defaultdict(set)
        for e in edges.values():
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
                    if overlap(edge, (key, val)):
                        return False
        return True

    def check_new_edge(node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in edges.values()}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not check_all_overlaps((node_to, node_from)):
            return False
        return True

    def new_edge_standard(data):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == player
        else:
            first_node, second_node = data[0], data[1]
            return first_node.id != second_node.id and check_new_edge(first_node.id, second_node.id)

    def new_edge_ports(data):
        if all([node.port_count > 0 for node in data]):
            return new_edge_standard(data)
        return False

    return new_edge_ports


def make_ability_validators(player, nodes, edges):
    return {
        SPAWN_CODE: unowned_node,
        BRIDGE_CODE: new_edge_validator(player, nodes, edges),
        D_BRIDGE_CODE: new_edge_validator(player, nodes, edges),
        BURN_CODE: standard_port_node, 
        RAGE_CODE: no_click,
        CAPITAL_CODE: capital_validator(player, edges),
    } | player_validators(player)


def make_event_validators(player):

    def cannon_shot_validator(data):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == player and first_node.state_name == "cannon" and first_node.value > MINIMUM_TRANSFER_VALUE
        else:
            second_node = data[1]
            return not (second_node.owner == player and second_node.full)
        
    def edge_validator(data):
        edge = data[0]
        return edge.controlled_by(player)
        
    return {
        CANNON_SHOT_CODE: cannon_shot_validator,
        STANDARD_LEFT_CLICK: edge_validator,
        STANDARD_RIGHT_CLICK: edge_validator,
    }

