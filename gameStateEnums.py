from enum import Enum, auto


class GameStateEnum(Enum):
    SETTINGS_SELECTION = auto()
    BUILING_GAME = auto()
    ABILITY_SELECTION = auto()
    START_SELECTION = auto()
    PLAY = auto()
    ELIMINATED = auto()
    GAME_OVER = auto()
