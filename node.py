from constants import *
from nodeStateFactory import StateFactory
import math

class Node:

    def __init__(self, id, pos, state_name='default'):
        self.set_state(state_name)
        self.item_type = NODE
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.type = NODE

    def __str__(self):
        return str(self.id)

    def set_state(self, state_name):
        self.state = StateFactory.create_state(state_name, self)
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

    def capture(self):
        self.check_edge_stati()
        self.expand()

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
        self.state.grow()
        if self.state.state_over():
            self.set_default_state()

    def delivery(self, amount, player):
        return self.state.delivery(amount, player)

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
    def value(self):
        return self.state.value

    @property
    def owner(self):
        return self.state.owner

    @property
    def size(self):
        return int(5+self.size_factor()*18)

    @property
    def size_factor(self):
        if self.value<5:
            return 0
        return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)
