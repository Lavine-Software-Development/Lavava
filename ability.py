class Ability:

    def __init__(self, key, name, cost, color, validity_func=None, effect_func=None):
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color
        self.validity_func = validity_func
        self.effect_func = effect_func

    def select(self, player):
        if player.mode == self.key:
            player.mode = 'default'
        elif player.money >= self.cost:
            player.mode = self.key