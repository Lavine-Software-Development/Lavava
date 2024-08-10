from math import dist
from constants import (
    BREAKDOWNS,
    BRIDGE_CODE,
    CANNON_CODE,
    CANNON_SHOT_CODE,
    CANNON_SHOT_DAMAGE_PERCENTAGE,
    CANNON_SHOT_SHRINK_RANGE_CUTOFF,
    CREDIT_USAGE_CODE,
    D_BRIDGE_CODE,
    POISON_TICKS,
    ZOMBIE_TICKS,
    ZOMBIE_FULL_SIZE,
    PUMP_DRAIN_CODE,
    SPAWN_CODE,
    FREEZE_CODE,
    NUKE_CODE,
    BURN_CODE,
    POISON_CODE,
    CAPITAL_CODE,
    RAGE_CODE,
    STANDARD_LEFT_CLICK,
    STANDARD_RIGHT_CLICK,
    ZOMBIE_CODE,
    EDGE,
    DYNAMIC_EDGE,
    PUMP_CODE,
    MINIMUM_TRANSFER_VALUE,
    MINI_BRIDGE_CODE,
    OVER_GROW_CODE,
    WALL_CODE,
    WORMHOLE_CODE,
)

def make_wormhole_effect(data, player):
    structure_effects = {
        "capital": capital_effect,
        "cannon": cannon_effect,
        "pump": pump_effect,
    }
    source_node, target_node = data
    structure = source_node.state_name
    structure_effects[structure]([target_node], player)
    source_node.set_state("default")   

def make_bridge(buy_new_edge, bridge_type, destroy_ports=False, only_to_node_port=False):
    def bridge_effect(data, player):
        id1, id2 = data
        buy_new_edge(id1, id2, bridge_type, only_to_node_port, destroy_ports)

    return bridge_effect

def make_nuke(remove_node):
    def nuke_effect(data, player):
        node = data[0]
        remove_node(node)
        if node.owner and node.owner.count == 0:
            node.owner.killed_event(player)

    return nuke_effect

def make_board_wide_effect(board_wide_effect):
    def rage_effect(data, player):
        board_wide_effect('rage', player)

    def over_grow_effect(data, player):
        board_wide_effect('over_grow', player)

    return {
        RAGE_CODE: rage_effect,
        OVER_GROW_CODE: over_grow_effect
    }

def make_rage(board_wide_effect):
    def rage_effect(data, player):
        board_wide_effect('rage', player)
    return rage_effect

def make_cannon_shot(id_dict, update_method):
    def constant_cannon_shot(player, data):
        cannon, target = id_dict[data[0]], id_dict[data[1]]
        if target.owner == player:
            loss = min(cannon.value - MINIMUM_TRANSFER_VALUE, (target.full_size - target.value) * (1 / CANNON_SHOT_DAMAGE_PERCENTAGE))
        else:
            loss = cannon.value - MINIMUM_TRANSFER_VALUE
        transfer = loss * CANNON_SHOT_DAMAGE_PERCENTAGE
        cannon.value -= loss
        target.delivery(transfer, player)
        update_method(("cannon_shot", (data[0], data[1], transfer)))

    def decreasing_cannon_shot(player, data):
        cannon, target = id_dict[data[0]], id_dict[data[1]]

        cannon_send = cannon.value - MINIMUM_TRANSFER_VALUE

        distance = dist(cannon.pos, target.pos)
        guaranteed_remaining_delivery = CANNON_SHOT_DAMAGE_PERCENTAGE * cannon_send
        delivery_distance_loss_percentage = 1 - min(distance / CANNON_SHOT_SHRINK_RANGE_CUTOFF, 1)
        leftover_shrink_delivery = delivery_distance_loss_percentage * (cannon_send - guaranteed_remaining_delivery)
        max_delivery = guaranteed_remaining_delivery + leftover_shrink_delivery

        if target.owner == cannon.owner and target.value + max_delivery > target.full_size:
            send_to_delivery_ratio = cannon_send / max_delivery # delivery * ratio = send
            max_delivery = target.full_size - target.value 
            cannon_send = send_to_delivery_ratio * max_delivery

        cannon.value -= cannon_send
        target.delivery(max_delivery, player)
        update_method(("cannon_shot", (data[0], data[1], cannon_send, max_delivery)))

    return decreasing_cannon_shot

