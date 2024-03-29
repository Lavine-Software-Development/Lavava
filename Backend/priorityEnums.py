from enum import Enum, auto

class PriorityEnum(Enum):
    NEW_EDGE = auto()
    BURNED_NODE = auto()