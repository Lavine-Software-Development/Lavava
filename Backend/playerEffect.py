from Backend.constants import RAGE_TICKS
from Backend.abstractEffect import AbstractPlayerEffect

class PlayerEnraged(AbstractPlayerEffect):

    def __init__(self):
        super().__init__(RAGE_TICKS)

    def spread(self, node):
        node.set_state('rage')