from dataclasses import dataclass
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
    victor : bool = False

@dataclass
class MyPlayer(OtherPlayer):
    score: float = 0.0

@dataclass
class Node:
    value: int
    pos: tuple
    ports: list[Port]
    owner: Optional[OtherPlayer] = None

@dataclass
class Edge:
    from_node: Node
    to_node: Node
    on: bool
    flowing: bool
    dynamic: bool

@dataclass
class GameState:
    my_player: int
    started: bool = False
    over: bool = False
    timer: int = 60


    