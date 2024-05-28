import { createAbilityVisual, createEventVisual } from './immutable_visuals';
import { Colors, KeyCodes} from './constants';
import { ClickType } from './enums';

// Create instances of AbilityVisual using the factory function
const SPAWN_V = createAbilityVisual("Spawn", "circle", Colors.YELLOW);
const BRIDGE_V = createAbilityVisual("Bridge", "triangle", Colors.YELLOW, 'A');
const D_BRIDGE_V = createAbilityVisual("D-Bridge", "circle", Colors.YELLOW);
const NUKE_V = createAbilityVisual("Nuke", "x", Colors.BLACK);
const POISON_V = createAbilityVisual("Poison", "circle", Colors.PURPLE);
const FREEZE_V = createAbilityVisual("Freeze", "triangle", Colors.LIGHT_BLUE);
const CAPITAL_V = createAbilityVisual("Capital", "star", Colors.PINK);
const ZOMBIE_V = createAbilityVisual("Zombie", "square", Colors.BLACK);
const BURN_V = createAbilityVisual("Burn", "square", Colors.DARK_ORANGE);
const RAGE_V = createAbilityVisual("Rage", "cross", Colors.GREEN);
const CANNON_V = createAbilityVisual("Cannon", "cannon", Colors.GREY, 'E');

// Create instances of EventVisual using the factory function
const CANNON_SHOT_V = createEventVisual("Cannon Shot", Colors.DARK_PINK);
const STANDARD_LEFT_CLICK_V = createEventVisual("Switch", Colors.GREY);
const STANDARD_RIGHT_CLICK_V = createEventVisual("Swap", Colors.GREY);

// Maps for visuals
export const VISUALS = {
    [KeyCodes.SPAWN_CODE]: SPAWN_V,
    [KeyCodes.BRIDGE_CODE]: BRIDGE_V,
    [KeyCodes.D_BRIDGE_CODE]: D_BRIDGE_V,
    [KeyCodes.NUKE_CODE]: NUKE_V,
    [KeyCodes.POISON_CODE]: POISON_V,
    [KeyCodes.FREEZE_CODE]: FREEZE_V,
    [KeyCodes.CAPITAL_CODE]: CAPITAL_V,
    [KeyCodes.ZOMBIE_CODE]: ZOMBIE_V,
    [KeyCodes.BURN_CODE]: BURN_V,
    [KeyCodes.RAGE_CODE]: RAGE_V,
    [KeyCodes.CANNON_CODE]: CANNON_V,

    [KeyCodes.CANNON_SHOT_CODE]: CANNON_SHOT_V,
    [KeyCodes.STANDARD_LEFT_CLICK]: STANDARD_LEFT_CLICK_V,
    [KeyCodes.STANDARD_RIGHT_CLICK]: STANDARD_RIGHT_CLICK_V
};

// Map for click behaviors
const CLICKS = {
    [KeyCodes.SPAWN_CODE]: [1, ClickType.NODE],
    [KeyCodes.BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.D_BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.NUKE_CODE]: [1, ClickType.NODE],
    [KeyCodes.POISON_CODE]: [1, ClickType.NODE],
    [KeyCodes.FREEZE_CODE]: [1, ClickType.EDGE],
    [KeyCodes.CAPITAL_CODE]: [1, ClickType.NODE],
    [KeyCodes.ZOMBIE_CODE]: [1, ClickType.NODE],
    [KeyCodes.BURN_CODE]: [1, ClickType.NODE],
    [KeyCodes.RAGE_CODE]: [0, ClickType.BLANK],
    [KeyCodes.CANNON_CODE]: [2, ClickType.NODE],
};

const EVENTS = {
    [KeyCodes.CANNON_SHOT_CODE]: [2, ClickType.NODE],
    [KeyCodes.STANDARD_LEFT_CLICK]: [1, ClickType.EDGE],
    [KeyCodes.STANDARD_RIGHT_CLICK]: [1, ClickType.EDGE]
};