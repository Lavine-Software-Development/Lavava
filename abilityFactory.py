from ability import *
from constants import *

class AbilityFactory:

    def __init__(self, player, board):
        self.abilities = {}
        
        spawn = Spawn(player)
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(player, board.new_edge_id, board.check_new_edge, board.buy_new_edge)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(player, board.remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison(player)
        self.abilities[POISON_CODE] = poison

        freeze = Freeze(player)
        self.abilities[FREEZE_CODE] = freeze

        capital = Capital(player)
        self.abilities[CAPITAL_CODE] = capital