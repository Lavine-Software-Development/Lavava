FLOW_RATE_CHANGE = 0.01

class Edge:

    def __init__(self, node1, node2):
        self.nodes = (node1, node2)
        self.opposing_nodes = {node1.id: node2, node2.id: node1}
        self.flow = 1
        # node1.neighbors.append(self)
        # node2.neighbors.append(self)
        self.owned = False

    def widen(self):
        self.flow += FLOW_RATE_CHANGE

    def restrict(self):
        self.flow -= FLOW_RATE_CHANGE

    def lose_ownership(self):
        self.owned = False
        self.flow = 1
    