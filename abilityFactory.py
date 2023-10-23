from ability import *
from constants import *

def create_abilities(board):
    return {
        SPAWN_CODE: Spawn(),
        BRIDGE_CODE: Bridge(board.new_edge_id, board.check_new_edge, board.buy_new_edge),
        NUKE_CODE: Nuke(board.remove_node),
        POISON_CODE: Poison(),
        FREEZE_CODE: Freeze(),
        CAPITAL_CODE: Capital()
    }
