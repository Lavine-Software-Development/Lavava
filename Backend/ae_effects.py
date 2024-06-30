from constants import (
    BREAKDOWNS,
    BRIDGE_CODE,
    CANNON_CODE,
    CANNON_SHOT_CODE,
    D_BRIDGE_CODE,
    POISON_TICKS,
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
    ZOMBIE_FULL_SIZE,
    PUMP_CODE,
    MINIMUM_TRANSFER_VALUE,
    GROWTH_STOP,
    NODE_MINIMUM_VALUE,
)

def make_bridge(buy_new_edge, bridge_type):
    def bridge_effect(data, player):
        id1, id2 = data
        buy_new_edge(id1, id2, bridge_type)

    return bridge_effect


def make_nuke(remove_node):
    def nuke_effect(data, player):
        node = data[0]
        remove_node(node)

    return nuke_effect


def make_rage(board_wide_effect):
    def rage_effect(data, player):
        board_wide_effect('rage', player)
    return rage_effect

def make_cannon_shot(id_dict):
    def cannon_shot(player, data):
        cannon, target = id_dict[data[0]], id_dict[data[1]]
        if target.owner == player:
            transfer = min(cannon.value - MINIMUM_TRANSFER_VALUE, GROWTH_STOP - target.value)
        else:
            transfer = cannon.value - MINIMUM_TRANSFER_VALUE
        cannon.value -= transfer
        target.delivery(transfer, player)

    return cannon_shot

def make_pump_drain(id_dict):
    def pump_drain(player, data):
        pump_node = id_dict[data[0]]
        ability_code = data[1]
        player.abilities[ability_code].remaining += 3 - BREAKDOWNS[ability_code].credits
        pump_node.state.draining = True
        
    return pump_drain

def freeze_effect(data, player):
    edge = data[0]
    edge.dynamic = False

def spawn_effect(data, player):
    node = data[0]
    node.capture(player)

def zombie_effect(data, player):
    node = data[0]
    node.capture(None)
    node.set_state("zombie")
    node.value = ZOMBIE_FULL_SIZE

def poison_effect(data, player):
    edge = data[0]
    edge.to_node.set_state("poison", (player, POISON_TICKS))

def burn_effect(data, player):
    node = data[0]
    node.is_port = False

def capital_effect(data, player):
    node = data[0]
    node.set_state("capital")

def cannon_effect(data, player):
    node = data[0]
    node.set_state("cannon")

def pump_effect(data, player):
    node = data[0]
    node.set_state("pump")

def make_ability_effects(board):
    return {
        BRIDGE_CODE: make_bridge(board.buy_new_edge, EDGE),
        D_BRIDGE_CODE: make_bridge(board.buy_new_edge, DYNAMIC_EDGE),
        SPAWN_CODE: spawn_effect,
        FREEZE_CODE: freeze_effect,
        NUKE_CODE: make_nuke(board.remove_node),
        BURN_CODE: burn_effect,
        POISON_CODE: poison_effect,
        CAPITAL_CODE: capital_effect,
        ZOMBIE_CODE: zombie_effect,
        RAGE_CODE: make_rage(board.board_wide_effect),
        CANNON_CODE: cannon_effect,
        PUMP_CODE: pump_effect,
    }


def make_event_effects(board):
    return {
        CANNON_SHOT_CODE: make_cannon_shot(board.id_dict),
        PUMP_DRAIN_CODE : make_pump_drain(board.id_dict),
        STANDARD_LEFT_CLICK: lambda player, data: board.id_dict[data[0]].switch(),
        STANDARD_RIGHT_CLICK : lambda player, data: board.id_dict[data[0]].click_swap(),
    }



