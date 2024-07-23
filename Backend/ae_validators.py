from math import dist
from constants import BREAKDOWNS, CANNON_SHOT_CODE, MINI_BRIDGE_COST, MINI_BRIDGE_RANGE, MINIMUM_TRANSFER_VALUE, PUMP_DRAIN_CODE, SPAWN_CODE, BRIDGE_CODE, D_BRIDGE_CODE, MINI_BRIDGE_CODE, POISON_CODE, NUKE_CODE, CAPITAL_CODE, BURN_CODE, FREEZE_CODE, RAGE_CODE, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ZOMBIE_CODE, CANNON_CODE, PUMP_CODE, CREDIT_USAGE_CODE, STRUCTURE_RANGES,


def no_click(data):
    return True

def owned_burnable_node(data):
    node = data[0]
    return node.owner is not None and burnable_node(data)

# option for slightly improved burn, allowing preemptive burns before ownership
def burnable_node(data):
    node = data[0]
    return node.is_port and len(node.edges) 

def unowned_node(data):
    node = data[0]
    return node.owner is None and node.state_name == "default"

# option for improved nuke, nuking something unowned (or theoreitcally ones own)
def default_node(data):
    node = data[0]
    return node.state_name == "default"

# option for worse nuke, requiring node to be owned
def standard_node_attack(data, player):
    node = data[0]
    return (
        node.owner != player
        and node.owner is not None
    )


def attack_validators(get_structures, player):

    def capital_ranged_node_attack(data):
        node = data[0]
        structures = get_structures(player)

        def in_structure_range(structure):
            x1, y1 = node.pos
            x2, y2 = structure.pos
            distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
            structure_nuke_range = (STRUCTURE_RANGES[structure.state_name] * structure.value) ** 2
            return distance <= structure_nuke_range

        return default_node([node]) and any(in_structure_range(structure) for structure in structures)

    return capital_ranged_node_attack


def validators_needing_player(player):

    def capital_logic(data):
        node = data[0]
        if (
            node.owner == player
            and node.state_name == "default"
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
    
    # can be used for buffed zombie, allowing it to delete about to capture cannons/pumps
    def my_node(data):
        node = data[0]
        return node.owner == player
    
    def my_default_port_node(data):
        node = data[0]
        return my_default_node(data) and node.is_port
    
    # Can be used for buffed cannon, not requiring port placement. Harder to attack for bridge players
    def my_default_node(data):
        node = data[0]
        return my_node(data) and node.state_name == "default"
    
    def attacking_edge(data):
        edge = data[0]
        return my_node([edge.from_node]) and standard_node_attack([edge.to_node], player)

    def dynamic_edge_own_from_node(data):
        edge = data[0]
        return edge.dynamic and (edge.from_node.owner == player)
    
    def dynamic_edge_own_either_but_not_flowing(data):
        edge = data[0]
        return edge.dynamic and ((edge.from_node.owner == player) or (edge.to_node.owner == player and not edge.flowing))
    
    def dynamic_edge_own_either(data):
        edge = data[0]
        return edge.dynamic and (edge.from_node.owner == player or edge.to_node.owner == player)
    
    return {
        CAPITAL_CODE: capital_logic,
        POISON_CODE: attacking_edge,
        FREEZE_CODE: dynamic_edge_own_either_but_not_flowing,
        ZOMBIE_CODE: my_default_node,
        CANNON_CODE: my_default_port_node,
        PUMP_CODE: my_default_node,
    }

def no_crossovers(check_new_edge, data, player):
    first_node, second_node = data[0], data[1]
    return first_node.owner == player and first_node.id != second_node.id and check_new_edge(
        first_node.id, second_node.id
    )

def make_cannon_shot_check(check_new_edge, id_dict):
    def cannon_shot_check(player, data):
        cannon, target = id_dict[data[0]], id_dict[data[1]]
        can_shoot = cannon.state_name == "cannon" and cannon.owner == player
        can_accept = cannon.value > MINIMUM_TRANSFER_VALUE and (target.owner != player or not target.full())
        return can_shoot and can_accept and no_crossovers(check_new_edge, [id_dict[data[0]], id_dict[data[1]]], player)
    return cannon_shot_check


def make_pump_drain_check(id_dict):

    def pump_drain(player, data):
        node = id_dict[data[0]]
        return node.state_name == "pump" and node.owner == player and node.full()
        
    return pump_drain

def valid_ability_for_credits(player, data):
    ability_code = data[0]
    return ability_code in player.abilities and BREAKDOWNS[ability_code].credits <= player.credits

def make_new_edge_ports(check_new_edge, player):
    def new_edge_ports(data):
        if all([node.is_port for node in data]):
            return no_crossovers(check_new_edge, data, player)
        return False
    
    # Check if the nodes are within the range of a mini bridge
    def check_mini_bridge_range(data):
        first_node, second_node = data
        distance = dist(first_node.pos, second_node.pos)
        return distance <= MINI_BRIDGE_RANGE  # Adjust the range as needed

    def mini_bridge_validator(data):
        return check_mini_bridge_range(data) and new_edge_ports(data)

    return {
        BRIDGE_CODE: new_edge_ports,
        D_BRIDGE_CODE: new_edge_ports,
        MINI_BRIDGE_CODE: mini_bridge_validator,  # Add mini bridge validator
    }


def make_ability_validators(board, player):
    return {
        SPAWN_CODE: unowned_node,
        BURN_CODE: owned_burnable_node,
        RAGE_CODE: no_click,
        NUKE_CODE: attack_validators(board.get_player_structures, player),
    } | validators_needing_player(player) | make_new_edge_ports(board.check_new_edge, player)


def make_effect_validators(board):
    return {
        CANNON_SHOT_CODE: make_cannon_shot_check(board.check_new_edge, board.id_dict),
        PUMP_DRAIN_CODE: make_pump_drain_check(board.id_dict),
        STANDARD_LEFT_CLICK: lambda player, data: board.id_dict[data[0]].valid_left_click(player),
        STANDARD_RIGHT_CLICK: lambda player, data: board.id_dict[data[0]].valid_right_click(player),
        CREDIT_USAGE_CODE : valid_ability_for_credits,
    }

