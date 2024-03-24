from dataclasses import dataclass, field
from typing import Optional
import math
from clickTypeEnum import ClickType
from typing import Callable

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
    id: int
    pos: tuple
    ports: list[Port]
    state: State
    value: int
    effects: set = field(default_factory=set)
    owner: Optional[OtherPlayer] = None
    type: ClickType = ClickType.NODE

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
    
    @property
    def full(self):
        return self.value >= GROWTH_STOP

@dataclass
class Edge:
    id: int
    from_node: Node
    to_node: Node
    dynamic: bool
    on: bool = False
    flowing: bool = False
    type: ClickType = ClickType.EDGE

    @property
    def color(self):
        if self.on:
            return self.from_node.color
        return (50, 50, 50)
    
    def controlled_by(self, player):
        if self.from_node.owner == player:
            return True
        return self.dynamic and self.to_node.owner == player and self.to_node.full

    
@dataclass
class AbilityVisual:
    name: str
    shape: str
    color: tuple
    letter: str = ''

@dataclass
class ReloadAbility:
    visual: AbilityVisual
    click_count: int
    click_type: ClickType
    verification_func: Callable[..., bool]
    credits: int
    reload: int
    percent: float = 1.0
    count: int = 0

    @property
    def selection_display_num(self):
        return self.credits
    
    @property
    def game_display_num(self):
        return self.count
    
    @property
    def centre_display_num(self):
        return self.count
    
    @property
    def selectable(self):
        return self.count > 0 and self.percent == 1.0

@dataclass
class GameState:
    my_player: int
    started: bool = False
    over: bool = False
    timer: int = 60
