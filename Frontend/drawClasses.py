from dataclasses import dataclass, field
from typing import Optional


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
    state: str
    effects: set = field(default_factory=set)
    value: int = 0
    owner: Optional[OtherPlayer] = None


@dataclass
class Edge:
    from_node: Node
    to_node: Node
    dynamic: bool
    on: bool = False
    flowing: bool = False


@dataclass
class GameState:
    my_player: int
    started: bool = False
    over: bool = False
    timer: int = 60
