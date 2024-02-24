from constants import (
    BURN_TICKS,
    POISON_TICKS,
    RAGE_TICKS,
    RAGE_MULTIPLIER,
    POISON_SPREAD_DELAY,
)
from effectEnums import EffectType
from abstractEffect import AbstractNodeEffect


class Burning(AbstractNodeEffect):
    def __init__(self, lose_ports):
        super().__init__(BURN_TICKS, EffectType.NONE)
        self.lose_ports_func = lose_ports

    def complete(self):
        self.lose_ports_func()


class Poisoned(AbstractNodeEffect):
    def __init__(self, spread_poison):
        super().__init__(POISON_TICKS, EffectType.GROW)
        self.spread_poison = spread_poison

    def effect(self, amount):
        return amount * -1

    def count(self):
        if self.counter == POISON_SPREAD_DELAY:
            self.spread_poison()
        return super().count()
    
    def spread_poison(self):
        


class NodeEnraged(AbstractNodeEffect):
    def __init__(self):
        super().__init__(RAGE_TICKS, EffectType.EXPEL)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
