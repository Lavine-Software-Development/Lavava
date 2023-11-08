from nodeState import *
from constants import MODE, PORT_NODE_START_PORTS, CONTEXT

def set_node_state(self, state_name, data=None):
    if state_name == 'default':
        return DefaultState(self)
    elif state_name == "poisoned":
        return PoisonedState(self)
    elif state_name == "capital":
        CapitalStateType = MODE['capital']
        return CapitalStateType(self)
    elif state_name == "mine":
        if data == True and CONTEXT['mode'] == 3:
            self.port_count = PORT_NODE_START_PORTS
        return MineState(self, data)
    
