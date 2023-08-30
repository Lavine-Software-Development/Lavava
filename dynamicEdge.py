from edge import Edge

class DynamicEdge(Edge):
    def __init__(self, node1, node2, id, directed=True):
        super().__init__(node1, node2, id, directed)
        self.nodes = [node1, node2]

        self.update_nodes()

    def update_nodes(self):
        del self.from_node
        del self.to_node
        self.nodes[0].outgoing.append(self)
        self.nodes[1].incoming.append(self)

    def owned_by(self, player):
        

    