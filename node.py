GROWTH_RATE = 0.1
TRANSFER_RATE = 0.02
ATTACK_PERCENTAGE = 0.5
BLACK = (0, 0, 0)

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.pressed = False
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos

    def __str__(self):
        return str(self.id)

    def grow(self):
        self.value += GROWTH_RATE
        self.owner.score += GROWTH_RATE

    def click(self, clicker):
        self.clicker = clicker
        if self.owner == None:
            if self.expand():
                return True
            else:
                return clicker.buy_node(self)
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
            self.owner = self.clicker

        return success

    def capture(self):
        print("Attack")
        attack_edges = []
        broken_edges = []
        attack_strength = 0

        for edge in self.incoming:
            neighbor = self.neighbor(edge)
            if neighbor.owner == self.clicker:
                attack_add_on = ATTACK_PERCENTAGE * neighbor.value
                attack_edges.append((edge, attack_add_on))
                attack_strength += attack_add_on
            elif edge.owned:
                broken_edges.append(edge)

        print("attack_strength: ", attack_strength)
        print("value: ", self.value)
        if attack_strength > self.value:
            self.handover(attack_edges, broken_edges)
            print("Attack Successful")
        else:
            print("Attack Failed")

    def handover(self, attack_edges, broken_edges):
        self.owner = self.clicker
        self.value = 0

        for attack in attack_edges:
            attack[0].owned = True
            self.transfer(self.neighbor(attack[0]), attack[1])

        for edge in broken_edges:
            edge.lose_ownership()

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

        
        
