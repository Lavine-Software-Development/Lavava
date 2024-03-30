from enum import Enum, auto

class PriorityEnum(Enum):
    NEW_EDGE = auto()
    LOST_NODE = auto()
    OTHER = auto()