from constants import (
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    GROWTH_STOP,
    MINIMUM_TRANSFER_VALUE,
    SPAWN_CODE,
    FREEZE_CODE,
    NUKE_CODE,
    BURN_CODE,
    POISON_CODE,
    CAPITAL_CODE,
    RAGE_CODE,
    ZOMBIE_CODE,
    EDGE,
    DYNAMIC_EDGE,
    ZOMBIE_FULL_SIZE,
)
from playerEffect import PlayerEnraged

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


def make_rage(rage):
    def rage_effect(data, player):
        rage(player, 'rage')
        player.effects.add(PlayerEnraged())
    return rage_effect


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
    node = data[0]
    node.set_state("poison")

def burn_effect(data, player):
    node = data[0]
    node.is_port = False

def capital_effect(data, player):
    node = data[0]
    node.set_state("capital")

def cannon_effect(data, player):
    node = data[0]
    node.set_state("cannon")

def cannon_shot_effect(data, player):
    cannon, target = data[0], data[1]
    if target.owner == player:
        transfer = min(cannon.value - MINIMUM_TRANSFER_VALUE, GROWTH_STOP - target.value)
    else:
        transfer = cannon.value - MINIMUM_TRANSFER_VALUE
    cannon.value -= transfer
    target.delivery(transfer, player)

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
    }


