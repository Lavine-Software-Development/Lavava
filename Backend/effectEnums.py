from enum import Enum, auto


class EffectType(Enum):
    NONE = auto()
    GROW = auto()
    GROW_CAP = auto()
    EXPEL = auto()
    INTAKE = auto()
