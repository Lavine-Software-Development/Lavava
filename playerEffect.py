from constants import RAGE_TICKS
from abstractEffect import AbstractPlayerEffect

class PlayerEnraged(AbstractPlayerEffect):

    def __init__(self):
        super().__init__(RAGE_TICKS)

    def spread(self, node):
        node.set_state('rage')
        for edge in node.outgoing:
            edge.effects.add('rage')