## effects-methods for whether effect can spread at all (can_spread)
def no_spread(effect):
    return False

def single_spread(delay):
    def spread(effect):
        return effect.counter == effect.length - delay
    return spread

## effects-methods for whether effect can spread to a specific node (spread)
def standard_outFlowing_sameOwner(edge, node):
    return edge.on and edge.to_node == node and \
        (not edge.contested) and edge.to_node.state_name == "default"
