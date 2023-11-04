from ability import *
from constants import *

def create_money_abilities(board):
    return {
        SPAWN_CODE: Spawn(SPAWN_COST),
        BRIDGE_CODE: Bridge(BRIDGE_COST, board.new_edge_id, board.check_new_edge, board.buy_new_edge),
        NUKE_CODE: Nuke(NUKE_COST, board.remove_node),
        POISON_CODE: Poison(POISON_COST),
        FREEZE_CODE: Freeze(FREEZE_COST),
        CAPITAL_CODE: Capital(CAPITAL_COST)
    }

def create_reload_abilities(board):
    return {
        SPAWN_CODE: Spawn(SPAWN_RELOAD),
        BRIDGE_CODE: Bridge(BRIDGE_RELOAD, board.new_edge_id, board.check_new_edge, board.buy_new_edge),
        FREEZE_CODE: Freeze(FREEZE_RELOAD),
    }
