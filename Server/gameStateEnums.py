from enum import Enum, auto


class GameStateEnum(Enum):
    LOBBY = auto()
    BUILDING_GAME = auto()
    ABILITY_SELECTION = auto()
    START_SELECTION = auto()
    PLAY = auto()
    ELIMINATED = auto()
    GAME_OVER = auto()
