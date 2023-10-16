from constants import *
from nodeState import *

class Node:

    def __init__(self, id, pos, state_name='default', data=None):
        self.set_state(state_name, data)
        self.value = 0
        self.owner = None
        self.item_type = NODE
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.type = NODE

    def __str__(self):
        return str(self.id)

    def set_state(self, state_name, data=None):
        if state_name == 'default':
            self.state = DefaultState(self)
        elif state_name == "poisoned":
            self.state = PoisonedState(self)
        elif state_name == "capital":
            self.state = CapitalState(self)
        elif state_name == "mine":
            self.state = MineState(self, data)
        self.state_name = state_name

    def set_default_state(self):
        self.set_state('default')

    def click(self, clicker, button):
        if button == 1:
            self.left_click(clicker)
        elif button == 3:
            self.right_click()

    def right_click(self):
        pass

    def left_click(self, clicker):
        if self.owner == None:
            if clicker.buy_node():
                self.capture(clicker)

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if AUTO_ATTACK:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and AUTO_EXPAND:
                edge.switch(True)
                edge.popped = False

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)

    def owned_and_alive(self):
        return self.owner != None and not self.owner.eliminated

    def spread_poison(self):
        for edge in self.outgoing:
            if edge.to_node != self and edge.on and not edge.contested and edge.to_node.normal:
                edge.poisoned = True
                edge.to_node.poison_score = POISON_TICKS

    def grow(self):
        self.value += self.state.grow()
        if self.state.state_over():
            self.set_default_state()

    def delivery(self, amount, player):
        self.value += self.state.delivery(amount, player)
        if self.state.killed():
            self.capture(player)

    def update_ownerships(self, player):
        if self.owner != None:
            self.owner.count -= 1
        player.count += 1
        self.owner = player

    def capture(self, player):
        self.value = self.state.capture()
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()

    def absorbing(self):
        for edge in self.current_incoming:
            if edge.flowing:
                return True
        return False

    @property
    def full(self):
        return self.state.full

    @property
    def edges(self):
        return self.incoming + self.outgoing

    @property
    def current_incoming(self):
        return [edge for edge in self.incoming if edge.to_node == self]

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    @property
    def size(self):
        return int(5+self.state.size_factor*18)

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK
