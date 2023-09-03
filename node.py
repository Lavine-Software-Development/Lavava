import math
from constants import *

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos

    def __str__(self):
        return str(self.id)

    def grow(self):
        if not self.full:
            self.value += GROWTH_RATE

    def click(self, clicker, button):
        self.clicker = clicker
        if button == 1:
            self.left_click()

    def left_click(self):
        if self.owner == None:
            if self.clicker.buy_node():
                self.capture()

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if self.owner.auto_attack:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and self.owner.auto_expand:
                edge.switch(True)
                edge.popped = False

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def capture(self, clicker=None):
        if clicker is None:
            clicker = self.clicker
        self.owner = clicker
        clicker.count += 1
        self.check_edge_stati()
        self.expand()

    def killed(self):
        if self.value < 0:
            self.value *= -1
            if self.owner:
                self.owner.count -= 1
            return True
        return False

    def size_factor(self):
        if self.value<5:
            return 0
        return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)

    @property
    def size(self):
        return int(5+self.size_factor()*18)

    @property
    def color(self):
        if self.owner:
            if self.value >= 250:
                return self.owner.color
            return self.owner.color
        return BLACK

    @property
    def full(self):
        return self.value >= GROWTH_STOP
