from enum import Enum, auto


class GameStateEnum(Enum):
    LOBBY = auto()
    BUILDING_GAME = auto()
    START_SELECTION = auto()
    PLAY = auto()
    END_GAME = auto()
    GAME_OVER = auto()
