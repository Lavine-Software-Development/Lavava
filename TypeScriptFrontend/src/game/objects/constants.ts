export const Colors = {
    RED: [255, 0, 0] as const,
    BLUE: [0, 0, 255] as const,
    GREEN: [0, 255, 0] as const,
    ORANGE: [243, 156, 18] as const,
    BLACK: [0, 0, 0] as const,
    WHITE: [255, 255, 255] as const,
    MEDIUM_GREEN: [179, 255, 149] as const,
    LIGHT_GREEN: [209, 255, 189] as const,
    DARK_GREEN: [0, 100, 0] as const,
    DARK_ORANGE: [193, 106, 8] as const,
    STRONG_ORANGE: [255, 77, 0] as const,
    YELLOW: [255, 255, 0] as const,
    LIGHT_YELLOW: [255, 255, 153] as const,
    DARK_YELLOW: [204, 204, 0] as const,
    GREY: [128, 128, 128] as const,
    LIGHT_GREY: [192, 192, 192] as const,
    PURPLE: [153, 51, 255] as const,
    DARK_PURPLE: [102, 0, 204] as const,
    PINK: [255, 51, 153] as const,
    DARK_PINK: [255, 0, 127] as const,
    LIGHT_BLUE: [173, 216, 230] as const,
    BROWN: [150, 75, 0] as const,
    LIGHT_BROWN: [205, 133, 63] as const,
    DARK_GRAY: [64, 64, 64] as const,
    DARK_RED: [139, 0, 0] as const,
};

export const PlayerColors: {
    [key: number]: Readonly<[number, number, number]>;
} = {
    0: Colors.RED,
    1: Colors.BLUE,
    2: Colors.ORANGE,
    3: Colors.GREEN,
};

export const KeyCodes = {
    SPAWN_CODE: 115,
    FREEZE_CODE: 102,
    BRIDGE_CODE: 97,
    D_BRIDGE_CODE: 100,
    ZOMBIE_CODE: 122,
    RAGE_CODE: 114,
    BURN_CODE: 98,
    NUKE_CODE: 110,
    POISON_CODE: 112,
    CAPITAL_CODE: 99,
    CANNON_CODE: 101,
    PUMP_CODE: 117,
    MINI_BRIDGE_CODE: 109,
    WORMHOLE_CODE: 119,
    OVER_GROW_CODE: 111,
    WALL_CODE: 118,
};

export const attackCodes = [KeyCodes.NUKE_CODE, KeyCodes.POISON_CODE, KeyCodes.ZOMBIE_CODE];

export const EventCodes = {
    CANNON_SHOT_CODE: 4,
    PUMP_DRAIN_CODE: 5,
    STANDARD_LEFT_CLICK: 1,
    STANDARD_RIGHT_CLICK: 3,
    CREDIT_USAGE_CODE: 6,
};

export const stateCodes = {
    OVERRIDE_RESTART_CODE: 121,
    RESTART_CODE: 32,
    FORFEIT_CODE: 120,
    FORFEIT_AND_LEAVE_CODE: 140,
};

export const MineVisuals = {
    RESOURCE_BUBBLE: 400,
    ISLAND_RESOURCE_BUBBLE: 400,
};

export const NameToCode = {
    "Spawn": KeyCodes.SPAWN_CODE,
    "Freeze": KeyCodes.FREEZE_CODE,
    "Bridge" : KeyCodes.BRIDGE_CODE,
    "D-Bridge": KeyCodes.D_BRIDGE_CODE,
    "Zombie": KeyCodes.ZOMBIE_CODE,
    "Rage": KeyCodes.RAGE_CODE,
    "Burn": KeyCodes.BURN_CODE,
    "Nuke": KeyCodes.NUKE_CODE,
    "Poison": KeyCodes.POISON_CODE,
    "Capital": KeyCodes.CAPITAL_CODE,
    "Cannon": KeyCodes.CANNON_CODE,
    "Pump": KeyCodes.PUMP_CODE,
    "Mini-Bridge": KeyCodes.MINI_BRIDGE_CODE,
    "Wormhole": KeyCodes.WORMHOLE_CODE,
    "Over-Grow": KeyCodes.OVER_GROW_CODE,
    "Wall": KeyCodes.WALL_CODE,
};

