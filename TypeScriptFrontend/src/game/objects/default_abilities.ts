import {
    AbilityVisual,
    createAbilityVisual,
    createEventVisual,
    EventVisual,
} from "./immutable_visuals";
import { Colors, KeyCodes, EventCodes } from "./constants";
import { ClickType } from "./enums";

// Create instances of AbilityVisual using the factory function
const SPAWN_V = createAbilityVisual("Spawn", "an unclaimed dot");
const BRIDGE_V = createAbilityVisual("Bridge", "to a non-walled dot. It also cannot cross other bridges", Colors.YELLOW, "A");
const D_BRIDGE_V = createAbilityVisual("D-Bridge", "to a non-walled dot. It also cannot cross other bridges", Colors.YELLOW);
const NUKE_V = createAbilityVisual("Nuke", "a neighboring dot (So long as it is not currently attacking you)", Colors.GREY);
const POISON_V = createAbilityVisual("Poison", "a neighboring dot (So long as it is not currently attacking you)", Colors.PURPLE);
const FREEZE_V = createAbilityVisual("Freeze", "a two-way bridge", Colors.LIGHT_BLUE);
const CAPITAL_V = createAbilityVisual("Capital", "a full dot you own (So long as it is not beside another capital)", Colors.PINK);
const ZOMBIE_V = createAbilityVisual("Zombie", "a neighboring dot (So long as it is not currently attacking you)", Colors.DARK_GRAY);
const BURN_V = createAbilityVisual("Burn", "a dot with ports", Colors.DARK_ORANGE);
const RAGE_V = createAbilityVisual("Rage", "", Colors.DARK_RED);
const CANNON_V = createAbilityVisual("Cannon", "a dot you own", Colors.GREY, "E");
const PUMP_V = createAbilityVisual("Pump", "a dot you own", Colors.DARK_PURPLE, "U");
const MINI_BRIDGE_V = createAbilityVisual("Mini-Bridge", "to a non-walled dot. It also cannot cross other bridges", Colors.YELLOW, "M");
const OVER_GROW_V = createAbilityVisual("Over-Grow", "", Colors.DARK_GREEN);
const WALL_V = createAbilityVisual("Wall", "a non-walled dot", Colors.LIGHT_BROWN, "V");
const WORMHOLE_V = createAbilityVisual("Wormhole", "a structured dot, to an unstructured dot",Colors.DARK_PINK, "W");

// Create instances of EventVisual using the factory function
const CANNON_SHOT_V = createEventVisual("Cannon Shot", "Shot cannot cross other bridges", Colors.PINK);
const PUMP_DRAIN_V = createEventVisual("Pump Drain", "", Colors.DARK_PURPLE);
const STANDARD_LEFT_CLICK_V = createEventVisual("Switch", "Can only switch bridges extending OUTWARDS from a dot you OWN", Colors.GREY);
const STANDARD_RIGHT_CLICK_V = createEventVisual("Swap", "Can only swap two-way (dotted) bridges that you own BOTH sides of", Colors.GREY);
const CREDIT_USAGE_V = createEventVisual("Credit Usage", "", Colors.DARK_PURPLE);
const NODE_LEFT_CLICK_V = createEventVisual("Node Left Click", "Only click your own dots or their neighbors, (Unless using abilities)");
const NODE_RIGHT_CLICK_V = createEventVisual("Node Right Click", "", Colors.GREY);

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
    [KeyCodes.OVER_GROW_CODE]: OVER_GROW_V,
    [KeyCodes.WALL_CODE]: WALL_V,
    [KeyCodes.WORMHOLE_CODE]: WORMHOLE_V,

    [EventCodes.CANNON_SHOT_CODE]: CANNON_SHOT_V,
    [EventCodes.PUMP_DRAIN_CODE]: PUMP_DRAIN_V,
    [EventCodes.STANDARD_LEFT_CLICK]: STANDARD_LEFT_CLICK_V,
    [EventCodes.STANDARD_RIGHT_CLICK]: STANDARD_RIGHT_CLICK_V,
    [EventCodes.CREDIT_USAGE_CODE]: CREDIT_USAGE_V,
    [EventCodes.NODE_LEFT_CLICK]: NODE_LEFT_CLICK_V,
    [EventCodes.NODE_RIGHT_CLICK]: NODE_RIGHT_CLICK_V,
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
    [KeyCodes.POISON_CODE]: [1, ClickType.NODE],
    [KeyCodes.FREEZE_CODE]: [1, ClickType.EDGE],
    [KeyCodes.CAPITAL_CODE]: [1, ClickType.NODE],
    [KeyCodes.ZOMBIE_CODE]: [1, ClickType.NODE],
    [KeyCodes.BURN_CODE]: [1, ClickType.NODE],
    [KeyCodes.RAGE_CODE]: [0, ClickType.BLANK],
    [KeyCodes.CANNON_CODE]: [1, ClickType.NODE],
    [KeyCodes.PUMP_CODE]: [1, ClickType.NODE],
    [KeyCodes.OVER_GROW_CODE]: [0, ClickType.BLANK],
    [KeyCodes.WALL_CODE]: [1, ClickType.NODE],
    [KeyCodes.WORMHOLE_CODE]: [2, ClickType.NODE],
};

interface EventParameters {
    [index: string]: [number, ClickType, Set<number>?]; // Make the Set optional
}

export const EVENTS: EventParameters = {
    [EventCodes.CANNON_SHOT_CODE]: [2, ClickType.NODE, new Set([KeyCodes.POISON_CODE, KeyCodes.NUKE_CODE, KeyCodes.ZOMBIE_CODE])],
    [EventCodes.PUMP_DRAIN_CODE]: [1, ClickType.NODE, new Set()],
    [EventCodes.STANDARD_LEFT_CLICK]: [1, ClickType.EDGE, new Set()],
    [EventCodes.STANDARD_RIGHT_CLICK]: [1, ClickType.EDGE, new Set()],
    [EventCodes.CREDIT_USAGE_CODE]: [1, ClickType.ABILITY, new Set()],
    [EventCodes.NODE_LEFT_CLICK]: [1, ClickType.NODE, new Set()],
    [EventCodes.NODE_RIGHT_CLICK]: [1, ClickType.NODE, new Set()],
};
