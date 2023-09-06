from edge import Edge

class DynamicEdge(Edge):
    def __init__(self, node1, node2, id):
        super().__init__(node1, node2, id)

    def update_nodes(self):
        self.to_node.outgoing.append(self)
        self.from_node.incoming.append(self)
        self.to_node.incoming.append(self)
        self.from_node.outgoing.append(self)

    def swap_direction(self):
        temp = self.to_node
        self.to_node = self.from_node
        self.from_node = temp

    def click(self, clicker, button):
        super().click(clicker, button)
        if button == 3:
            if not self.contested and self.to_node.owner == clicker or self.from_node.owner == clicker:
                self.swap_direction()

    def check_status(self):
        self.owned = False
        self.contested = False
        if self.to_node.owner == None or self.from_node.owner == None:
            if self.from_node.owner is None:
                self.swap_direction()
            return
        elif self.to_node.owner == self.from_node.owner:
            self.owned = True
        else:
            self.contested = True

    def update(self):
        super().update()
        if self.contested:
            if self.to_node.value > self.from_node.value:
                self.swap_direction()
    


    