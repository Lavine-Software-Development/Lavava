from drawClasses import AbilityVisual, EventVisual
from constants import DARK_PINK, STANDARD_RIGHT_CLICK, YELLOW, BLACK, PURPLE, LIGHT_BLUE, PINK, DARK_ORANGE, GREEN, RAGE_CODE, BURN_CODE, \
    ZOMBIE_CODE, CAPITAL_CODE, FREEZE_CODE, POISON_CODE, NUKE_CODE, D_BRIDGE_CODE, BRIDGE_CODE, SPAWN_CODE, \
          GREY, CANNON_CODE, CANNON_SHOT_CODE, STANDARD_LEFT_CLICK
from clickTypeEnum import ClickType


SPAWN_V = AbilityVisual("Spawn", "circle", (None,))
BRIDGE_V = AbilityVisual("Bridge", "triangle", YELLOW, 'A')
D_BRIDGE_V = AbilityVisual("D-Bridge", "circle", YELLOW)
NUKE_V = AbilityVisual("Nuke", "x", BLACK)
POISON_V = AbilityVisual("Poison", "circle", PURPLE)
FREEZE_V = AbilityVisual("Freeze", "triangle", LIGHT_BLUE)
CAPITAL_V = AbilityVisual("Capital", "star", PINK)
ZOMBIE_V = AbilityVisual("Zombie", "square", BLACK)
BURN_V = AbilityVisual("Burn", "square", DARK_ORANGE)
RAGE_V = AbilityVisual("Rage", "cross", GREEN)
CANNON_V = AbilityVisual("Cannon", "cannon", GREY, 'E')

CANNON_SHOT_V = EventVisual("Cannon Shot", DARK_PINK)
STANDARD_LEFT_CLICK_V = EventVisual("Switch", GREY)
STANDARD_RIGHT_CLICK_V = EventVisual("Swap", GREY)

VISUALS = {
    SPAWN_CODE: SPAWN_V,
    BRIDGE_CODE: BRIDGE_V,
    D_BRIDGE_CODE: D_BRIDGE_V,
    NUKE_CODE: NUKE_V,
    POISON_CODE: POISON_V,
    FREEZE_CODE: FREEZE_V,
    CAPITAL_CODE: CAPITAL_V,
    ZOMBIE_CODE: ZOMBIE_V,
    BURN_CODE: BURN_V,
    RAGE_CODE: RAGE_V,
    CANNON_CODE: CANNON_V,

    CANNON_SHOT_CODE: CANNON_SHOT_V,
    STANDARD_LEFT_CLICK: STANDARD_LEFT_CLICK_V,
    STANDARD_RIGHT_CLICK: STANDARD_RIGHT_CLICK_V
}

CLICKS = {
    SPAWN_CODE: (1, ClickType.NODE),
    BRIDGE_CODE: (2, ClickType.NODE),
    D_BRIDGE_CODE: (2, ClickType.NODE),
    NUKE_CODE: (1, ClickType.NODE),
    POISON_CODE: (1, ClickType.NODE),
    FREEZE_CODE: (1, ClickType.EDGE),
    CAPITAL_CODE: (1, ClickType.NODE),
    ZOMBIE_CODE: (1, ClickType.NODE),
    BURN_CODE: (1, ClickType.NODE),
    RAGE_CODE: (0, ClickType.BLANK),
    CANNON_CODE: (2, ClickType.NODE),
}

EVENTS = {
    CANNON_SHOT_CODE: (2, ClickType.NODE),
    STANDARD_LEFT_CLICK: (1, ClickType.EDGE),
    STANDARD_RIGHT_CLICK: (1, ClickType.EDGE)
}