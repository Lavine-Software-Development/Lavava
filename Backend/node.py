from abstractEffect import AbstractSpreadingEffect
from jsonable import JsonableTracked
from constants import (
    NODE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_NAMES,
    EFFECT_NAMES,
    AUTO_ATTACK,
    AUTO_EXPAND,
    BLACK,
)
from nodeState import DefaultState, MineState, StartingCapitalState, ZombieState, CapitalState, CannonState, PumpState
from nodeEffect import Poisoned, Enraged
from effectEnums import EffectType
from tracking_decorator.track_changes import track_changes
from method_mulitplier import method_multipliers
from end_game_methods import stall, freeAttack, shrink
from playerStateEnums import PlayerStateEnum as PSE


@track_changes('owner', 'state', 'value', 'effects')
@method_multipliers({('lost_amount', freeAttack)})
class Node(JsonableTracked):

    def __init__(self, id, pos):

        self.value: float = 0
        self.owner = None
        self.item_type = NODE
        self.edges = set()
        self.pos = pos
        self.type = NODE
        self.effects: dict[str, AbstractSpreadingEffect] = dict()
        self.expel_multiplier = 1
        self.intake_multiplier = 1
        self.grow_multiplier = 1

        start_values = {'pos', 'state', 'value'}
        full_values = {'state', 'value', 'effects', 'owner'}
        super().__init__(id, start_values, set(), full_values)

        self.set_default_state()
        self.updated = False

    def __str__(self):
        return str(self.id)

    def new_edge(self, edge):
        self.edges.add(edge)

    def set_state(self, status_name, data=None):
        if status_name in STATE_NAMES:
            self.state = self.new_state(status_name, data)
            self.state_name = status_name
        elif status_name in EFFECT_NAMES:
            if new_effect := self.new_effect(status_name, data):
                self.effects = self.effects | {status_name: new_effect}
        self.calculate_interactions()

    def new_state(self, state_name, data=None):
        self.updated = True
        if state_name == "default":
            return DefaultState(self)
        elif state_name == "mine":
            # if data is True and mode.MODE == 3:
            return MineState(self, self.absorbing, data)
        elif state_name == "zombie":
            return ZombieState(self)
        elif state_name == "capital":
            if data:
                return StartingCapitalState(self)
            return CapitalState(self)
        elif state_name == "cannon":
            return CannonState(self)
        elif state_name == "pump":
            return PumpState(self)
        else:
            return DefaultState(self)

    def new_effect(self, effect_name, data=[]):
        if effect_name == 'poison':
            originator, length = data
            return Poisoned(originator, length)
        elif effect_name == 'rage':
            return Enraged()
        else:
            return None

    def calculate_interactions(self):
        inter_grow, inter_intake, inter_expel = 1, 1, 1
        for effect in self.effects.values():
            if effect.effect_type == EffectType.GROW:
                inter_grow *= effect.effect(inter_grow)
            elif effect.effect_type == EffectType.INTAKE:
                inter_intake *= effect.effect(inter_intake)
            elif effect.effect_type == EffectType.EXPEL:
                inter_expel *= effect.effect(inter_expel)
        self.grow_multiplier = inter_grow
        self.intake_multiplier = inter_intake
        self.expel_multiplier = inter_expel

    def set_default_state(self):
        self.set_state("default")

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if AUTO_ATTACK:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and AUTO_EXPAND and not edge.popped:
                edge.switch(True)

    def check_edge_stati(self):
        for edge in self.edges:
            edge.check_status()

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)
        
    def owned_and_alive(self):
        return self.owner is not None and self.owner.ps.value < PSE.ELIMINATED.value

    def tick(self):
        self.value = min(self.value + self.grow(), self.full_size)
        self.effects_update(lambda effect: effect.count())

    def grow(self):
        return self.state.grow()

    def effects_update(self, condition_func):
        original_length = len(self.effects)
        self.effects = {key: effect for key, effect in self.effects.items() if condition_func(effect)}
        if len(self.effects) < original_length:
            self.calculate_interactions()

    def delivery(self, amount, player):
        self.value += self.state.intake(amount, player)
        return self.delivery_status_update(player)
        
    def delivery_status_update(self, player):
        if self.state.flow_ownership:
            self.owner = player
        if self.state.killed():
            self.capture(player)
            return True
        return False

    def send_amount(self):
        return self.state.expel()
    
    def lost_amount(self, amount, contested):
        return amount

    def update_ownerships(self, player=None):
        if self.owner is not None and self.owner != player:
            self.owner.count -= 1
            if self.owner.count == 0:
                self.owner.killed_event(player)
        if player is not None:
            player.count += 1
        self.owner = player
        if self.state.update_on_new_owner:
            self.updated = True

    def capture(self, player):
        self.value = self.state.capture_event()
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()
        self.effects_update(lambda effect: effect.capture_removal(player))

    def absorbing(self):
        for edge in self.incoming:
            if edge.flowing:
                return True
        return False

    def acceptBridge(self):
        return self.state.acceptBridge

    @property
    def swap_status(self):
        return self.state.swap_status

    def full(self):
        return self.value >= self.full_size
    
    @property
    def full_size(self):
        return self.state.full_size
    
    @property
    def incoming(self):
        return {edge for edge in self.edges if edge.to_node == self}
    
    @property
    def outgoing(self):
        return {edge for edge in self.edges if edge.from_node == self}

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK
    
    @property
    def effect_keys(self):
        return self.effects.keys()

    
