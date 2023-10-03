from ability import *
from constants import *

class AbilityBuilder:

    def __init__(self, color, check_new_edge, buy_new_edge, new_edge_id, remove_node):
        self.abilities = {}
        
        spawn = Spawn(color)
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(check_new_edge, buy_new_edge, new_edge_id)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison()
        self.abilities[POISON_CODE] = poison

        freeze = Freeze()
        self.abilities[FREEZE_CODE] = freeze

        capital = Capital()
        self.abilities[CAPITAL_CODE] = capital