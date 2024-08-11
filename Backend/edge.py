from node import Node
from jsonable import JsonableTracked
from constants import (
    EDGE,
    MINIMUM_TRANSFER_VALUE,
    BEGIN_TRANSFER_VALUE,
)
from tracking_decorator.track_changes import track_changes

@track_changes('dynamic', 'on', 'flowing_d')
class Edge(JsonableTracked):
    to_node: Node
    from_node: Node

    def __init__(self, to_node, from_node, id):
        self.item_type = EDGE
        self.to_node = to_node
        self.from_node = from_node
        self.on = False
        self.flowing = False
        self.popped = False
        self.update_nodes()
        self.dynamic = False
        self.type = EDGE

        start_values = {'to_node', 'from_node', 'dynamic', 'on', 'flowing'}
        full_values = start_values
        super().__init__(id, start_values, set(), full_values)

    def __str__(self):
        return str(self.id)

    def update_nodes(self):
        self.to_node.new_edge(self)
        self.from_node.new_edge(self)

    def valid_left_click(self, clicker):
        return self.controlled_by(clicker)

    def valid_right_click(self, clicker):
        return False
    
    def manual_switch(self, specified=None):
        self.popped = True
        self.switch(specified)

    def switch(self, specified=None):
        if specified is None:
            self.on = not self.on
        else:
            self.on = specified
        if not self:
            self.popped = True
    
    @property
    def begin_transfer_value(self):
        return BEGIN_TRANSFER_VALUE + self.from_node.to_output_load * 2
    
    @property
    def minimum_transfer_value(self):
        return MINIMUM_TRANSFER_VALUE + self.from_node.to_output_load * 2

    def update(self):
        if (
            not self.on
            or self.from_node.value < self.minimum_transfer_value
            or not self.flow_allowed()
        ):
            self.flowing = False
        elif self.from_node.value > self.begin_transfer_value:
            self.flowing = True

        if self.flowing:
            self.flow()
            if not self.popped:
                self.pop()

    def flow_allowed(self):
        return self.to_node.state.accept_intake(self.owner)

    def pop(self):
        self.popped = True
        if not self.contested or not self.from_node.owner.auto_attack:
            self.on = False

    def flow(self):
        amount_transferred = self.from_node.send_amount()
        killed = self.to_node.delivery(amount_transferred, self.from_node.owner)
        self.from_node.value -= self.from_node.lost_amount(amount_transferred, self.contested)

        self.spread_effects(killed)

    def spread_effects(self, killed):
        for key, effect in self.from_node.effects.items():
            if key not in self.to_node.effects and effect.past_incubation and effect.can_spread(killed, self.to_node.owner):
                self.to_node.set_state(effect.spread_key(key), effect.spread())

        for key, effect in self.to_node.effects.items():
            if effect.back_spread and key not in self.from_node.effects and effect.past_incubation and effect.can_spread(False, self.from_node.owner):
                    self.from_node.set_state(effect.spread_key(key), effect.spread())

    def check_status(self):
        pass

    def controlled_by(self, player):
        return self.from_node.owner == player

    def can_be_controlled_by(self, player):
        return self.controlled_by(player)

    @property
    def owned(self):
        return self.duo_ownership and self.to_node.owner == self.from_node.owner

    @property
    def duo_ownership(self):
        return self.to_node.owner is not None and self.from_node.owner is not None

    @property
    def contested(self):
        return self.duo_ownership and self.to_node.owner != self.from_node.owner

    @property
    def owner(self):
        return self.from_node.owner

    @property
    def color(self):
        if self.on:
            if self.flowing:
                return self.from_node.color
            return self.from_node.color
        return (50, 50, 50)

    def opposite(self, node):
        if node == self.from_node:
            return self.to_node
        return self.from_node
