from enum import Enum, auto


class PlayerStateEnum(Enum):
    WAITING = auto()
    START_SELECTION = auto()
    START_WAITING = auto()
    PLAY = auto()
    ELIMINATED = auto()
    VICTORY = auto()
    LOSER = auto()