def make_pump_drain(id_dict):
    def pump_drain(player, data):
        pump_node = id_dict[data[0]]
        player.credits += 2
        pump_node.state.draining = True
        
    return pump_drain

def credit_usage_effect(player, data):
    ability_code = data[0]
    player.credits -= BREAKDOWNS[ability_code].credits
    player.abilities[ability_code].remaining += 1

def freeze_effect(data, player):
    edge = data[0] 
    if edge.from_node.owner != player:
        edge.natural_swap()
    edge.dynamic = False

def spawn_effect(data, player):
    node = data[0]
    node.capture(player)

def zombie_effect(data, player):
    node = data[0]
    if node.owner != player:
        node.owner.count -= 1
        node.owner = player
        node.value = max(ZOMBIE_FULL_SIZE - node.value, 10)
        # nodes captured by zombie do not go to the player and thus count is by default reduced
        player.count += 1 # so we add 1 to counteract this the first time
    else:
        node.value = ZOMBIE_FULL_SIZE

    node.set_state("zombie", ZOMBIE_TICKS)

def poison_effect(data, player):
    node = data[0]
    node.set_state("poison", (player, POISON_TICKS))

# weak burn, only gets one node
def burn_effect(data, player):
    node = data[0]
    node.is_port = False

# medium burn, gets all interrupted paths of ports *IF FLOWING*
def burn_setting_effect(data, player):
    node = data[0]
    node.set_state("burn")

# strongest burn, gets all interrupted paths of ports
def spreading_burn_effect(data, player):
    node = data[0]
    node.is_port = False
    for edge in node.outgoing:
        if edge.to_node.is_port:
            spreading_burn_effect((edge.to_node), player)

def capital_effect(data, player):
    node = data[0]
    node.set_state("capital")

def cannon_effect(data, player):
    node = data[0]
    node.set_state("cannon")

def pump_effect(data, player):
    node = data[0]
    node.set_state("pump")

def wall_effect(data, player):
    node = data[0]
    node.wall_count = 1

def make_ability_effects(board, settings):
    return {
        BRIDGE_CODE: make_bridge(board.buy_new_edge, EDGE, settings["bridge_burn"], settings["bridge_from_port_needed"]),
        D_BRIDGE_CODE: make_bridge(board.buy_new_edge, DYNAMIC_EDGE, settings["bridge_burn"], settings["bridge_from_port_needed"]),
        MINI_BRIDGE_CODE : make_bridge(board.buy_new_edge, DYNAMIC_EDGE, settings["bridge_burn"]),
        SPAWN_CODE: spawn_effect,
        FREEZE_CODE: freeze_effect,
        NUKE_CODE: make_nuke(board.remove_node),
        BURN_CODE: burn_setting_effect,
        POISON_CODE: poison_effect,
        CAPITAL_CODE: capital_effect,
        ZOMBIE_CODE: zombie_effect,
        CANNON_CODE: cannon_effect,
        PUMP_CODE: pump_effect,
        WORMHOLE_CODE: make_wormhole_effect,
        WALL_CODE: wall_effect
    } | make_board_wide_effect(board.board_wide_effect)


def make_event_effects(board, update_method):
    return {
        CANNON_SHOT_CODE: make_cannon_shot(board.id_dict, update_method),
        PUMP_DRAIN_CODE : make_pump_drain(board.id_dict),
        STANDARD_LEFT_CLICK: lambda player, data: board.id_dict[data[0]].manual_switch(),
        STANDARD_RIGHT_CLICK : lambda player, data: board.id_dict[data[0]].click_swap(),
        CREDIT_USAGE_CODE: credit_usage_effect
    }



