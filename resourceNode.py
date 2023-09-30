from node import Node
from constants import *
import math

class ResourceNode(Node):
    def __init__(self, id, pos, island):
        super().__init__(id, pos)

        self.state = 'resource'
        self.bubble_owner = None

        if island:
            self.bonus = ISLAND_RESOURCE_BONUS
            self.bubble = ISLAND_RESOURCE_BUBBLE
            self.ring_color = YELLOW
        else:
            self.bonus = RESOURCE_BONUS
            self.bubble = RESOURCE_BUBBLE
            self.ring_color = DARK_YELLOW

        self.bubble_size = self.bubble

    def grow(self):
        if self.normal:
            super().grow()

    def delivery(self, amount, player):
        if not self.normal:
            self.bubble_owner = player
            self.bubble_size -= amount
            if self.bubble_size <= 0:
                self.pop()
        else:
            super().delivery(amount, player)

    def pop(self):
        self.normalize()
        self.capture(self.bubble_owner)
        self.owner.tick_production += self.bonus
        self.value = self.bubble * RESOURCE_RECOUP # 1 - (18 + 5) / (2*18 + 5) = NOT USED ANYMORE

    def bubble_controlled(self, owner):
        if self.bubble_owner == None or owner == self.bubble_owner:
            return False
        for edge in self.current_incoming:
            if edge.flowing:
                return True
        return False

    def size_factor(self):
        if self.state == 'resource':
            return max(math.log10(self.bubble/10)/2+self.bubble/1000+0.15,0)/2
        else:
            if self.value<5:
                return 0
            return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)

    @property
    def color(self):
        if self.state == 'resource':
            return GREY
        return super().color
    




