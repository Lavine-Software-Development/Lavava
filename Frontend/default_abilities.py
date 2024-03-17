from drawClasses import AbilityVisual
from constants import YELLOW, BLACK, PURPLE, LIGHT_BLUE, PINK, DARK_ORANGE, GREEN, RAGE_CODE, BURN_CODE, \
    ZOMBIE_CODE, CAPITAL_CODE, FREEZE_CODE, POISON_CODE, NUKE_CODE, D_BRIDGE_CODE, BRIDGE_CODE, SPAWN_CODE

SPAWN = AbilityVisual("Spawn", "circle", (None,))
BRIDGE = AbilityVisual("Bridge", "triangle", YELLOW)
D_BRIDGE = AbilityVisual("D-Bridge", "circle", YELLOW)
NUKE = AbilityVisual("Nuke", "x", BLACK)
POISON = AbilityVisual("Poison", "circle", PURPLE)
FREEZE = AbilityVisual("Freeze", "triangle", LIGHT_BLUE)
CAPITAL = AbilityVisual("Capital", "star", PINK)
ZOMBIE = AbilityVisual("Zombie", "square", BLACK)
BURN = AbilityVisual("Burn", "square", DARK_ORANGE)
RAGE = AbilityVisual("Rage", "cross", GREEN)

VISUALS = {
    SPAWN_CODE: SPAWN,
    BRIDGE_CODE: BRIDGE,
    D_BRIDGE_CODE: D_BRIDGE,
    NUKE_CODE: NUKE,
    POISON_CODE: POISON,
    FREEZE_CODE: FREEZE,
    CAPITAL_CODE: CAPITAL,
    ZOMBIE_CODE: ZOMBIE,
    BURN_CODE: BURN,
    RAGE_CODE: RAGE
}