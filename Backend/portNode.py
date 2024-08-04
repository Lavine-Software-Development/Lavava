from nodeEffect import Burning
from node import Node
from constants import PORT_NODE, WALL_NODE
from tracking_decorator.track_changes import track_changes
import random

@track_changes('is_port')
class PortNode(Node):
    def __init__(self, id, pos, growth_rate, transfer_rate, default_full_size):

        super().__init__(id, pos, growth_rate, transfer_rate, default_full_size)
        self.item_type = PORT_NODE
        self.is_port = False

        self.start_values = self.start_values | {'is_port'}
        self.full_values = self.full_values | {'is_port'}

    def new_effect(self, effect_name, data=[]):
        if effect_name == "burn":
            if self.is_port:
                self.is_port = False
                return Burning()
        return super().new_effect(effect_name, data)
    
    def bridge_access(self, accesibile, settings):
        self.is_port = accesibile

    def make_accessible(self):
        self.is_port = True

    @property
    def accessible(self):
        return self.is_port
    

@track_changes('wall_count')
class WallNode(Node):
    def __init__(self, id, pos, growth_rate, transfer_rate, default_full_size):

        super().__init__(id, pos, growth_rate, transfer_rate, default_full_size)
        self.item_type = WALL_NODE
        self.wall_count = 0

        self.start_values = self.start_values | {'wall_count'}
        self.full_values = self.full_values | {'wall_count'}

    def bridge_access(self, accessibile, settings):
        if not accessibile:
            self.wall_count = random.choice(settings["wall_counts"])
        print(self.wall_count)

    def make_accessible(self):
        if self.wall_count > 0:
            self.wall_count -= 1

    @property
    def accessible(self):
        return self.wall_count == 0