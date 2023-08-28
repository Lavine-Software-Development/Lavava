TRANSFER_RATE = 0.02

class Edge:

    def __init__(self, to_node, from_node, id, directed=True):
        self.directed = directed
        self.to_node = to_node
        self.from_node = from_node
        self.id = id
        self.opposing_nodes = {to_node.id: from_node, from_node.id: to_node}
        self.flowing = True
        to_node.incoming.append(self)
        from_node.outgoing.append(self)
        if not directed:
            from_node.incoming.append(self)
            to_node.outgoing.append(self)
        self.owned = False
        self.contested = False
        self.pressed = False

    def lose_ownership(self):
        self.owned = False
        self.flowing = True

    def click(self, clicker, press):
        if press == 1 and clicker == self.owner:
            self.pressed = True
            return (True, True)
        elif press == 3 and clicker == self.directional_owner:
            self.change_flow()
            return (True, False)
        return (False, False)

    def flow(self):
        if self.directed:
            amount_transferred = self.from_node.value * TRANSFER_RATE
            self.to_node.value += amount_transferred
            self.from_node.value -= amount_transferred

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

    @property
    def owner(self):
        if self.owned:
            return self.to_node.owner
        return None

    @property
    def directional_owner(self):
        if self.directed:
            return self.to_node.owner
        return None
    