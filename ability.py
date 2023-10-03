from abc import ABC, abstractmethod
from constants import *

class Ability(ABC):

    def __init__(self, key, name, cost, color, shape, letter=None, click_type=NODE):
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color
        self.shape = shape
        self.click_type = click_type
        self.letter = letter

    @abstractmethod
    def validate(self, player, item):
        pass

    @abstractmethod
    def effect(self, data):
        pass

    def wipe(self):
        pass

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(*data)

    def complete(self, item):
        return [item.id]


class Bridge(Ability):
    def __init__(self, check_new_edge, buy_new_edge, new_edge_id):
        super().__init__(BRIDGE_CODE, 'Bridge', BRIDGE_COST, DARK_YELLOW, 'triangle', 'A')
        self.first_node = None
        self.check_new_edge = check_new_edge
        self.buy_new_edge = buy_new_edge
        self.new_edge_id = new_edge_id

    def effect(self, id1, id2, id3):
        return self.buy_new_edge(id1, id2.id, id3.id)

    def validate(self, player, node):
        if self.first_node is not None:
            return self.check_new_edge(self.first_node, node.id)
        else:
            return node.owner == player

    def wipe(self):
        self.first_node = None

    def complete(self, node):
        if not self.first_node:
            self.first_node = node.id
            return False
        return (self.new_edge_id(self.first_node), self.first_node, node.id)


class BasicAttack(Ability):

    def validate(self, player, node):
        return node.owner != player and node.owner is not None and node.state not in ['capital', 'resource']

class Nuke(BasicAttack):

    def __init__(self, remove_node):
        super().__init__(NUKE_CODE, 'Nuke', NUKE_COST, BLACK, 'square', 'N')
        self.remove_node = remove_node

    def effect(self, node):
        self.remove_node(node.id)


class Poison(BasicAttack):

    def __init__(self):
        super().__init__(POISON_CODE, 'Poison', POISON_COST, PURPLE, 'circle', 'P')

    def effect(self, node):
        node.poison_score = POISON_TICKS


class Spawn(Ability):

    def __init__(self, color):
        super().__init__(SPAWN_CODE, 'Spawn', SPAWN_COST, color, 'circle')

    def validate(self, player, node):
        return node.owner is None and player.money >= self.cost and node.normal

    def effect(self, node, player):
        node.capture(player)

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(*data, player)


class Freeze(Ability):

    def __init__(self):
        super().__init__(FREEZE_CODE, 'Freeze', FREEZE_COST, LIGHT_BLUE, 'triangle', 'F', EDGE)

    def validate(self, player, edge):
        return edge.state == 'two-way' and edge.owned_by(player):

    def effect(self, edge):
        edge.freeze()

class Capital(Ability):

    def __init__(self):
        super().__init__(CAPITAL_CODE, 'Capital', CAPITAL_COST, PINK, 'star', 'C')

    def validate(self, player, node):
        if node.owner == player and node.state != 'capital':
            neighbor_capital = False
            for neighbor in node.neighbors:
                if neighbor.state == 'capital':
                    neighbor_capital = True
                    break
            if not neighbor_capital:
                return True
        return False

    def effect(self, node):
        node.capitalize()

        