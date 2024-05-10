from drawClasses import AbilityVisual, EventVisual
from constants import DARK_PINK, YELLOW, BLACK, PURPLE, LIGHT_BLUE, PINK, DARK_ORANGE, GREEN, RAGE_CODE, BURN_CODE, \
    ZOMBIE_CODE, CAPITAL_CODE, FREEZE_CODE, POISON_CODE, NUKE_CODE, D_BRIDGE_CODE, BRIDGE_CODE, SPAWN_CODE, \
          GREY, CANNON_CODE, CANNON_SHOT_CODE
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
CANNON_V = AbilityVisual("Cannon", "cannon", GREY)

CANNON_SHOT_V = EventVisual("Cannon Shot", DARK_PINK)

SPAWN_C = {1, ClickType.NODE}
BRIDGE_C = {2, ClickType.NODE}
D_BRIDGE_C = {2, ClickType.NODE}
NUKE_C = {1, ClickType.NODE}
POISON_C = {1, ClickType.NODE}
FREEZE_C = {1, ClickType.EDGE}
CAPITAL_C = {1, ClickType.NODE}
ZOMBIE_C = {1, ClickType.NODE}
BURN_C = {1, ClickType.NODE}
RAGE_C = {0, ClickType.BLANK}
CANNON_C = {2, ClickType.NODE}

CANNON_SHOT_C = {2, ClickType.NODE}

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

    CANNON_SHOT_CODE: DARK_PINK
}

CLICKS = {
    SPAWN_CODE: SPAWN_C,
    BRIDGE_CODE: BRIDGE_C,
    D_BRIDGE_CODE: D_BRIDGE_C,
    NUKE_CODE: NUKE_C,
    POISON_CODE: POISON_C,
    FREEZE_CODE: FREEZE_C,
    CAPITAL_CODE: CAPITAL_C,
    ZOMBIE_CODE: ZOMBIE_C,
    BURN_CODE: BURN_C,
    RAGE_CODE: RAGE_C,
    CANNON_CODE: CANNON_C,
}

EVENTS = {
    CANNON_SHOT_CODE: CANNON_SHOT_C
}