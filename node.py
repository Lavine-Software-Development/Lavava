GROWTH_RATE = 0.1
TRANSFER_RATE = 0.02
ATTACK_LOSS = 0.25
BLACK = (0, 0, 0)

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.pressed = False
        self.threaten_score = 0
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.pressed = False

    def __str__(self):
        return str(self.id)

    def grow(self):
        self.value += GROWTH_RATE
        self.owner.score += GROWTH_RATE

    def click(self, clicker, press):
        self.clicker = clicker
        if self.owner == None:
            if self.expand():
                return True
            else:
                return clicker.buy_node(self)
        elif self.owner == clicker:
            self.pressed = press
        elif self.owner != clicker:
            return self.capture()
        return False

    def absorb(self):
        for edge in self.incoming:
            if edge.owned and edge.flowing:
                self.share(edge)

    def expel(self):
        transfer_amount = self.value * TRANSFER_RATE * -1
        for edge in self.outgoing:
            if edge.owned and edge.flowing:
                self.transfer(self.neighbor(edge), transfer_amount)

    def neighbor(self, edge):
        return edge.opposing_nodes[self.id]

    def expand(self):
        success = False
        for edge in self.incoming:
            if self.neighbor(edge).owner == self.clicker:
                edge.owned = True
                success = True
                self.share(edge)
        
        if success:
            self.own()

        return success

    def own(self):
        self.owner = self.clicker
        self.check_edge_stati()

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def capture(self):
        if self.threatened:
            self.attack_loss()
            self.own()
            self.value = 1
            self.pressed = 1

    def attack_loss(self):
        threatened_difference = 1 - self.value / self.threaten_score
        for edge in self.incoming:
            if edge.flowing and edge.contested:
                self.neighbor(edge).value *= threatened_difference

    def calculate_threatened_score(self):
        score = 0
        for edge in self.incoming:
            if edge.flowing and edge.contested:
                score += self.neighbor(edge).value
        self.threaten_score = score

    def share(self, edge):
        neighbor = self.neighbor(edge)
        transfer_amount = neighbor.value * TRANSFER_RATE
        self.transfer(neighbor, transfer_amount)

    def transfer(self, neighbor, amount):
        self.value += amount
        neighbor.value -= amount

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK

    @property
    def threatened(self):
        return self.threaten_score > self.value

        
        
