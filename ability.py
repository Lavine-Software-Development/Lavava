from abc import ABC, abstractmethod
from constants import *

class Ability(ABC):

    def __init__(self, key, name, cost, color):
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color

    @abstractmethod
    def build(self, player, node):
        pass

    @abstractmethod
    def effect(self, player, node):
        pass

    def select(self, player):
        if player.mode == self.key:
            player.mode = 'default'
        elif player.money >= self.cost:
            player.mode = self.key

    def use(self, player, node):
        if data := self.build(player, node):
            return self.success(player, data)
        return False

    def success(self, player, data):
        player.mode = 'default'
        return data


class Bridge(Ability):
    def __init__(self):
        super().__init__(BRIDGE_KEY, 'Bridge', BRIDGE_COST, DARK_YELLOW)
        self.first_node = None
        self.board = None

    def set_board(self, board):
        self.board = board

    def build(self, player, node):
        if self.first_node is not None:
            if new_edge_id := self.board.check_new_edge(self.first_node, node.id):
                old_node_id = self.first_node
                self.first_node = None
                return (new_edge_id, node.id, old_node_id)
        else:
            if node.owner == player:
                self.first_node = node.id
        return False

    def effect(self, player, node):
        pass
        