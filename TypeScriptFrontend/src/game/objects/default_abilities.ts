import {
    AbilityVisual,
    createAbilityVisual,
    createEventVisual,
    EventVisual,
} from "./immutable_visuals";
import { Colors, KeyCodes, EventCodes } from "./constants";
import { ClickType } from "./enums";

// Create instances of AbilityVisual using the factory function
const SPAWN_V = createAbilityVisual("Spawn", "circle");
const BRIDGE_V = createAbilityVisual("Bridge", "triangle", Colors.YELLOW, "A");
const D_BRIDGE_V = createAbilityVisual("D-Bridge", "circle", Colors.YELLOW);
const NUKE_V = createAbilityVisual("Nuke", "x", Colors.GREY);
const POISON_V = createAbilityVisual("Poison", "circle", Colors.PURPLE);
const FREEZE_V = createAbilityVisual("Freeze", "triangle", Colors.LIGHT_BLUE);
const CAPITAL_V = createAbilityVisual("Capital", "star", Colors.PINK);
const ZOMBIE_V = createAbilityVisual("Zombie", "square", Colors.DARK_RED);
const BURN_V = createAbilityVisual("Burn", "square", Colors.DARK_ORANGE);
const RAGE_V = createAbilityVisual("Rage", "cross", Colors.LIGHT_GREEN);
const CANNON_V = createAbilityVisual("Cannon", "cannon", Colors.GREY, "E");
const PUMP_V = createAbilityVisual("Pump", "circle", Colors.DARK_PURPLE, "U");
const MINI_BRIDGE_V = createAbilityVisual("Mini-Bridge", "circle", Colors.YELLOW, "M");
const WORMHOLE_V = createAbilityVisual("Wormhole", "circle", Colors.BLACK, "W");

// Create instances of EventVisual using the factory function
const CANNON_SHOT_V = createEventVisual("Cannon Shot", Colors.PINK);
const PUMP_DRAIN_V = createEventVisual("Pump Drain", Colors.DARK_PURPLE);
const STANDARD_LEFT_CLICK_V = createEventVisual("Switch", Colors.GREY);
const STANDARD_RIGHT_CLICK_V = createEventVisual("Swap", Colors.GREY);
const CREDIT_USAGE_V = createEventVisual("Credit Usage", Colors.DARK_PURPLE);

interface EventVisualParameters {
    [index: string]: EventVisual | AbilityVisual;
};

// Maps for visuals
export const VISUALS: EventVisualParameters = {
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
    [KeyCodes.PUMP_CODE]: PUMP_V,
    [KeyCodes.MINI_BRIDGE_CODE]: MINI_BRIDGE_V,
    [KeyCodes.WORMHOLE_CODE]: WORMHOLE_V,

    [EventCodes.CANNON_SHOT_CODE]: CANNON_SHOT_V,
    [EventCodes.PUMP_DRAIN_CODE]: PUMP_DRAIN_V,
    [EventCodes.STANDARD_LEFT_CLICK]: STANDARD_LEFT_CLICK_V,
    [EventCodes.STANDARD_RIGHT_CLICK]: STANDARD_RIGHT_CLICK_V,
    [EventCodes.CREDIT_USAGE_CODE]: CREDIT_USAGE_V,
};

interface ClickParameters {
    [index: string]: [number, ClickType]; // Adjust the types according to what Event constructor expects
}

// Map for click behaviors
export const CLICKS: ClickParameters = {
    [KeyCodes.SPAWN_CODE]: [1, ClickType.NODE],
    [KeyCodes.BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.D_BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.MINI_BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.NUKE_CODE]: [1, ClickType.NODE],
    [KeyCodes.POISON_CODE]: [1, ClickType.EDGE],
    [KeyCodes.FREEZE_CODE]: [1, ClickType.EDGE],
    [KeyCodes.CAPITAL_CODE]: [1, ClickType.NODE],
    [KeyCodes.ZOMBIE_CODE]: [1, ClickType.NODE],
    [KeyCodes.BURN_CODE]: [1, ClickType.NODE],
    [KeyCodes.RAGE_CODE]: [0, ClickType.BLANK],
    [KeyCodes.CANNON_CODE]: [1, ClickType.NODE],
    [KeyCodes.PUMP_CODE]: [1, ClickType.NODE],
    [KeyCodes.WORMHOLE_CODE]: [1, ClickType.NODE],
};

interface EventParameters {
    [index: string]: [number, ClickType]; // Adjust the types according to what Event constructor expects
}

export const EVENTS: EventParameters = {
    [EventCodes.CANNON_SHOT_CODE]: [2, ClickType.NODE],
    [EventCodes.PUMP_DRAIN_CODE]: [1, ClickType.NODE],
    [EventCodes.STANDARD_LEFT_CLICK]: [1, ClickType.EDGE],
    [EventCodes.STANDARD_RIGHT_CLICK]: [1, ClickType.EDGE],
    [EventCodes.CREDIT_USAGE_CODE]: [1, ClickType.ABILITY],
};
