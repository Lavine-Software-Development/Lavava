TRANSFER_RATE = 0.005
MINIMUM_TRANSFER_VALUE = 20
BEGIN_TRANSFER_VALUE = 50

class Edge:

    def __init__(self, to_node, from_node, id, directed=True):
        self.directed = directed
        self.to_node = to_node
        self.from_node = from_node
        self.id = id
        self.opposing_nodes = {to_node.id: from_node, from_node.id: to_node}
        self.on = False
        self.flowing = False
        self.owned = False
        self.contested = False
        self.popped = False
        self.update_nodes()

    def update_nodes(self):
        self.to_node.incoming.append(self)
        self.from_node.outgoing.append(self)
        if not self.directed:
            self.from_node.incoming.append(self)
            self.to_node.outgoing.append(self)

    def lose_ownership(self):
        self.owned = False
        self.flowing = True

    def click(self, clicker, button):
        if button == 1 and self.owned_by(clicker):
            self.switch()

    def switch(self, specified=None):
        if specified == None:
            self.on = not self.on
        else:
            self.on = specified

    def update(self):
        if self.from_node.value > BEGIN_TRANSFER_VALUE:
            self.flowing = True
        elif self.from_node.value < MINIMUM_TRANSFER_VALUE:
            self.flowing = False

        if self.on and self.sharing() and self.flowing:
            self.flow()
            if not self.popped:
                self.pop()

    def sharing(self):
        return self.from_node.status != 'absorbing' and self.to_node.status != 'expelling'

    def pop(self):
        self.popped = True
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

    def change_flow(self):
        self.flowing = not self.flowing

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
    def color(self):
        if self.on:
            if self.flowing:
                return self.from_node.color
            return self.from_node.color
        return (50, 50, 50)
    