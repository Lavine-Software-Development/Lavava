from ability import *
from constants import *

class AbilityFactory:

    def __init__(self, board):
        self.abilities = {}
        
        spawn = Spawn()
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(board.new_edge_id, board.check_new_edge, board.buy_new_edge)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(board.remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison()
        self.abilities[POISON_CODE] = poison

        freeze = Freeze()
        self.abilities[FREEZE_CODE] = freeze

        capital = Capital()
        self.abilities[CAPITAL_CODE] = capital