from dataclasses import dataclass, field
from typing import Optional
import math

from constants import BROWN, BLACK, GREY, GROWTH_STOP

@dataclass
class State:
    name: str

@dataclass
class MineState(State):
    bubble: int
    ring_color: tuple
    unfilled_color: tuple = GREY

@dataclass
class CapitalState(State):
    capitalized: bool = False

@dataclass
class Port:
    angle: float
    burn_percent: float = 0.0

@dataclass
class OtherPlayer:
    name: str
    color: tuple
    ready: bool = False
    eliminated: bool = False
    victor: bool = False

@dataclass
class MyPlayer(OtherPlayer):
    score: float = 0.0

@dataclass
class Node:
    pos: tuple
    ports: list[Port]
    state: State
    effects: set = field(default_factory=set)
    value: int = 0
    owner: Optional[OtherPlayer] = None

    @property
    def color(self):
        if self.owner is None:
            if len(self.ports) > 0:
                return BROWN
            else:
                return BLACK
        else:
            return self.owner.color
        
    @property
    def size(self):
        return int(5 + self.size_factor * 18)
    
    @property
    def size_factor(self):
        if self.value < 5:
            return 0
        return max(math.log10(self.value / 10) / 2 + self.value / 1000 + 0.15, 0)
    
    @property
    def state_name(self):
        return self.state.name
    
    def full(self):
        return self.value >= GROWTH_STOP

@dataclass
class Edge:
    from_node: Node
    to_node: Node
    dynamic: bool
    on: bool = False
    flowing: bool = False

    @property
    def color(self):
        if self.on:
            return self.from_node.color
        return (50, 50, 50)

@dataclass
class GameState:
    my_player: int
    started: bool = False
    over: bool = False
    timer: int = 60
