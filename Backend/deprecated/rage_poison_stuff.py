from constants import RAGE_TICKS
from abc import abstractmethod
from abstractEffect import AbstractEffect

class AbstractPlayerEffect(AbstractEffect):

    @abstractmethod
    def spread(self, node):
        pass

class PlayerEnraged(AbstractPlayerEffect):

    def __init__(self):
        super().__init__(RAGE_TICKS)

    def spread(self, node):
        node.set_state('rage')

def make_rage(rage):
    def rage_effect(data, player):
        rage(player, 'rage')
        player.effects.add(PlayerEnraged())
    return rage_effect


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

def effects_update(self):

    removed_effects = self.effects_tick()

    if removed_effects:
        self.calculate_interactions()

    self.spread_effects()

def spread_effects(self):
    for key, effect in self.effects.items():
        if effect.can_spread_func(effect):
            for edge in self.edges:
                neighbor = edge.opposite(self)
                if key not in neighbor.effects and effect.spread_criteria_func(edge, neighbor):
                    neighbor.set_state(key)



def spread_poison(self):
    for edge in self.outgoing:
        if (
            edge.to_node != self
            and edge.on
            and not edge.contested
            and edge.to_node.state_name == "default"
        ):
            edge.to_node.set_state("poison")