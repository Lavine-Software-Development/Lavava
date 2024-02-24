from abc import ABC, abstractmethod

class AbstractEffect(ABC):

    def __init__(self, expiry_time):
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


class AbstractPlayerEffect(AbstractEffect):

    @abstractmethod
    def spread(self, node):
        pass