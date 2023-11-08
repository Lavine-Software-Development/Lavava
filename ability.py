from abc import ABC, abstractmethod
from constants import *

class Ability(ABC):

    def __init__(self, key, name, color, shape, letter=None, click_type=NODE):
        self.key = key
        self.name = name
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


class NewEdge(Ability):
    def __init__(self, shape, code, letter, new_edge_id, check_new_edge, buy_new_edge, edge_type):
        super().__init__(code, 'Bridge', DARK_YELLOW, shape, letter)
        self.first_node = None
        self.new_edge_id = new_edge_id
        self.check_new_edge = check_new_edge
        self.buy_new_edge = buy_new_edge
        self.edge_type = edge_type

    def effect(self, player, data):
        id1, id2, id3, bridge_type = data
        return self.buy_new_edge(id1, id2.id, id3.id, bridge_type)

    def validate(self, node):
        if self.first_node is not None:
            return self.first_node.id != node.id and node.acceptBridge() and self.check_new_edge(self.first_node.id, node.id)
        else:
            return node.owner == CONTEXT['main_player'] and node.acceptBridge()

    def wipe(self):
        self.first_node = None

    def complete_check(self, node):
        if self.first_node is None:
            self.first_node = node
            return False
        return (self.new_edge_id(self.first_node.id), self.first_node.id, node.id, self.edge_type)


class Bridge(NewEdge):
    def __init__(self, new_edge_id, check_new_edge, buy_new_edge):
        super().__init__('triangle', BRIDGE_CODE, 'A', new_edge_id, check_new_edge, buy_new_edge, EDGE)


class D_Bridge(NewEdge):
    def __init__(self, new_edge_id, check_new_edge, buy_new_edge):
        super().__init__('circle', D_BRIDGE_CODE, 'D', new_edge_id, check_new_edge, buy_new_edge, DYNAMIC_EDGE)


class BasicAttack(Ability):

    def validate(self, node):
        return node.owner != CONTEXT['main_player'] and node.owner is not None and node.state not in ['capital', 'resource']


class Nuke(BasicAttack):

    def __init__(self, remove_node):
        super().__init__(NUKE_CODE, 'Nuke', BLACK, 'square', 'N')
        self.remove_node = remove_node

    def effect(self, player, data):
        node = data[0]
        self.remove_node(node.id)


class Poison(BasicAttack):

    def __init__(self):
        super().__init__(POISON_CODE, 'Poison', PURPLE, 'circle', 'P')

    def effect(self, player, data):
        node = data[0]
        node.set_state('poisoned')


class Spawn(Ability):

    def __init__(self):
        super().__init__(SPAWN_CODE, 'Spawn', CONTEXT['main_player'].default_color, 'circle')

    def validate(self, node):
        return node.owner is None and node.state_name == 'default'

    def effect(self, player, data):
        node = data[0]
        node.capture(player)


class Freeze(Ability):

    def __init__(self):
        super().__init__(FREEZE_CODE, 'Freeze', LIGHT_BLUE, 'triangle', 'F', EDGE)

    def validate(self, edge):
        return edge.state == 'two-way' and \
            edge.from_node.owner == CONTEXT['main_player'] or edge.to_node.owner == CONTEXT['main_player']

    def effect(self, player, data):
        edge = data[0]
        if player != edge.from_node.owner:
            edge.swap()
        edge.freeze()


class Capital(Ability):

    def __init__(self):
        super().__init__(CAPITAL_CODE, 'Capital', PINK, 'star', 'C')

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


class Burn(Ability):

    def __init__(self):
        super().__init__(BURN_CODE, 'Burn', DARK_ORANGE, 'square', 'B')

    def validate(self, node):
        return node.owner is not None and node.is_port

    def effect(self, player, data):
        node = data[0]
        node.burn()