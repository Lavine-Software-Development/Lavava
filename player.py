from constants import *

class Player:

    def __init__(self, color, id):
        self.money = START_MONEY
        self.count = 0
        self.begun = False
        self.color = color
        self.id = id
        self.auto_expand = True
        self.auto_attack = False
        self.considering_edge = False
        self.new_edge_start = None
        self.highlighted_node = None

    def buy_node(self):
        if self.money >= BUY_NODE_COST:
            self.money -= BUY_NODE_COST
            return True
        return False

    def buy_edge(self):
        if self.money >= BUILD_EDGE_COST:
            self.money -= BUILD_EDGE_COST
            return True
        return False

    def switch_autoplay(self):
        self.autoplay = not self.autoplay

    def switch_considering(self):
        self.considering_edge = not self.considering_edge
        self.new_edge_start = None

    def new_edge_started(self):
        return self.new_edge_start is not None