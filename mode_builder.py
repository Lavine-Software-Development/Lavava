from constants import MODE, CONTEXT, MODE_ABILITY_OPTIONS
from nodeState import CapitalState, StartingCapitalState
from player import MoneyPlayer, DefaultPlayer
from helpers import starter_capitals, starter_mines, starter_port_nodes, starter_nodes
from abilityManager import MoneyAbilityManager, ReloadAbilityManager


def set_mode(mode_num):
    if mode_num == 1:
        set_mode_1()
    elif mode_num == 2:
        set_mode_2()
    elif mode_num == 3:
        set_mode_1()
        MODE["node_function"] = starter_port_nodes

    CONTEXT["mode"] = mode_num
    CONTEXT["all_ability_codes"] = MODE_ABILITY_OPTIONS[CONTEXT["mode"]]


def set_mode_1():
    MODE["player"] = MoneyPlayer
    MODE["manager"] = MoneyAbilityManager
    MODE["capital"] = CapitalState
    MODE["setup"] = starter_mines
    MODE["node_function"] = starter_nodes
    MODE["ability_display"] = "costs"


def set_mode_2():
    MODE["player"] = DefaultPlayer
    MODE["manager"] = ReloadAbilityManager
    MODE["capital"] = StartingCapitalState
    MODE["setup"] = starter_capitals
    MODE["node_function"] = starter_nodes
    MODE["ability_display"] = "total"
