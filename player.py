from constants import *

class Player:

    def __init__(self, color, id):
        self.default_color = color[0]
        self.name = color[1]
        self.id = id
        self.auto_expand = True
        self.auto_attack = False
        self.points = 0
        self.default_values()

    def default_values(self):
        self.money = START_MONEY
        self.count = 0
        self.begun = False
        self.mode = 'default'
        self.highlighted_node = None
        self.eliminated = False
        self.victory = False
        self.tick_production = MONEY_RATE
        self.placement = 0
        self.color = self.default_color

    def buy_node(self):
        if self.money >= BUY_NODE_COST:
            self.money -= BUY_NODE_COST
            return True
        return False

    def eliminate(self, placement):
        self.eliminated = True
        self.money = 0
        self.color = GREY
        self.placement = placement

    def update(self):
        if not self.eliminated:
            self.money += self.tick_production
            return self.count == 0
        return False

    def win(self):
        self.victory = True
        self.placement = 0

    def display(self):
        print(f"{self.name}|| {self.points}")

    @property
    def production_per_second(self):
        return self.tick_production * 10