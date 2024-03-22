from enum import Enum, auto


class PlayerStateEnum(Enum):
    WAITING = auto()
    ABILITIES_SELECTED = auto()
    START_SELECTED = auto()
    PLAYING = auto()
    ELIMINATED = auto()
    VICTORY = auto()