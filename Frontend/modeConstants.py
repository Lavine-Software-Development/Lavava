from abilityManager import MoneyAbilityManager, ReloadAbilityManager
from Server.map_builder_helpers import starter_capitals, starter_default_nodes, starter_mines, starter_port_nodes
from player import DefaultPlayer, MoneyPlayer
from Server.constants import ALL_ABILITIES, BREAKDOWNS, BURN_CODE

def reload_abilities():
    return {x for x in ALL_ABILITIES if BREAKDOWNS[x].reload}
 
m1_ability_options = ALL_ABILITIES - {BURN_CODE}
m2_ability_options = reload_abilities()

class MKD(dict): # Multi Key Dictionary
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            for k in key:
                super().__setitem__(k, value)
        else:
            super().__setitem__(key, value)

    def __init__(self, *args):
        for key, value in args:
            self.__setitem__(key, value)

MODE_PLAYERS = MKD(((1, 3), MoneyPlayer), ((2), DefaultPlayer))
MODE_ABILITY_MANAGERS = MKD(((1, 3), MoneyAbilityManager), (2, ReloadAbilityManager))
STARTING_NODES = MKD(((1), starter_default_nodes), ((2, 3), starter_port_nodes))
STARTING_NODES_STATES = MKD(((1, 3), starter_mines), ((2), starter_capitals))
ABILITY_DISPLAYS = MKD(((1, 3), "costs"), ((2), "total"))
ABILITY_OPTIONS = MKD((1, m1_ability_options), (2, m2_ability_options), (3, ALL_ABILITIES))
ABILITY_COUNT = MKD(((1, 2, 3), 4))
DEFAULT_SPAWN = MKD(((1), True), ((2, 3), False))
