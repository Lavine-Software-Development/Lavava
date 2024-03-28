from jsonable import Jsonable
from constants import TIME_AMOUNT
from abc import ABC, abstractmethod

class AbstractAbility(ABC, Jsonable):
    def __init__(self, id, validation_func, effect_func, in_game_cost, player, remaining=float("inf")):
        self.id = id
        self.validation_func = validation_func
        self.effect_func = effect_func
        self.in_game_cost = in_game_cost
        self.player = player
        self.remaining = remaining
        self.tick_values = {'remaining', 'percentage'}

    @abstractmethod
    def counter(self):
        pass

    def can_use(self, data):
        return self.counter() >= self.in_game_cost and self.validation_func(data)
    
    @abstractmethod
    def update(self):
        pass

    def use(self, data):
        self.remaining -= 1
        self.effect_func(data, self.player)

    @property
    def percentage(self):
        return min(1, self.counter() / self.in_game_cost)


class ReloadAbility(AbstractAbility):
    def __init__(self, id, validation_func, effect_func, in_game_cost, player, remaining):
        super().__init__(id, validation_func, effect_func, in_game_cost, player, remaining)
        self.load_amount = 0

    def counter(self):
        return self.load_amount
    
    def update(self):
        self.load_amount += TIME_AMOUNT

    def use(self, data):
        super().use(data)
        self.load_amount = 0


class MoneyAbility(AbstractAbility):

    def counter(self):
        return self.player.money
    
    def update(self):
        pass