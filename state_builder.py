from nodeState import *
from constants import MODE

def set_node_state(self, state_name, data=None):
    if state_name == 'default':
        return DefaultState(self)
    elif state_name == "poisoned":
        return PoisonedState(self)
    elif state_name == "capital":
        CapitalStateType = MODE['capital']
        return CapitalStateType(self)
    elif state_name == "mine":
        return MineState(self, data)
    
