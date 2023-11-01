from constants import MODE
from nodeState import CapitalState, StartingCapitalState
from player import MoneyPlayer, DefaultPlayer
from helpers import starter_capitals, starter_mines
from abilityManager import MoneyAbilityManager, ReloadAbilityManager

def set_mode(mode_num,):
    if mode_num == 0:
        MODE['player'] = MoneyPlayer
        MODE['manager'] = MoneyAbilityManager
        MODE['capital'] = CapitalState
        MODE['setup'] = starter_mines
    elif mode_num == 1:
        MODE['player'] = DefaultPlayer
        MODE['manager'] = ReloadAbilityManager
        MODE['capital'] = StartingCapitalState
        MODE['setup'] = starter_capitals