export const AbilityElixir = {
    [KeyCodes.FREEZE_CODE]: 2,
    [KeyCodes.MINI_BRIDGE_CODE]: 2,
    [KeyCodes.D_BRIDGE_CODE]: 3,
    [KeyCodes.WALL_CODE]: 3,
    [KeyCodes.BRIDGE_CODE]: 4,
    [KeyCodes.OVER_GROW_CODE]: 4,
    [KeyCodes.RAGE_CODE]: 5,
    [KeyCodes.POISON_CODE]: 5,
    [KeyCodes.NUKE_CODE]: 6,
};


export const AbilityCredits = {
    [KeyCodes.SPAWN_CODE]: 1,
    [KeyCodes.FREEZE_CODE]: 1,
    [KeyCodes.BURN_CODE]: 1,
    [KeyCodes.ZOMBIE_CODE]: 1,
    [KeyCodes.MINI_BRIDGE_CODE]: 1,
    [KeyCodes.WORMHOLE_CODE]: 1,
    [KeyCodes.BRIDGE_CODE]: 2,
    [KeyCodes.D_BRIDGE_CODE]: 2,
    [KeyCodes.RAGE_CODE]: 2,
    [KeyCodes.POISON_CODE]: 2,
    [KeyCodes.CAPITAL_CODE]: 2,
    [KeyCodes.NUKE_CODE]: 3,
    [KeyCodes.PUMP_CODE]: 3,
    [KeyCodes.CANNON_CODE]: 4,
};

export const AbilityReloadTimes = {
    [KeyCodes.SPAWN_CODE]: 30,
    [KeyCodes.FREEZE_CODE]: 8,
    [KeyCodes.BURN_CODE]: 5,
    [KeyCodes.ZOMBIE_CODE]: 2,
    [KeyCodes.BRIDGE_CODE]: 2,
    [KeyCodes.D_BRIDGE_CODE]: 8,
    [KeyCodes.RAGE_CODE]: 20, // Adjust this based on RAGE_TICKS being defined
    [KeyCodes.NUKE_CODE]: 20,
    [KeyCodes.POISON_CODE]: 5,
    [KeyCodes.CAPITAL_CODE]: 20,
    [KeyCodes.CANNON_CODE]: 3,
    [KeyCodes.WORMHOLE_CODE]: 20,
};

export const CAPITAL_FULL_SIZE = 300;
export const PUMP_FULL_SIZE = 200;
export const CANNON_FULL_SIZE = 200;
export const ZOMBIE_FULL_SIZE = 300;
export const MINIMUM_TRANSFER_VALUE = 8;
export const PORT_COUNT = 3;
export const CAPITAL_ATTACK_RANGE = 0.8;
export const PUMP_ATTACK_RANGE = 0.8;
export const CANNON_ATTACK_RANGE = 0.6;

export const NUKE_OPTION_STRINGS = ["cannon", "pump", "capital"];
export const NUKE_OPTION_CODES = [KeyCodes.CANNON_CODE, KeyCodes.PUMP_CODE, KeyCodes.CAPITAL_CODE];
export const PRE_STRUCTURE_RANGES = {[KeyCodes.CANNON_CODE]: CANNON_FULL_SIZE * CANNON_ATTACK_RANGE,
                                    [KeyCodes.PUMP_CODE]: PUMP_FULL_SIZE * PUMP_ATTACK_RANGE,
                                    [KeyCodes.CAPITAL_CODE]: CAPITAL_FULL_SIZE * CAPITAL_ATTACK_RANGE};

export const MINI_BRIDGE_RANGE = 150;