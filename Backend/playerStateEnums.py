from enum import Enum, auto


class PlayerStateEnum(Enum):
    ABILITY_SELECTION = auto()
    ABILITY_WAITING = auto()
    START_SELECTION = auto()
    START_WAITING = auto()
    PLAY = auto()
    ELIMINATED = auto()
    VICTORY = auto()
    LOSER = auto()