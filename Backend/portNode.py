from nodeEffect import Burning
from node import Node
from constants import PORT_NODE
from tracking_decorator.track_changes import track_changes

@track_changes('is_port')
class PortNode(Node):
    def __init__(self, id, pos):

        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.is_port = False

        self.start_values = self.start_values | {'is_port'}

    def new_effect(self, effect_name, data=[]):
        if effect_name == "burn":
            if self.is_port:
                self.is_port = False
                return Burning()
        return super().new_effect(effect_name, data)