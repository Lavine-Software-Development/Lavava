from jsonable import JsonableTracked
from constants import TIME_AMOUNT
from abc import abstractmethod
from tracking_decorator.track_changes import track_changes

class AbstractAbility(JsonableTracked):
    def __init__(self, id, validation_func, effect_func, in_game_cost, player):
        self.validation_func = validation_func
        self.effect_func = effect_func
        self.in_game_cost = in_game_cost
        self.player = player

        super().__init__(id)

        self.create_attributes()

    def create_attributes(self):
        pass

    @abstractmethod
    def counter(self):
        pass

    def can_use(self, data):
        return self.counter >= self.in_game_cost and self.validation_func(data)
    
    @abstractmethod
    def update(self):
        pass

    def use(self, data):
        self.effect_func(data, self.player)

    @property
    def percentage(self):
        return min(1, self.counter / self.in_game_cost)


@track_changes('remaining', ('load_amount', 'percentage'))
class CreditAbility(AbstractAbility):

    def __init__(self, id, validation_func, effect_func, in_game_cost, player, remaining):
        super().__init__(id, validation_func, effect_func, in_game_cost, player)
        self.remaining = remaining

    def create_attributes(self):
        self.load_amount = 0

    @property
    def counter(self):
        return self.load_amount
    
    def update(self):
        if self.remaining > 0:
            self.load_amount += TIME_AMOUNT

    def use(self, data):
        super().use(data)
        self.remaining -= 1
        self.load_amount = 0


@track_changes(('chop', 'percentage'))
class RoyaleAbility(AbstractAbility):

    def create_attributes(self):
        # Updated occasionally so the percentage is only checked on whole numbers. Same way elixir works
        self.chop = 0

    @property
    def counter(self):
        return self.player.elixir
    
    def update(self):
        self.chop += 1

    def use(self, data):
        super().use(data)
        self.player.elixir -= self.in_game_cost
        print(self.player.elixir)