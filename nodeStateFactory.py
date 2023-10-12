from nodeState import *

class StateFactory:

    @staticmethod
    def create_state(state_name, node):
        if state_name == 'default':
            state = DefaultState(node.value, node.owner)
        elif state_name == "poisoned":
            state = PoisonedState(node.value, node.owner)
            state.on("spread_poison", node.spread_poison)
        elif state_name == "mine":
            state = MineState()
        elif state_name == "capital":
            state = CapitalState(node.value, node.owner)

        state.on('capture', node.capture)
        return state