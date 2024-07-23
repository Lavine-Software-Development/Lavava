from jsonable import JsonableSkeleton
from constants import (
    GROWTH_RATE,
    MINIMUM_TRANSFER_VALUE,
    STANDARD_SHRINK_SPEED,
    MINE_DICT,
    GROWTH_STOP,
    GREY,
    TRANSFER_RATE,
    STANDARD_SWAP_STATUS,
    BELOW_SWAP_STATUS,
    ZOMBIE_FULL_SIZE,
    CAPITAL_FULL_SIZE,
)
from abc import abstractmethod
import math


class AbstractState(JsonableSkeleton):
    def __init__(self, node, reset_on_capture, flow_ownership, update_on_new_owner, visual_id):
        self.node = node
        self.id = node.id
        self.reset_on_capture = reset_on_capture
        self.flow_ownership = flow_ownership
        self.update_on_new_owner = update_on_new_owner
        self.acceptBridge = True
        self.swap_status = STANDARD_SWAP_STATUS
        self.visual_id = visual_id

    def grow(self):
        change = GROWTH_RATE * self.node.grow_multiplier
        if self.can_grow(change):
            return change
        return 0
    
    def can_grow(self, change):
        return 0 < self.node.value + change < self.full_size

    @abstractmethod
    def intake(self, amount, incoming_player):
        pass

    def accept_intake(self, incoming_player):
        return self.node.value < self.full_size or self.contested(incoming_player)

    def expel(self):
        return TRANSFER_RATE * self.node.expel_multiplier * self.node.value

    @abstractmethod
    def capture_event(self):
        pass

    @abstractmethod
    def killed(self):
        pass

    def size_factor(self, value):
        if value < 5:
            return 0
        return max(math.log10(value / 10) / 2 + value / 1000 + 0.15, 0)
    
    def contested(self, incoming_player):
        return incoming_player != self.node.owner
    
    @property
    def json_repr(self):
        return self.visual_id

    @property
    def full_size(self):
        return GROWTH_STOP

class DefaultState(AbstractState):
    def __init__(self, node):
        super().__init__(node, False, False, False, 0)

    def intake(self, amount, incoming_player):
        change = amount * self.node.intake_multiplier
        if self.contested(incoming_player):
            change *= -1
        return change

    def capture_event(self):
        return self.node.value * -1

    def killed(self):
        return self.node.value < 0


class ZombieState(DefaultState):

    def __init__(self, node):
        node.capture(None)
        AbstractState.__init__(self, node, True, False, False, 1) # default on capture
        self.node.value = ZOMBIE_FULL_SIZE

    def grow(self):
        return 0

    def intake(self, amount, incoming_player):
        return super().intake(amount, incoming_player) / 2
    

class CannonState(DefaultState):
    
    def __init__(self, node):
        AbstractState.__init__(self, node, True, False, False, 5) # stays on capture

    def grow(self):
        return 0

class PumpState(DefaultState):

    def __init__(self, node):
        AbstractState.__init__(self, node, True, False, False, 6) # stays on capture
        self.prep_shrink()

    def prep_shrink(self):
        self.draining = False
        self.shrink_count = math.floor(
            (GROWTH_STOP - MINIMUM_TRANSFER_VALUE) / abs(STANDARD_SHRINK_SPEED)
        )

    def grow(self):
        if self.draining:
            return self.drain()
        return 0
    
    def drain(self):
        if self.shrink_count == 0:
            self.prep_shrink()
            return 0
        self.shrink_count -= 1
        return STANDARD_SHRINK_SPEED


class CapitalState(DefaultState):
    def __init__(self, node, reset=True, update_on_new_owner=False):
        AbstractState.__init__(self, node, reset, False, update_on_new_owner, 2) # default on capture
        self.capitalized = False
        self.acceptBridge = False
        self.shrink_count = math.floor(
            (GROWTH_STOP - MINIMUM_TRANSFER_VALUE) / abs(STANDARD_SHRINK_SPEED)
        )

    def grow(self):
        if not self.capitalized:
            return self.shrink()
        return 0

    def shrink(self):
        if self.shrink_count == 0:
            self.capitalized = True
            return 0
        self.shrink_count -= 1
        return STANDARD_SHRINK_SPEED
    
    def accept_intake(self, incoming_player):
        return self.capitalized and super().accept_intake(incoming_player)
    
    @property
    def full_size(self):
        return CAPITAL_FULL_SIZE


class StartingCapitalState(CapitalState): # stays on capture
    def __init__(self, node, is_owned=False):
        super().__init__(node, False, True)
        self.capitalized = True
        self.is_owned = is_owned

    def grow(self):
        return 0


class MineState(AbstractState): # default on capture
    def __init__(self, node, absorbing_func, island):
        node.port_count = 3
        self.bonus, self.bubble, self.ring_color, visual_id = MINE_DICT[island]
        super().__init__(node, True, True, False, visual_id)
        self.absorbing_func = absorbing_func
        self.swap_status = BELOW_SWAP_STATUS

    def grow(self):
        return 0

    def intake(self, amount, incoming_player):
        return amount * self.node.intake_multiplier

    def accept_intake(self, incoming_player):
        return not self.contested(incoming_player) or not self.absorbing_func()

    def killed(self):
        return self.node.value >= self.bubble

    def capture_event(self):
        return MINIMUM_TRANSFER_VALUE

    def size_factor(self, value):
        return super().size_factor(self.bubble) / 2

    @property
    def color(self):
        return GREY

    @property
    def full_size(self):
        return self.bubble
