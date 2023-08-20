FLOW_RATE_CHANGE = 0.01

class Edge:

    def __init__(self, to_node, from_node):
        self.to_node = to_node
        self.from_node = from_node
        self.opposing_nodes = {to_node.id: from_node, from_node.id: to_node}
        self.flow = 1
        to_node.incoming.append(self)
        from_node.outgoing.append(self)
        self.owned = False

    def widen(self):
        self.flow += FLOW_RATE_CHANGE

    def restrict(self):
        self.flow -= FLOW_RATE_CHANGE

    def lose_ownership(self):
        self.owned = False
        self.flow = 1
    