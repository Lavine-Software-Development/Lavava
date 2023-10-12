from constants import *

class Node:

    def __init__(self, id, pos):
        self.item_type = NODE
        self.value = 0
        self.owner = None
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.type = NODE

    def __str__(self):
        return str(self.id)

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

    def capture(self, clicker):
        if self.poisoned:
            self.end_poison()
        elif self.state == 'capital':
            self.owner.lose_capital(self)
            
        self.normalize()
        self.owner = clicker
        clicker.count += 1
        self.check_edge_stati()
        self.expand()

    @property
    def current_incoming(self):
        return [edge for edge in self.incoming if edge.to_node == self]

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

    @property
    def edges(self):
        return self.incoming + self.outgoing

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]