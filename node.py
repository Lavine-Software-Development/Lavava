GROWTH_RATE = 0.1
BLACK = (0, 0, 0)

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.status = 'neutral'
        self.hovered = False

    def __str__(self):
        return str(self.id)

    def grow(self):
        if self.value < 250:
            self.value += GROWTH_RATE
            self.owner.score += GROWTH_RATE

    def click(self, clicker, button):
        self.clicker = clicker
        if button == 1:
            self.left_click()
        elif button == 3:
            self.right_click()

    def right_click(self):
        if self.clicker == self.owner:
            if self.status == "absorbing":
                self.status = "neutral"
                self.absorb(False)
            else:
                self.status = "expelling"
                self.expel(True)

    def left_click(self):
        if self.enemy():
            self.attack()
        elif self.owner == None:
            if self.clicker.buy_node(self):
                self.capture()
        else:
            if self.status == "expelling":
                self.status = "neutral"
                self.expel(False)
            else:
                self.status = "absorbing"
                self.absorb(True)

    def attack(self):
        pass
        # self.absorb(True)

    def absorb(self, on):
        pass
        # for edge in self.incoming:
        #     if edge.owned_by(self.clicker):
        #         edge.switch(on)

    def expel(self, on):
        pass
        # for edge in self.outgoing:
        #     if not on or not edge.contested:
        #         edge.switch(on)

    def expand(self):
        for edge in self.outgoing:
            if not edge.to_node.owner:
                edge.switch(True)

    def enemy(self, player=None):
        if player == None:
            player = self.clicker
        return self.owner != None and self.owner != player

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def capture(self, clicker=None):
        if clicker is None:
            clicker = self.clicker
        self.owner = clicker
        self.check_edge_stati()
        if self.owner.autoplay:
            self.expand()

    def killed(self):
        if self.value < 0:
            self.value *= -1
            return True
        return False

    @property
    def color(self):
        if self.owner:
            if self.value >= 250:
                return self.owner.color
            return self.owner.color
        return BLACK
