from jsonable import JsonableTracked
from constants import TIME_AMOUNT
from abc import abstractmethod
from track_change_decorator import track_changes

@track_changes('remaining')
class AbstractAbility(JsonableTracked):
    def __init__(self, id, validation_func, effect_func, in_game_cost, player, remaining=float("inf")):
        self.validation_func = validation_func
        self.effect_func = effect_func
        self.in_game_cost = in_game_cost
        self.player = player
        self.remaining = remaining

        super().__init__(id)

    @abstractmethod
    def counter(self):
        pass

    def can_use(self, data):
        return self.counter >= self.in_game_cost and self.validation_func(data)
    
    @abstractmethod
    def update(self):
        pass

    def use(self, data):
        self.remaining -= 1
        self.effect_func(data, self.player)

    @property
    def percentage(self):
        return min(1, self.counter / self.in_game_cost)


@track_changes(('load_amount', 'percentage'))
class ReloadAbility(AbstractAbility):
    def __init__(self, id, validation_func, effect_func, in_game_cost, player, remaining):
        super().__init__(id, validation_func, effect_func, in_game_cost, player, remaining)
        self.load_amount = 0

    @property
    def counter(self):
        return self.load_amount
    
    def update(self):
        self.load_amount += TIME_AMOUNT

    def use(self, data):
        super().use(data)
        self.load_amount = 0


class MoneyAbility(AbstractAbility):

    @property
    def counter(self):
        return self.player.money
    
    def update(self):
        pass