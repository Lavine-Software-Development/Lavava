import {
    AbilityVisual,
    createAbilityVisual,
    createEventVisual,
    EventVisual,
} from "./immutable_visuals";
import { Colors, KeyCodes, EventCodes } from "./constants";
import { ClickType } from "./enums";

// Create instances of AbilityVisual using the factory function
const SPAWN_V = createAbilityVisual("Spawn", "circle", Colors.GREEN);
const BRIDGE_V = createAbilityVisual("Bridge", "triangle", Colors.YELLOW, "A");
const D_BRIDGE_V = createAbilityVisual("D-Bridge", "circle", Colors.YELLOW);
const NUKE_V = createAbilityVisual("Nuke", "x", Colors.BLACK);
const POISON_V = createAbilityVisual("Poison", "circle", Colors.PURPLE);
const FREEZE_V = createAbilityVisual("Freeze", "triangle", Colors.LIGHT_BLUE);
const CAPITAL_V = createAbilityVisual("Capital", "star", Colors.PINK);
const ZOMBIE_V = createAbilityVisual("Zombie", "square", Colors.BLACK);
const BURN_V = createAbilityVisual("Burn", "square", Colors.DARK_ORANGE);
const RAGE_V = createAbilityVisual("Rage", "cross", Colors.GREEN);
const CANNON_V = createAbilityVisual("Cannon", "cannon", Colors.GREY, "E");
const PUMP_V = createAbilityVisual("Pump", "circle", Colors.GREEN, "U");

// Create instances of EventVisual using the factory function
const CANNON_SHOT_V = createEventVisual("Cannon Shot", Colors.DARK_PINK);
const PUMP_DRAIN_V = createEventVisual("Pump Drain", Colors.YELLOW);
const STANDARD_LEFT_CLICK_V = createEventVisual("Switch", Colors.GREY);
const STANDARD_RIGHT_CLICK_V = createEventVisual("Swap", Colors.GREY);

interface EventVisualParameters {
    [index: string]: EventVisual | AbilityVisual;
}

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

    [EventCodes.CANNON_SHOT_CODE]: CANNON_SHOT_V,
    [EventCodes.PUMP_DRAIN_CODE]: PUMP_DRAIN_V,
    [EventCodes.STANDARD_LEFT_CLICK]: STANDARD_LEFT_CLICK_V,
    [EventCodes.STANDARD_RIGHT_CLICK]: STANDARD_RIGHT_CLICK_V,
};

interface ClickParameters {
    [index: string]: [number, ClickType]; // Adjust the types according to what Event constructor expects
}

// Map for click behaviors
export const CLICKS: ClickParameters = {
    [KeyCodes.SPAWN_CODE]: [1, ClickType.NODE],
    [KeyCodes.BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.D_BRIDGE_CODE]: [2, ClickType.NODE],
    [KeyCodes.NUKE_CODE]: [1, ClickType.NODE],
    [KeyCodes.POISON_CODE]: [1, ClickType.EDGE],
    [KeyCodes.FREEZE_CODE]: [1, ClickType.EDGE],
    [KeyCodes.CAPITAL_CODE]: [1, ClickType.NODE],
    [KeyCodes.ZOMBIE_CODE]: [1, ClickType.NODE],
    [KeyCodes.BURN_CODE]: [1, ClickType.NODE],
    [KeyCodes.RAGE_CODE]: [0, ClickType.BLANK],
    [KeyCodes.CANNON_CODE]: [2, ClickType.NODE],
    [KeyCodes.PUMP_CODE]: [1, ClickType.NODE],
};

interface EventParameters {
    [index: string]: [number, ClickType]; // Adjust the types according to what Event constructor expects
}

export const EVENTS: EventParameters = {
    [EventCodes.CANNON_SHOT_CODE]: [2, ClickType.NODE],
    [EventCodes.PUMP_DRAIN_CODE]: [1, ClickType.NODE],
    [EventCodes.STANDARD_LEFT_CLICK]: [1, ClickType.EDGE],
    [EventCodes.STANDARD_RIGHT_CLICK]: [1, ClickType.EDGE],
};
