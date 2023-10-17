from abc import ABC, abstractmethod
from constants import *

class Ability(ABC):

    def __init__(self, main_player, key, name, cost, color, shape, letter=None, click_type=NODE):
        self.main_player = main_player
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color
        self.shape = shape
        self.click_type = click_type
        self.letter = letter

    @abstractmethod
    def validate(self, item):
        pass

    @abstractmethod
    def effect(self, data):
        pass

    def wipe(self):
        pass

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(*data)

    def complete_check(self, item):
        return [item]

    def complete(self, item):
        if data := self.complete_check(item):
            self.wipe()
            return data
        return False

class Bridge(Ability):
    def __init__(self, main_player, new_edge_id, check_new_edge, buy_new_edge):
        super().__init__(main_player, BRIDGE_CODE, 'Bridge', BRIDGE_COST, DARK_YELLOW, 'triangle', 'A')
        self.first_node = None
        self.new_edge_id = new_edge_id
        self.check_new_edge = check_new_edge
        self.buy_new_edge = buy_new_edge

    def effect(self, id1, id2, id3):
        return self.buy_new_edge(id1, id2.id, id3.id)

    def validate(self, node):
        if self.first_node is not None:
            return self.first_node.id != node.id and self.check_new_edge(self.first_node.id, node.id)
        else:
            return node.owner == self.main_player

    def wipe(self):
        self.first_node = None

    def complete_check(self, node):
        if self.first_node is None:
            self.first_node = node
            return False
        return (self.new_edge_id(self.first_node.id), self.first_node.id, node.id)

class BasicAttack(Ability):

    def validate(self, node):
        return node.owner != self.main_player and node.owner is not None and node.state not in ['capital', 'resource']

class Nuke(BasicAttack):

    def __init__(self, main_player, remove_node):
        super().__init__(main_player, NUKE_CODE, 'Nuke', NUKE_COST, BLACK, 'square', 'N')
        self.remove_node = remove_node

    def effect(self, node):
        self.remove_node(node.id)


class Poison(BasicAttack):

    def __init__(self, main_player):
        super().__init__(main_player, POISON_CODE, 'Poison', POISON_COST, PURPLE, 'circle', 'P')

    def effect(self, node):
        node.set_state('poisoned')


class Spawn(Ability):

    def __init__(self, main_player):
        super().__init__(main_player, SPAWN_CODE, 'Spawn', SPAWN_COST, main_player.default_color, 'circle')

    def validate(self, node):
        return node.owner is None and self.main_player.money >= self.cost and node.state_name == 'default'

    def effect(self, node, player):
        node.capture(player)

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(*data, player)


class Freeze(Ability):

    def __init__(self, main_player):
        super().__init__(main_player, FREEZE_CODE, 'Freeze', FREEZE_COST, LIGHT_BLUE, 'triangle', 'F', EDGE)

    def validate(self, edge):
        return edge.state == 'two-way' and edge.owned_by(self.main_player)

    def effect(self, edge):
        edge.freeze()

class Capital(Ability):

    def __init__(self, main_player):
        super().__init__(main_player, CAPITAL_CODE, 'Capital', CAPITAL_COST, PINK, 'star', 'C')

    def validate(self, node):
        if node.owner == self.main_player and node.state_name != 'capital' and node.full:
            neighbor_capital = False
            for neighbor in node.neighbors:
                if neighbor.state_name == 'capital':
                    neighbor_capital = True
                    break
            if not neighbor_capital:
                return True
        return False

    def effect(self, node):
        node.set_state('capital')

        