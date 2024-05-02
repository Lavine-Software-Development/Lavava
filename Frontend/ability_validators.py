from Backend.constants import CANNON_SHOT_CODE
from constants import SPAWN_CODE, BRIDGE_CODE, D_BRIDGE_CODE, POISON_CODE, NUKE_CODE, CAPITAL_CODE, BURN_CODE, FREEZE_CODE, RAGE_CODE, ZOMBIE_CODE, CANNON_CODE, MINIMUM_TRANSFER_VALUE


def no_click(data):
    return False

def standard_port_node(data):
    node = data[0]
    return node.owner is not None and node.is_port and node.state_name not in ["mine"]

def unowned_node(data):
    node = data[0]
    return node.owner is None and node.state_name == "default"

def capital_validator(neighbors, player):
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
    
    def cannon_shot_validator(data):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == player and first_node.state_name == "cannon" and first_node.value > MINIMUM_TRANSFER_VALUE
        else:
            second_node = data[1]
            return not (second_node.owner == player and second_node.full)
    
    return {
        POISON_CODE: standard_node_attack,
        NUKE_CODE: standard_node_attack,
        FREEZE_CODE: dynamic_edge_own_either,
        ZOMBIE_CODE: my_node,
        CANNON_CODE: my_node,
        CANNON_SHOT_CODE: cannon_shot_validator
    }


def new_edge_validator(check_new_edge, player):
    def new_edge_standard(data):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == player
        else:
            first_node, second_node = data[0], data[1]
            return first_node.id != second_node.id and check_new_edge(
                first_node.id, second_node.id
            )

    def new_edge_ports(data):
        if all([node.port_count > 0 for node in data]):
            return new_edge_standard(data)
        return False

    return new_edge_ports


def make_ability_validators(logic, player):
    return {
        SPAWN_CODE: unowned_node,
        BRIDGE_CODE: new_edge_validator(logic.check_new_edge, player),
        D_BRIDGE_CODE: new_edge_validator(logic.check_new_edge, player),
        BURN_CODE: standard_port_node, 
        RAGE_CODE: no_click,
        CAPITAL_CODE: capital_validator(logic.neighbors, player),
    } | player_validators(player)

