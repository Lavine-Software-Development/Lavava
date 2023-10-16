from constants import GROWTH_RATE, POISON_TICKS, POISON_SPREAD_DELAY, \
    MINIMUM_TRANSFER_VALUE, CAPITAL_SHRINK_SPEED, MINE_DICT, BLACK, GROWTH_STOP, \
    GREY
from abc import ABC, abstractmethod
import math


class AbstractState(ABC):

    def __init__(self, node):
        self.node = node
        self.reset_on_capture = False

    @property
    def value(self):
        return self.node.value

    @property
    def owner(self):
        return self.node.owner

    @abstractmethod
    def grow(self):
        pass

    @abstractmethod
    def delivery(self, value, amount):
        pass

    @abstractmethod
    def capture(self):
        pass

    @abstractmethod
    def killed(self):
        pass

    @abstractmethod
    def state_over(self):
        pass

    @property
    def size_factor(self):
        if self.value<5:
            return 0
        return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)


class DefaultState(AbstractState):

    def grow(self):
        if self.value < GROWTH_STOP:
            return GROWTH_RATE
        return 0

    def delivery(self, amount, player):
        if self.owner == None or self.owner != player:
            return -amount
        return amount

    def capture(self):
        return self.value * -1

    def killed(self):
        return self.value < 0

    def state_over(self):
        return False


class PoisonedState(DefaultState):

    def __init__(self, node):
        super().__init__(node)
        self.reset_on_capture = True
        self.poison_timer = POISON_TICKS

    def grow(self):
        self.poison_timer -= 1
        if self.poison_timer == POISON_TICKS - POISON_SPREAD_DELAY:
            self.node.spread_poison()
        if self.value > MINIMUM_TRANSFER_VALUE:
            return GROWTH_RATE * -1
        return 0

    def state_over(self):
        return self.poison_timer == 0


class CapitalState(DefaultState):

    def __init__(self, node):
        super().__init__(node)
        self.reset_on_capture = True
        self.capitalized = False

    def grow(self):
        if not self.capitalized:
            return self.shrink()
        return 0

    def shrink(self):
        if self.value + CAPITAL_SHRINK_SPEED <= MINIMUM_TRANSFER_VALUE:
            self.capitalized = True
            self.owner.capitalize(self)
            return MINIMUM_TRANSFER_VALUE - self.value
        return CAPITAL_SHRINK_SPEED

    def capture(self):
        self.owner.lose_capital(self)
        return super().capture()


class MineState(AbstractState):

    def __init__(self, node, island):
        super().__init__(node)
        self.reset_on_capture = True
        self.bonus, self.bubble, self.ring_color = MINE_DICT[island]

    def grow(self):
        return 0

    def delivery(self, amount, player):
        if player == self.owner:
            return amount
        elif self.node.absorbing():
            self.node.owner = player
            return amount
        return 0

    def killed(self):
        return self.value >= self.bubble

    def capture(self):
        return MINIMUM_TRANSFER_VALUE

    def state_over(self):
        return False

    @property
    def size_factor(self):
        return max(math.log10(self.bubble/10)/2+self.bubble/1000+0.15,0)/2

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return GREY