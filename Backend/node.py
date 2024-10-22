from abstractEffect import AbstractSpreadingEffect
from jsonable import JsonableTracked
from constants import (
    NODE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_NAMES,
    EFFECT_NAMES,
    BLACK,
)
from nodeState import (
    DefaultState,
    MineState,
    StartingCapitalState,
    ZombieState,
    CapitalState,
    CannonState,
    PumpState,
)
from nodeEffect import Poisoned, Enraged, OverGrown, Zombified
from effectEnums import EffectType
from tracking_decorator.track_changes import track_changes
from method_mulitplier import method_multipliers
from end_game_methods import stall, freeAttack, shrink
from playerStateEnums import PlayerStateEnum as PSE


@track_changes("owner", "state", "value", "effects")
@method_multipliers({("lost_amount", freeAttack)})
class Node(JsonableTracked):
    def __init__(
        self, id, pos, growth_rate, transfer_rate, default_full_size, structures_grow
    ):
        self.value: float = 0
        self.owner = None
        self.item_type = NODE
        self.edges = set()
        self.pos = pos
        self.type = NODE
        self.effects: dict[str, AbstractSpreadingEffect] = dict()
        self.expel_multiplier = 1
        self.intake_multiplier = 1
        self.grow_maximum = 1
        self.grow_multiplier = 1
        self.growth_rate = growth_rate
        self.transfer_rate = transfer_rate
        self.default_full_size = default_full_size
        self.structure_grow = structures_grow

        start_values = {"pos", "state", "value"}
        full_values = {"state", "value", "effects", "owner"}
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
        if effect_name == "poison":
            originator, length = data
            return Poisoned(originator, length)
        elif effect_name == "rage":
            return Enraged()
        elif effect_name == "over_grow":
            return OverGrown()
        elif effect_name == "zombified":
            length = data
            return Zombified()
        else:
            return None

    def calculate_interactions(self):
        inter_grow, inter_grow_cap, inter_intake, inter_expel = 1, 1, 1, 1
        for effect in self.effects.values():
            if effect.effect_type == EffectType.GROW:
                inter_grow *= effect.effect(inter_grow)
            elif effect.effect_type == EffectType.GROW_CAP:
                inter_grow_cap *= effect.effect(inter_grow_cap)
            elif effect.effect_type == EffectType.INTAKE:
                inter_intake *= effect.effect(inter_intake)
            elif effect.effect_type == EffectType.EXPEL:
                inter_expel *= effect.effect(inter_expel)
        self.grow_maximum = inter_grow_cap
        self.grow_multiplier = inter_grow
        self.intake_multiplier = inter_intake
        self.expel_multiplier = inter_expel

    def set_default_state(self):
        self.set_state("default")

    def bridge_access(self):
        pass

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if self.owner.auto_attack:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and self.owner.auto_spread and not edge.popped:
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
        if self.value - 10 < self.full_size or self.grow_multiplier < 0:
            self.value = min(self.value + self.grow(), self.full_size)
        self.effects_update(lambda effect: effect.count())

    def grow(self):
        return self.state.grow()

    def effects_update(self, condition_func):
        experimental_length = len(self.effects)
        self.effects = {
            key: effect
            for key, effect in self.effects.items()
            if condition_func(effect)
        }
        if len(self.effects) < experimental_length:
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
        return self.state.lost_amount(amount, contested)

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
        if self.owner:
            self.owner.capture_event(self, False)
        self.value = self.state.capture_event()
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()
        self.effects_update(lambda effect: effect.capture_removal(player))
        player.capture_event(self, True)

    def absorbing(self):
        for edge in self.incoming:
            if edge.flowing:
                return True
        return False

    def acceptBridge(self):
        return self.state.acceptBridge

    def valid_left_click(self, clicker):
        return self.owner == clicker or clicker in {n.owner for n in self.neighbors}

    def valid_right_click(self, clicker):
        return self.owner == clicker or clicker in {n.owner for n in self.neighbors}

    def suck(self, player):
        for edge in self.incoming:
            if edge.controlled_by(player):
                edge.manual_switch(True)

        for edge in self.outgoing:
            if edge.dynamic and edge.owned_by(player):
                edge.click_swap()

    def stop_suck(self, player):
        for edge in self.incoming:
            if edge.controlled_by(player):
                edge.manual_switch(False)

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
    def reachable(self):
        visited = set()
        res = 0

        def dfs(node):
            nonlocal res
            if node in visited:
                return
            visited.add(node)
            res += 1
            for edge in node.possible_outgoing:
                dfs(edge.opposite(node))

        dfs(self)
        return res

    @property
    def possible_outgoing(self):
        return {edge for edge in self.edges if edge.from_node == self or edge.dynamic}

    @property
    def to_output_load(self):
        return len({edge for edge in self.outgoing if edge.on and not edge.flowing})

    @property
    def outputting_load(self):
        return len({edge for edge in self.outgoing if edge.on and edge.flowing})

    def extended_neighbors(self, range=3):
        nei_set = set()
        for neigh in self.neighbors:
            nei_set.add(neigh)
            if range > 1:
                nei_set.update(neigh.extended_neighbors(range - 1))
        return nei_set

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    def neighbors_(self, direction):
        return [edge.opposite(self) for edge in getattr(self, direction)]

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK

    @property
    def effect_keys(self):
        return self.effects.keys()
