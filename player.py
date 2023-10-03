from constants import *

class Player:

    def __init__(self, color, id):
        self.default_color = color[0]
        self.name = color[1]
        self.id = id
        self.points = 0
        self.default_values()

    def default_values(self):
        self.money = START_MONEY
        self.count = 0
        self.begun = False
        self.mode = DEFAULT_ABILITY_CODE
        self.highlighted_node = None
        self.eliminated = False
        self.victory = False
        self.tick_production = MONEY_RATE
        self.color = self.default_color
        self.capitals = {}

    def eliminate(self):
        self.eliminated = True
        self.money = 0
        self.color = GREY
        self.points += self.count

    def update(self):
        self.money += self.tick_production

    def win(self):
        self.victory = True
        self.points += NODE_COUNT

    def display(self):
        print(f"{self.name}|| {self.points}")

    def capitalize(self, capital):
        self.tick_production += CAPITAL_BONUS
        self.capitals[capital.id] = capital

    def lose_capital(self, capital):
        self.tick_production -= CAPITAL_BONUS
        del self.capitals[capital.id]

    def check_capital_win(self):
        return self.capital_count == CAPITAL_WIN_COUNT

    @property
    def capital_count(self):
        return len([c for c in self.capitals.values() if c.full])

    @property
    def production_per_second(self):
        return self.tick_production * 10