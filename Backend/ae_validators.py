from math import dist
from constants import (
    BREAKDOWNS,
    CANNON_SHOT_CODE,
    MINI_BRIDGE_RANGE,
    MINIMUM_TRANSFER_VALUE,
    PUMP_DRAIN_CODE,
    SPAWN_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    MINI_BRIDGE_CODE,
    POISON_CODE,
    NUKE_CODE,
    CAPITAL_CODE,
    BURN_CODE,
    FREEZE_CODE,
    RAGE_CODE,
    OVER_GROW_CODE,
    STANDARD_LEFT_CLICK,
    STANDARD_RIGHT_CLICK,
    ZOMBIE_CODE,
    CANNON_CODE,
    PUMP_CODE,
    CREDIT_USAGE_CODE,
    STRUCTURE_RANGES,
    WALL_CODE,
    WORMHOLE_CODE,
)


def no_click(data):
    return True


def owned_burnable_node(data):
    node = data[0]
    return node.owner is not None and burnable_node(data)


def non_walled_node(data):
    node = data[0]
    return node.wall_count == 0


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
    return node.owner != player and node.owner is not None


def attack_validators(get_structures, player, attack_type):
    def structure_ranged_default_attack(data):
        return default_node(data) and (
            structure_ranged_node_attack(data)
            or not_attacking_neighbor_or_owner_attack(data)
        )

    def opposing_structure_ranged_attack(data):
        node = data[0]
        return node.owner != player and (
            structure_ranged_node_attack(data) or not_attacking_neighbor_attack(data)
        )

    def structure_ranged_node_attack(data):
        node = data[0]
        structures = get_structures(player)

        def in_structure_range(structure):
            x1, y1 = node.pos
            x2, y2 = structure.pos
            distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
            structure_attack_range = (
                STRUCTURE_RANGES[structure.state_name] * structure.value
            ) ** 2
            return distance <= structure_attack_range

        return any(in_structure_range(structure) for structure in structures)

    def not_attacking_edge(edge):
        return edge.from_node.owner == player or not edge.flowing

    def not_attacking_neighbor_attack(data):
        node = data[0]
        if node.owner == player:
            return False
        for edge in node.edges:
            if edge.opposite(node).owner == player and not_attacking_edge(edge):
                return True
        return False

    def neighbor_attack(data):
        node = data[0]
        if node.owner == player:
            return False
        for neighbor in node.neighbors:
            if neighbor.owner == player:
                return True
        return False

    def neighbor_or_owner_attack(data):
        node = data[0]
        return node.owner == player or neighbor_attack(data)

    def not_attacking_neighbor_or_owner_attack(data):
        node = data[0]
        return node.owner == player or not_attacking_neighbor_attack(data)

    return {
        POISON_CODE: not_attacking_neighbor_attack
        if attack_type == "neighbor"
        else opposing_structure_ranged_attack,
        NUKE_CODE: not_attacking_neighbor_or_owner_attack
        if attack_type == "neighbor"
        else structure_ranged_default_attack,
        ZOMBIE_CODE: not_attacking_neighbor_or_owner_attack
        if attack_type == "neighbor"
        else structure_ranged_default_attack,
    }


def validators_needing_player(player):
    def capital_logic(data):
        node = data[0]
        if node.owner == player and node.state_name == "default" and node.full():
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
        return my_default_node(data) and node.accessible

    # Can be used for buffed cannon, not requiring port placement. Harder to attack for bridge players
    def my_default_node(data):
        node = data[0]
        return my_node(data) and node.state_name == "default"

    # effectively a neighbor attack, but by clicking the shared edge
    # slightly weaker, must be pointed away
    def attacking_edge(data):
        edge = data[0]
        return my_node([edge.from_node]) and standard_node_attack(
            [edge.to_node], player
        )

    def dynamic_edge_own_from_node(data):
        edge = data[0]
        return edge.dynamic and (edge.from_node.owner == player)

    def dynamic_edge_own_either_but_not_flowing(data):
        edge = data[0]
        return edge.dynamic and (
            (edge.from_node.owner == player)
            or (edge.to_node.owner == player and not edge.flowing)
        )

    def dynamic_edge_own_either(data):
        edge = data[0]
        return edge.dynamic and (
            edge.from_node.owner == player or edge.to_node.owner == player
        )

    structure_validators = {
        CAPITAL_CODE: capital_logic,
        CANNON_CODE: my_default_port_node,
        PUMP_CODE: my_default_node,
    }

    def wormhole_validator(data):
        name_to_code = {
            "capital": CAPITAL_CODE,
            "cannon": CANNON_CODE,
            "pump": PUMP_CODE,
        }
        source_node, target_node = data
        if source_node.state_name in STRUCTURE_RANGES:
            validator_func = structure_validators[name_to_code[source_node.state_name]]
            if validator_func:
                return validator_func([target_node])  # Pass target_node as a list
        return False

    return {
        FREEZE_CODE: dynamic_edge_own_either_but_not_flowing,
        WORMHOLE_CODE: wormhole_validator,
    } | structure_validators


