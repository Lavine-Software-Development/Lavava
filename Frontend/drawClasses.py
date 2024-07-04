from dataclasses import dataclass, field
from typing import Optional
import math
from clickTypeEnum import ClickType
from typing import Callable
from angled_position import angles

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
class CannonState(State):
    angle: int = angles(1)[0]

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
class IDItem():
    id: int
    type: ClickType

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, IDItem):
            return self.id == other.id
        return False

@dataclass(unsafe_hash=True)
class Node(IDItem):
    pos: tuple
    is_port: bool
    port_percent: float
    ports: list
    state: State
    value: int
    effects: set = field(default_factory=set)
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
    
    @property
    def full(self):
        return self.value >= GROWTH_STOP
    
    @property
    def port_count(self):
        return len(self.ports)

@dataclass
class Edge(IDItem):
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
    
    def controlled_by(self, player):
        if self.from_node.owner == player:
            return True
        return self.dynamic and self.to_node.owner == player and self.to_node.full
    
    def other(self, node):
        if node == self.from_node:
            return self.to_node
        elif node == self.to_node:
            return self.from_node
        else:
            raise ValueError('Node not in edge')
        

@dataclass
class EventVisual():
    name: str
    color: tuple

@dataclass
class Event:
    visual: EventVisual
    click_count: int
    click_type: ClickType
    verification_func: Callable[..., bool]
    
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
    remaining: int = 0
    percentage: float = 1.0
    
    @property
    def game_display_num(self):
        return self.remaining
    
    @property
    def selectable(self):
        return self.remaining > 0 and self.percentage == 1.0