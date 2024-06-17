from constants import (
    RAGE_TICKS,
    RAGE_MULTIPLIER,
    POISON_SPREAD_DELAY,
)
from effectEnums import EffectType
from abstractEffect import AbstractSpreadingEffect

class Poisoned(AbstractSpreadingEffect):
    def __init__(self, originator, length):
        super().__init__(length, EffectType.GROW, POISON_SPREAD_DELAY)
        self.originator = originator
       
    def can_spread(self, killed, new_owner):
        return self.originator != new_owner

    def effect(self, amount):
        return amount * -1
    
    def spread(self):
        return (self.originator, self.length)


class NodeEnraged(AbstractSpreadingEffect):
    def __init__(self):
        super().__init__(RAGE_TICKS, EffectType.EXPEL)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
    
    def can_spread(self, killed, new_owner):
        return killed
