from node import Node
from constants import PORT_NODE

class PortNode(Node):
    def __init__(self, id, pos, is_port):

        track_values = {'is_port'}

        super().__init__(id, pos, set())
        self.item_type = PORT_NODE
        self.is_port = is_port

        self.start_values = self.start_values | {'is_port'}