def no_crossovers(check_new_edge, data, player):
    first_node, second_node = data[0], data[1]
    return (
        first_node.owner == player
        and first_node.id != second_node.id
        and check_new_edge(first_node.id, second_node.id)
    )


def make_cannon_shot_check(check_new_edge, id_dict):
    def cannon_shot_check(player, data):
        cannon, target = id_dict[data[0]], id_dict[data[1]]
        can_shoot = cannon.state_name == "cannon" and cannon.owner == player
        can_accept = cannon.value > MINIMUM_TRANSFER_VALUE and (
            target.owner != player or not target.full()
        )
        return (
            can_shoot
            and can_accept
            and no_crossovers(
                check_new_edge, [id_dict[data[0]], id_dict[data[1]]], player
            )
        )

    return cannon_shot_check


def make_pump_drain_check(id_dict):
    def pump_drain(player, data):
        node = id_dict[data[0]]
        return node.state_name == "pump" and node.owner == player and node.full()

    return pump_drain


def valid_ability_for_credits(player, data):
    ability_code = data[0]
    return (
        ability_code in player.abilities
        and BREAKDOWNS[ability_code].credits <= player.credits
    )


def make_new_edge_ports(check_new_edge, player, from_port_needed):
    def new_edge_ports(data):
        if all([node.accessible for node in data]):
            return no_crossovers(check_new_edge, data, player)
        return False

    def defense_bridge(data):
        return data[1].owner == data[0].owner and (
            data[1].accessible or data[0].accessible
        )

    def only_to_node_port(data):
        return (defense_bridge(data) or data[1].accessible) and no_crossovers(
            check_new_edge, data, player
        )

    # Check if the nodes are within the range of a mini bridge
    def check_mini_bridge_range(data):
        first_node, second_node = data
        distance = dist(first_node.pos, second_node.pos)
        return distance <= MINI_BRIDGE_RANGE

    def mini_bridge_validator(data):
        return check_mini_bridge_range(data) and new_edge_ports(data)

    to_node_dict = {False: only_to_node_port, True: new_edge_ports}

    return {
        BRIDGE_CODE: to_node_dict[from_port_needed],
        D_BRIDGE_CODE: to_node_dict[from_port_needed],
        MINI_BRIDGE_CODE: mini_bridge_validator,
    }


def make_ability_validators(board, player, settings):
    return (
        {
            SPAWN_CODE: unowned_node,
            BURN_CODE: owned_burnable_node,
            RAGE_CODE: no_click,
            OVER_GROW_CODE: no_click,
            WALL_CODE: non_walled_node,
        }
        | validators_needing_player(player)
        | make_new_edge_ports(
            board.check_new_edge, player, settings["bridge_from_port_needed"]
        )
        | attack_validators(
            board.get_player_structures, player, settings["attack_type"]
        )
    )

def standard_click_validators(board):

    def left_click(player, data):
        try:
            return board.id_dict[data[0]].valid_left_click(player)
        except KeyError:
            return False
        
    def right_click(player, data):
        try:
            return board.id_dict[data[0]].valid_right_click(player)
        except KeyError:
            return False


    return {
        STANDARD_LEFT_CLICK: left_click,
        STANDARD_RIGHT_CLICK: right_click,
    }


def make_effect_validators(board):
    return {
        CANNON_SHOT_CODE: make_cannon_shot_check(board.check_new_edge, board.id_dict),
        PUMP_DRAIN_CODE: make_pump_drain_check(board.id_dict),
        CREDIT_USAGE_CODE: valid_ability_for_credits,
    } | standard_click_validators(board)
