from constants import SPAWN_CODE, BRIDGE_CODE, D_BRIDGE_CODE, POISON_CODE, NUKE_CODE, CAPITAL_CODE, BURN_CODE, FREEZE_CODE, RAGE_CODE, ZOMBIE_CODE

def no_click(data, player):
    return False


def standard_node_attack(data, player):
    node = data[0]
    return (
        node.owner != player
        and node.owner is not None
        and node.state_name not in ["capital", "mine"]
    )

def my_node(data, player):
    node = data[0]
    return node.owner == player


def dynamic_edge_own_either(data, player):
    edge = data[0]
    return edge.state == "two-way" and (edge.from_node.owner == player)


def capital_logic(data, player):
    node = data[0]
    if (
        node.owner == player
        and node.state_name != "capital"
        and node.full()
    ):
        neighbor_capital = False
        for neighbor in node.neighbors:
            if neighbor.state_name == "capital":
                neighbor_capital = True
                break
        if not neighbor_capital:
            return True
    return False


def standard_port_node(data, player):
    node = data[0]
    return node.owner is not None and node.is_port and node.state_name not in ["mine"]


def unowned_node(data, player):
    node = data[0]
    return node.owner is None and node.state_name == "default"


def new_edge_validator(check_new_edge):
    def new_edge_standard(data, player):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == player
        else:
            first_node, second_node = data[0], data[1]
            return first_node.id != second_node.id and check_new_edge(
                first_node.id, second_node.id
            )

    def new_edge_ports(data, player):
        if all([node.port_count > 0 for node in data]):
            return new_edge_standard(data, player)
        return False

    return new_edge_ports


def make_ability_validators(board):
    return {
        SPAWN_CODE: unowned_node,
        BRIDGE_CODE: new_edge_validator(board.check_new_edge),
        D_BRIDGE_CODE: new_edge_validator(board.check_new_edge),
        POISON_CODE: standard_node_attack,
        NUKE_CODE: standard_node_attack,
        CAPITAL_CODE: capital_logic,
        BURN_CODE: standard_port_node, 
        FREEZE_CODE: dynamic_edge_own_either,
        RAGE_CODE: no_click,
        ZOMBIE_CODE: my_node
    }

