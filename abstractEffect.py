from abc import ABC, abstractmethod

class AbstractEffect(ABC):

    def __init__(self, expiry_time):
        self.length = expiry_time
        self.counter = expiry_time

    def count(self):
        self.counter -= 1
        return self.counter > 0

    def complete(self):
        pass


class AbstractNodeEffect(AbstractEffect):

    def __init__(self, expiry_time, effect_type):
        super().__init__(expiry_time)
        self.effect_type = effect_type

    @abstractmethod
    def can_spread(self):
        pass


class SpreadingNodeEffect(AbstractNodeEffect):

    def __init__(self, expiry_time, effect_type, spread_criteria, spread_delay):
        super().__init__(expiry_time, effect_type)
        self.spread_delay = spread_delay
        self.spread_criteria = spread_criteria

    def can_spread(self):
        return self.counter == self.length - self.spread_delay
    

class BenignNodeEffect(AbstractNodeEffect):

    def __init__(self, expiry_time, effect_type):
        super().__init__(expiry_time, effect_type)

    def can_spread(self):
        return False


class AbstractPlayerEffect(AbstractEffect):

    @abstractmethod
    def spread(self, node):
        pass