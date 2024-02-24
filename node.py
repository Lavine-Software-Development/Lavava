from constants import (
    NODE,
    PORT_NODE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_NAMES,
    EFFECT_NAMES,
    AUTO_ATTACK,
    AUTO_EXPAND,
    CONTEXT,
    BLACK,
    BROWN,
)
from nodeState import DefaultState, MineState
from nodeEffect import EffectType, Poisoned, NodeEnraged, Burning
import mode

class Node:
    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.item_type = NODE
        self.incoming = set()
        self.outgoing = set()
        self.id = id
        self.pos = pos
        self.type = NODE
        self.effects = {}
        self.expel_multiplier = 1
        self.intake_multiplier = 1
        self.grow_multiplier = 1
        self.set_default_state()

    def __str__(self):
        return str(self.id)

    def new_edge(self, edge, dir):
        if dir == "incoming":
            self.incoming.add(edge)
        else:
            self.outgoing.add(edge)

    def set_state(self, status_name, data=None):
        if status_name in STATE_NAMES:
            self.state = self.new_state(status_name, data)
            self.state_name = status_name
        elif status_name in EFFECT_NAMES:
            self.effects[status_name] = self.new_effect(status_name)
        self.calculate_interactions()

    def new_state(self, state_name, data=None):
        if state_name == "default":
            return DefaultState(self.id)
        elif state_name == "mine":
            if data is True and mode.MODE == 3:
                self.port_count = 3
            return MineState(self.id, self.absorbing, data)
        elif state_name == "capital":
            from modeConstants import CAPITAL_TYPES
            CapitalStateType = CAPITAL_TYPES[mode.MODE]
            if self.owner:
                self.owner.capital_handover(self)
            return CapitalStateType(self.id)
        else:
            return DefaultState(self.id)


    def new_effect(self, effect_name):
        if effect_name == 'poison':
            return Poisoned(self.spread_poison)
        elif effect_name == 'rage':
            return NodeEnraged()

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
        print(self.grow_multiplier, self.intake_multiplier, self.expel_multiplier)

    def set_default_state(self):
        self.set_state("default")

    def click(self, clicker, button):
        if button == 1:
            self.left_click(clicker)
        elif button == 3:
            self.right_click()

    def right_click(self):
        pass

    def left_click(self, clicker):
        if self.owner is None:
            if clicker.buy_node():
                self.capture(clicker)

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if AUTO_ATTACK:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and AUTO_EXPAND:
                edge.switch(True)
                edge.popped = False

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)

    def owned_and_alive(self):
        return self.owner is not None and not self.owner.eliminated

    def spread_poison(self):
        for edge in self.outgoing:
            if (
                edge.to_node != self
                and edge.on
                and not edge.contested
                and edge.to_node.state_name == "default"
            ):
                edge.to_node.set_state("poison")

    def grow(self):
        if self.state.can_grow(self.value):
            self.value += self.state.grow(self.grow_multiplier)
        self.effects_update()

    def effects_update(self):

        removed_effects = self.effects_tick()

        if removed_effects:
            self.calculate_interactions()

        self.spread_effects()
    
    def effects_tick(self):
        effects_to_remove = [key for key, effect in self.effects.items() if not effect.count()]
        for key in effects_to_remove:
            self.effects[key].complete()
        for key in effects_to_remove:
            del self.effects[key]

        return effects_to_remove

    def spread_effects(self):
        for key, effect in self.effects.items():
            if effect.can_spread_func(effect):
                print("spread at: ", effect.counter)
                for edge in self.edges:
                    neighbor = edge.opposite(self)
                    if key not in neighbor.effects and effect.spread_criteria_func(edge, neighbor):
                        neighbor.set_state(key)

    def delivery(self, amount, player):
        self.value += self.state.intake(
            amount, self.intake_multiplier, player != self.owner
        )
        if self.state.flow_ownership:
            self.owner = player
        if self.state.killed(self.value):
            self.capture(player)

    def accept_delivery(self, player):
        return self.state.accept_intake(player != self.owner, self.value)

    def send_amount(self):
        return self.state.expel(self.expel_multiplier, self.value)

    def update_ownerships(self, player):
        if self.owner is not None and self.owner != player:
            self.owner.count -= 1
        player.count += 1
        self.owner = player
        player.pass_on_effects(self)

    def capture(self, player):
        self.value = self.state.capture_event(player)(self.value)
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()

    def absorbing(self):
        for edge in self.current_incoming:
            if edge.flowing:
                return True
        return False

    def acceptBridge(self):
        return self.state.acceptBridge

    @property
    def swap_status(self):
        return self.state.swap_status

    @property
    def full(self):
        return self.value >= self.state.full_size

    @property
    def edges(self):
        return self.incoming | self.outgoing

    @property
    def current_incoming(self):
        return [edge for edge in self.incoming if edge.to_node == self]

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    @property
    def size(self):
        return int(5 + self.state.size_factor(self.value) * 18)

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK


class PortNode(Node):
    def __init__(self, id, pos, port_count):
        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.port_count = port_count

    @property
    def is_port(self):
        return self.port_count != 0

    def new_effect(self, effect_name):
        if effect_name == 'burn':
            return Burning(self.lose_ports)
        else:
            return super().new_effect(effect_name)

    def acceptBridge(self):
        return self.port_count > 0 and 'burn' not in self.effects and self.state.acceptBridge

    def new_edge(self, edge, dir):
        if CONTEXT["started"] and edge not in self.edges and dir == "outgoing":
            self.port_count -= 1
        super().new_edge(edge, dir)

    def lose_ports(self):
        self.port_count = 0

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        elif self.is_port:
            return BROWN
        return BLACK
