from constants import GROWTH_RATE, POISON_TICKS, POISON_SPREAD_DELAY, \
    MINIMUM_TRANSFER_VALUE, CAPITAL_SHRINK_SPEED, MINE_DICT, BLACK, GROWTH_STOP
from abc import ABC, abstractmethod
from observable import Observable


class AbstractState(ABC, Observable):

    def __init__(self, value=0, owner=None):
        self.value = value
        self.owner = owner

    @abstractmethod
    def grow(self):
        pass

    @abstractmethod
    def delivery(self, value, amount):
        pass

    @abstractmethod
    def state_over(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK

    @property
    def full(self):
        return self.value >= GROWTH_STOP


class AbstractStandardDelivery(AbstractState):

    def __init__(self, value=0, owner=None):
        super().__init__(value, owner)
        self.reset_on_capture = False

    def delivery(self, amount, player):
        self.change_value(amount, player)
        if self.killed():
            self.capture(player)
            return self.reset_on_capture
        return False

    def change_value(self, amount, player):
        if self.owner != player:
            self.value -= amount
        else:
            self.value += amount

    def killed(self):
        return self.value < 0

    def capture(self, player):
        self.value *= -1
        self.owner = player
        self.emit('capture')

class DefaultState(AbstractStandardDelivery):

    def grow(self):
        self.value += GROWTH_RATE
    
    def state_over(self):
        return False


class PoisonedState(AbstractStandardDelivery):

    def __init__(self, value=0, owner=None):
        super().__init__(value, owner)
        self.reset_on_capture = True
        self.poison_timer = POISON_TICKS

    def grow(self):
        if self.poison_timer == POISON_TICKS - POISON_SPREAD_DELAY:
            self.emit('spread_poison')
        if self.value > MINIMUM_TRANSFER_VALUE:
            self.value -= GROWTH_RATE
        self.poison_timer -= 1

    def state_over(self):
        return self.poison_timer == 0


class CapitalState(AbstractStandardDelivery):

    def __init__(self, value=0, owner=None):
        super().__init__(value, owner)
        self.reset_on_capture = True
        self.capitalized = False

    def grow(self):
        if not self.capitalized:
            self.shrink()

    def shrink(self):
        self.value -= CAPITAL_SHRINK_SPEED
        if self.value <= MINIMUM_TRANSFER_VALUE:
            self.value = MINIMUM_TRANSFER_VALUE
            self.capitalized = True
            self.owner.capitalize(self)

    def state_over(self):
        return False

class MineState(AbstractState):

    def __init__(self, island):
        super().__init__()
        self.bonus, self.bubble, self.ring_color = MINE_DICT[island]

    def grow(self):
        pass

    def delivery(self, amount, player):
        self.value += amount
        if player != self.owner:
            self.owner = player
        return False

    def state_over(self):
        return self.value >= self.bubble