from ability import *
from constants import *

class AbilityBuilder:

    def __init__(self, player, check_new_edge, buy_new_edge, new_edge_id, remove_node):
        self.abilities = {}
        
        spawn = Spawn(player, player.color)
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(player, check_new_edge, buy_new_edge, new_edge_id)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(player, remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison(player)
        self.abilities[POISON_CODE] = poison

        freeze = Freeze(player)
        self.abilities[FREEZE_CODE] = freeze

        capital = Capital(player)
        self.abilities[CAPITAL_CODE] = capital