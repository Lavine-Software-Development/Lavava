from constants import *

class Edge:

    def __init__(self, to_node, from_node, id):
        self.to_node = to_node
        self.from_node = from_node
        self.id = id
        self.on = False
        self.flowing = False
        self.owned = False
        self.contested = False
        self.popped = False
        self.update_nodes()

    def update_nodes(self):
        self.to_node.incoming.append(self)
        self.from_node.outgoing.append(self)

    def click(self, clicker, button):
        if button == 1 and self.owned_by(clicker):
            self.switch()

    def switch(self, specified=None):
        if specified == None:
            self.on = not self.on
        else:
            self.on = specified

    def update(self):
        if self.from_node.value < MINIMUM_TRANSFER_VALUE or not self.on or (self.to_node.full and not self.contested):
            self.flowing = False
        elif self.from_node.value > BEGIN_TRANSFER_VALUE:
            self.flowing = True

        if self.flowing:
            self.flow()
            if not self.popped:
                self.pop()

    def pop(self):
        self.popped = True
        if not self.contested or not self.from_node.owner.auto_attack: 
            self.on = False

    def flow(self):
        amount_transferred = TRANSFER_RATE * self.from_node.value
        self.delivery(amount_transferred)
        self.from_node.value -= amount_transferred

    def delivery(self, amount):
        if self.to_node.owner != self.from_node.owner:
            self.to_node.value -= amount
            if self.to_node.killed():
                self.capture()
        else:
            if self.to_node.owner == None:
                self.capture()
            self.to_node.value += amount

    def capture(self):
        self.to_node.capture(self.from_node.owner)

    def check_status(self):
        self.owned = False
        self.contested = False
        if self.to_node.owner == None or self.from_node.owner == None:
            return
        elif self.to_node.owner == self.from_node.owner:
            self.owned = True
        else:
            self.contested = True

    def owned_by(self, player):
        return self.from_node.owner == player

    @property
    def duo_owned(self):
        return self.contested or self.owned

    @property
    def color(self):
        if self.on:
            if self.flowing:
                return self.from_node.color
            return self.from_node.color
        return (50, 50, 50)
    