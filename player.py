from constants import *
from math import sqrt

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
        self.eliminated = False
        self.victory = False
        self.started = False

    def buy_node(self):
        if self.money >= BUY_NODE_COST:
            self.money -= BUY_NODE_COST
            self.started = True
            return True
        return False

    def buy_edge(self):
        if self.money >= BUILD_EDGE_COST:
            self.money -= BUILD_EDGE_COST
            return True
        return False

    def switch_considering(self):
        self.considering_edge = not self.considering_edge
        if self.money < BUILD_EDGE_COST:
            self.considering_edge = False
        self.new_edge_start = None

    def new_edge_started(self):
        return self.new_edge_start is not None

    def eliminate(self):
        self.eliminated = True
        self.money = 0
        self.color = GREY

    def update(self):
        if not self.eliminated:
            self.money += self.tick_production
        return self.started and self.count == 0

    def win(self):
        self.victory = True

    @property
    def tick_production(self):
        return round((1 + sqrt(self.count)) * MONEY_RATE, 2)

    @property
    def production_per_second(self):
        return self.tick_production * 4