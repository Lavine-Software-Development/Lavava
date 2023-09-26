class Ability:

    def __init__(self, key, name, cost, color, validity_func=None, effect_func=None):
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color
        self.validity_func = validity_func
        self.effect_func = effect_func

    def select(self, player):
        if s