from constants import (
    BURN_TICKS,
)
from effectEnums import EffectType
from abstractEffect import AbstractNodeEffect
from effect_spreaders import no_spread

class Burning(AbstractNodeEffect):
    def __init__(self, lose_ports):
        super().__init__(BURN_TICKS, EffectType.NONE, no_spread)
        self.lose_ports_func = lose_ports

    def complete(self):
        self.lose_ports_func()
