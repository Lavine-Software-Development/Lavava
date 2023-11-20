from abc import ABC, abstractmethod, abstractproperty
from constants import BURN_TICKS, POISON_TICKS, RAGE_TICKS, RAGE_MULTIPLIER
from effectEnums import EffectType

class AbstractEffect(ABC):

    def __init__(self, node, expiry_time, effect_type):
        self.node = node
        self.expiry_time = expiry_time
        self.counter = 0
        self.effect_type = effect_type

    def count(self):
        self.counter += 1

    def complete(self):
        pass

    def effect(self, amount):
        return amount

    @property
    def expired(self):
        return self.counter >= self.expiry_time


class Burning(AbstractEffect):

    def __init__(self, node):
        super().__init__(node, BURN_TICKS, EffectType.NONE)

    def complete(self):
        self.node.lose_ports()


class Poisoned(AbstractEffect):

    def __init__(self, node):
        super().__init__(node, POISON_TICKS, EffectType.GROW)

    def effect(self, amount):
        return amount * -1


class Raged(AbstractEffect):

    def __init__(self, node):
        super().__init__(node, RAGE_TICKS, EffectType.EXPEL)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
        