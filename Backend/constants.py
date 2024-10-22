from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AbilityBreakdown:
    letter: str
    name: str
    cost: int
    reload: int = 0
    credits: int = 0
    elixir: int = 0
    tick: Optional[int] = None
    eliminate_val: Optional[int] = None


@dataclass
class AbilityVisual:
    ab: AbilityBreakdown
    shape: str
    color: tuple
    count: int = 0


NODE_COUNT = 65
EDGE_COUNT = 60
MAX_EDGE_LENGTH = 7
ONE_WAY_COUNT = 17  # to 1
MIN_ANGLE = 15

TIME_AMOUNT = 0.1

NODE = "node"
PORT_NODE = "port node"
WALL_NODE = "wall node"
EDGE = "edge"
DYNAMIC_EDGE = "dynamic edge"

MODES = {1: "Money", 2: "Reload", 3: "Ports"}

STATE_NAMES = {"default", "capital", "mine", "zombie", "cannon", "pump"}
EFFECT_NAMES = {"burn", "poison", "rage", "zombified", "over_grow"}

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CAPITALS_NEEDED_FOR_WIN = 3
CAPITAL_FULL_SIZE = 300

ABILITY_START_HEIGHT = 0.005
ABILITY_SIZE = 0.19
HORIZONTAL_ABILITY_GAP = 0.2
VERTICAL_ABILITY_GAP = 0.2
ABILITY_FONT = 0.05
FONT_GAP = 0.035

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MEDIUM_GREEN = (179, 255, 149)
LIGHT_GREEN = (209, 255, 189)
DARK_GREEN = (0, 100, 0)
ORANGE = (243, 156, 18)
DARK_ORANGE = (193, 106, 8)
STRONG_ORANGE = (255, 77, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (204, 204, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
PURPLE = (153, 51, 255)
PINK = (255, 51, 153)
LIGHT_BLUE = (173, 216, 230)
BROWN = (150, 75, 0)
DARK_GRAY = (64, 64, 64)

ZOMBIE_FULL_SIZE = 300
NODE_MINIMUM_VALUE = 5

MINIMUM_TRANSFER_VALUE = 8
BEGIN_TRANSFER_VALUE = 13

STANDARD_SWAP_STATUS = 1
BELOW_SWAP_STATUS = 0

START_MONEY = 0
START_MONEY_RATE = 0.7
START_CREDITS = 20

RESOURCE_BONUS = 0.2
RESOURCE_BUBBLE = 400
ISLAND_RESOURCE_BONUS = 0.4
ISLAND_RESOURCE_BUBBLE = 400
NETWORK_RESOURCE_COUNT = 3
ISLAND_RESOURCE_COUNT = 4
RESOURCE_RECOUP = 0.15

CAPITAL_START_SIZE = 50

MINE_DICT = {
    True: (ISLAND_RESOURCE_BONUS, ISLAND_RESOURCE_BUBBLE, YELLOW, 4),
    False: (RESOURCE_BONUS, RESOURCE_BUBBLE, DARK_YELLOW, 3),
}

COUNTDOWN_LENGTH = 60.0

KILL_BONUS = 3
OVERTIME_BONUS = 3

TICK = 0
ELIMINATE_VAL = -1
RESTART_GAME_VAL = -2
ABILITIES_SELECTED = -3

STANDARD_LEFT_CLICK = 1
STANDARD_RIGHT_CLICK = 3
CANNON_SHOT_CODE = 4
PUMP_DRAIN_CODE = 5
CREDIT_USAGE_CODE = 6
NODE_LEFT_CLICK = 7
NODE_RIGHT_CLICK = 9

BURN_TICKS = 50
POISON_TICKS = 225
RAGE_TICKS = 175
ZOMBIE_TICKS = float("inf")
OVER_GROW_TICKS = 250

MINI_BRIDGE_RANGE = 150

CANNON_SHOT_DAMAGE_PERCENTAGE = 1 / 3
CANNON_SHOT_SHRINK_RANGE_CUTOFF = 400
JATAPULT_SHOT_DAMAGE_PERCENTAGE = 2 / 5
JATAPULT_SHOT_SHRINK_RANGE_CUTOFF = 500

PUMP_INTAKE_MULTIPLIER = 1.5

SPAWN_COST = 100
FREEZE_COST = 75
BURN_COST = 75
WALL_COST = 75
ZOMBIE_COST = 75
BRIDGE_COST = 175
D_BRIDGE_COST = 200
RAGE_COST = 100
NUKE_COST = 350
POISON_COST = 350
CAPITAL_COST = 450
CANNON_COST = 400
PUMP_COST = 400  # update
MINI_BRIDGE_COST = 50
OVER_GROW_COST = 80
WORMHOLE_COST = 200

SPAWN_CREDITS = 1
FREEZE_CREDITS = 1
BURN_CREDITS = 1
WALL_CREDITS = 1
ZOMBIE_CREDITS = 1
BRIDGE_CREDITS = 2
D_BRIDGE_CREDITS = 2
RAGE_CREDITS = 2
OVER_GROW_CREDITS = 2
POISON_CREDITS = 2
NUKE_CREDITS = 3
CAPITAL_CREDITS = 2
CANNON_CREDITS = 4
PUMP_CREDITS = 3
MINI_BRIDGE_CREDITS = 1

SPAWN_ELIXIR = 1
FREEZE_ELIXIR = 3
MINI_BRIDGE_ELIXIR = 2
D_BRIDGE_ELIXIR = 3
BRIDGE_ELIXIR = 5
OVER_GROW_ELIXIR = 2
RAGE_ELIXIR = 5
NUKE_ELIXIR = 7
WALL_ELIXIR = 2
POISON_ELIXIR = 4
CANNON_ELIXIR = 6

SPAWN_RELOAD = 20
FREEZE_RELOAD = 4
BURN_RELOAD = 1
WALL_RELOAD = 1
ZOMBIE_RELOAD = 2
BRIDGE_RELOAD = 2
D_BRIDGE_RELOAD = 8
RAGE_RELOAD = int(RAGE_TICKS / 10)
OVER_GROW_RELOAD = int(OVER_GROW_TICKS / 10)
NUKE_RELOAD = 2
POISON_RELOAD = 5
CAPITAL_RELOAD = 15
CANNON_RELOAD = 15
PUMP_RELOAD = 15
MINI_BRIDGE_RELOAD = 10
WORMHOLE_RELOAD = 10

SPAWN_CODE = 115  # S
FREEZE_CODE = 102
BRIDGE_CODE = 97  # A
D_BRIDGE_CODE = 100
ZOMBIE_CODE = 122
RAGE_CODE = 114
BURN_CODE = 98
WALL_CODE = 118  # V
NUKE_CODE = 110
OVER_GROW_CODE = 111
POISON_CODE = 112
CAPITAL_CODE = 99
CANNON_CODE = 101  # E
PUMP_CODE = 117  # U
MINI_BRIDGE_CODE = 109
WORMHOLE_CODE = 119

POISON_SPREAD_DELAY = 15
BURN_SPREAD_DELAY = 15

DEFAULT_ABILITY_CODE = SPAWN_CODE
RESTART_CODE = 32
FORFEIT_CODE = 120
OVERRIDE_RESTART_CODE = 121
FORFEIT_AND_LEAVE_CODE = 140

CAPITAL_BONUS = 0.2
STANDARD_SHRINK_SPEED = -20

RAGE_MULTIPLIER = 3.5
POISON_MULTIPLIER = 1.5

ALL_ABILITIES = {
    SPAWN_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    MINI_BRIDGE_CODE,
    NUKE_CODE,
    POISON_CODE,
    FREEZE_CODE,
    CAPITAL_CODE,
    BURN_CODE,
    RAGE_CODE,
    ZOMBIE_CODE,
    CANNON_CODE,
    PUMP_CODE,
    WORMHOLE_CODE,
    OVER_GROW_CODE,
    WALL_CODE,
}

BASIC_ABILITIES = {
    SPAWN_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    NUKE_CODE,
    FREEZE_CODE,
    RAGE_CODE,
    OVER_GROW_CODE,
    WALL_CODE,
    CANNON_CODE,
}


SPAWN_BREAKDOWN = AbilityBreakdown(
    "S", "Spawn", SPAWN_COST, SPAWN_RELOAD, SPAWN_CREDITS, SPAWN_ELIXIR
)
BRIDGE_BREAKDOWN = AbilityBreakdown(
    "A", "Bridge", BRIDGE_COST, BRIDGE_RELOAD, BRIDGE_CREDITS, BRIDGE_ELIXIR
)
D_BRIDGE_BREAKDOWN = AbilityBreakdown(
    "D", "D-Bridge", D_BRIDGE_COST, D_BRIDGE_RELOAD, D_BRIDGE_CREDITS, D_BRIDGE_ELIXIR
)
NUKE_BREAKDOWN = AbilityBreakdown(
    "N", "Nuke", NUKE_COST, NUKE_RELOAD, NUKE_CREDITS, NUKE_ELIXIR
)
POISON_BREAKDOWN = AbilityBreakdown(
    "P", "Poison", POISON_COST, POISON_RELOAD, POISON_CREDITS, POISON_ELIXIR
)
FREEZE_BREAKDOWN = AbilityBreakdown(
    "F", "Freeze", FREEZE_COST, FREEZE_RELOAD, FREEZE_CREDITS, FREEZE_ELIXIR
)
CAPITAL_BREAKDOWN = AbilityBreakdown(
    "C", "Capital", CAPITAL_COST, CAPITAL_RELOAD, CAPITAL_CREDITS
)
ZOMBIE_BREAKDOWN = AbilityBreakdown(
    "Z", "Zombie", ZOMBIE_COST, ZOMBIE_RELOAD, ZOMBIE_CREDITS
)
BURN_BREAKDOWN = AbilityBreakdown("B", "Burn", BURN_COST, BURN_RELOAD, BURN_CREDITS)
WALL_BREAKDOWN = AbilityBreakdown(
    "V", "Wall", WALL_COST, WALL_RELOAD, WALL_CREDITS, WALL_ELIXIR
)
RAGE_BREAKDOWN = AbilityBreakdown(
    "R", "Rage", RAGE_COST, RAGE_RELOAD, RAGE_CREDITS, RAGE_ELIXIR
)
OVER_GROW_BREAKDOWN = AbilityBreakdown(
    "O",
    "Over-Grow",
    OVER_GROW_COST,
    OVER_GROW_RELOAD,
    OVER_GROW_CREDITS,
    OVER_GROW_ELIXIR,
)
CANNON_BREAKDOWN = AbilityBreakdown(
    "E", "Cannon", CANNON_COST, CANNON_RELOAD, CANNON_CREDITS, CANNON_ELIXIR
)
PUMP_BREAKDOWN = AbilityBreakdown("U", "Pump", PUMP_COST, PUMP_RELOAD, PUMP_CREDITS)
MINI_BRIDGE_BREAKDOWN = AbilityBreakdown(
    "M", "Mini-Bridge", MINI_BRIDGE_COST, MINI_BRIDGE_RELOAD, MINI_BRIDGE_CREDITS
)
WORMHOLE_BREAKDOWN = AbilityBreakdown("W", "Wormhole", WORMHOLE_COST, WORMHOLE_RELOAD)

BREAKDOWNS = {
    SPAWN_CODE: SPAWN_BREAKDOWN,
    FREEZE_CODE: FREEZE_BREAKDOWN,
    BURN_CODE: BURN_BREAKDOWN,
    ZOMBIE_CODE: ZOMBIE_BREAKDOWN,
    BRIDGE_CODE: BRIDGE_BREAKDOWN,
    D_BRIDGE_CODE: D_BRIDGE_BREAKDOWN,
    RAGE_CODE: RAGE_BREAKDOWN,
    POISON_CODE: POISON_BREAKDOWN,
    NUKE_CODE: NUKE_BREAKDOWN,
    CAPITAL_CODE: CAPITAL_BREAKDOWN,
    CANNON_CODE: CANNON_BREAKDOWN,
    PUMP_CODE: PUMP_BREAKDOWN,
    MINI_BRIDGE_CODE: MINI_BRIDGE_BREAKDOWN,
    WORMHOLE_CODE: WORMHOLE_BREAKDOWN,
    OVER_GROW_CODE: OVER_GROW_BREAKDOWN,
    WALL_CODE: WALL_BREAKDOWN,
}

STRUCTURE_RANGES = {"capital": 0.85, "cannon": 0.65, "pump": 0.85}
EVENTS = {
    CANNON_SHOT_CODE,
    PUMP_DRAIN_CODE,
    STANDARD_LEFT_CLICK,
    STANDARD_RIGHT_CLICK,
    CREDIT_USAGE_CODE,
    NODE_LEFT_CLICK,
    NODE_RIGHT_CLICK,
}


BOT_START_DELAY = 50
AI_REGULAR_WAIT_TIME = 25
AI_DELAYED_WAIT_TIME = 198
