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
    def validate(self, item):
        pass

    @abstractmethod
    def effect(self, player, data):
        pass

    def wipe(self):
        pass

    def complete_check(self, item):
        return [item]

    def complete(self, item):
        if data := self.complete_check(item):
            self.wipe()
            return data
        return False

class Bridge(Ability):
    def __init__(self, cost, new_edge_id, check_new_edge, buy_new_edge):
        super().__init__(BRIDGE_CODE, 'Bridge', cost, DARK_YELLOW, 'triangle', 'A')
        self.first_node = None
        self.new_edge_id = new_edge_id
        self.check_new_edge = check_new_edge
        self.buy_new_edge = buy_new_edge

    def effect(self, player, data):
        id1, id2, id3 = data
        return self.buy_new_edge(id1, id2.id, id3.id)

    def validate(self, node):
        if self.first_node is not None:
            return self.first_node.id != node.id and self.check_new_edge(self.first_node.id, node.id)
        else:
            return node.owner == CONTEXT['main_player']

    def wipe(self):
        self.first_node = None

    def complete_check(self, node):
        if self.first_node is None:
            self.first_node = node
            return False
        return (self.new_edge_id(self.first_node.id), self.first_node.id, node.id)

class BasicAttack(Ability):

    def validate(self, node):
        return node.owner != CONTEXT['main_player'] and node.owner is not None and node.state not in ['capital', 'resource']

class Nuke(BasicAttack):

    def __init__(self, cost, remove_node):
        super().__init__(NUKE_CODE, 'Nuke', cost, BLACK, 'square', 'N')
        self.remove_node = remove_node

    def effect(self, player, data):
        node = data[0]
        self.remove_node(node.id)


class Poison(BasicAttack):

    def __init__(self, cost):
        super().__init__(POISON_CODE, 'Poison', cost, PURPLE, 'circle', 'P')

    def effect(self, player, data):
        node = data[0]
        node.set_state('poisoned')


class Spawn(Ability):

    def __init__(self, cost):
        super().__init__(SPAWN_CODE, 'Spawn', cost, CONTEXT['main_player'].default_color, 'circle')

    def validate(self, node):
        return node.owner is None and node.state_name == 'default'

    def effect(self, player, data):
        node = data[0]
        node.capture(player)

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(*data, player)


class Freeze(Ability):

    def __init__(self, cost):
        super().__init__(FREEZE_CODE, 'Freeze', cost, LIGHT_BLUE, 'triangle', 'F', EDGE)

    def validate(self, edge):
        return edge.state == 'two-way' and edge.owned_by( CONTEXT['main_player'])

    def effect(self, player, data):
        edge = data[0]
        edge.freeze()

class Capital(Ability):

    def __init__(self, cost):
        super().__init__(CAPITAL_CODE, 'Capital', cost, PINK, 'star', 'C')

    def validate(self, node):
        if node.owner ==  CONTEXT['main_player'] and node.state_name != 'capital' and node.full:
            neighbor_capital = False
            for neighbor in node.neighbors:
                if neighbor.state_name == 'capital':
                    neighbor_capital = True
                    break
            if not neighbor_capital:
                return True
        return False

    def effect(self, player, data):
        node = data[0]
        node.set_state('capital')

        