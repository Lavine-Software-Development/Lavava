from abilityManager import MoneyAbilityManager, ReloadAbilityManager
from map_builder_helpers import starter_capitals, starter_default_nodes, starter_mines, starter_port_nodes
from nodeState import CapitalState, StartingCapitalState
from player import DefaultPlayer, MoneyPlayer
from constants import ALL_ABILITIES, CAPITAL_CODE, BURN_CODE
 
m1_ability_options = ALL_ABILITIES - {BURN_CODE}
m2_ability_options = ALL_ABILITIES - {BURN_CODE, CAPITAL_CODE}

class MKD(dict): # Multi Key Dictionary
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            for k in key:
                super().__setitem__(k, value)
        else:
            super().__setitem__(key, value)

    def __init__(self, *args, **kwargs):
        super().__init__()
        for arg in args:
            for key, value in arg:
                self.__setitem__(key, value)
        for key, value in kwargs.items():
            self.__setitem__(key, value)

PLAYER = None
MANAGER = None
START_NODE_ALGORITHM = None
START_NODE_STATE_ALGORITHM = None
CAPITAL_TYPE = None
ABILITY_DISPLAY = None
ABILITY_OPTION = None

MODE_PLAYERS = MKD(((1, 3), MoneyPlayer), (2, DefaultPlayer))
MODE_ABILITY_MANAGERS = MKD(((1, 3), MoneyAbilityManager), (2, ReloadAbilityManager))
STARTING_NODES = MKD(((1, 2), starter_default_nodes), (3, starter_port_nodes))
STARTING_NODES_STATES = MKD(((1, 3), starter_mines), (2, starter_capitals))
CAPITAL_TYPES = MKD(((1, 3), CapitalState), (2, StartingCapitalState))
ABILITY_DISPLAYS = MKD(((1, 3), "costs"), (2, "total"))
ABILITY_OPTIONS = MKD((1, m1_ability_options), (2, m2_ability_options), (3, ALL_ABILITIES))

