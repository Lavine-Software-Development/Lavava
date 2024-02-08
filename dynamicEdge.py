from edge import Edge
from constants import DYNAMIC_EDGE

class DynamicEdge(Edge):
    def __init__(self, node1, node2, id):
        super().__init__(node1, node2, id)
        self.state = 'two-way'
        self.item_type = DYNAMIC_EDGE

    def update_nodes(self):
        self.to_node.new_edge(self, 'incoming')
        self.from_node.new_edge(self, 'outgoing')
        self.to_node.new_edge(self, 'outgoing')
        self.from_node.new_edge(self, 'incoming')

    def click_swap(self):
        self.on = True
        self.swap_direction()

    def natural_swap(self):
        self.on = False
        self.swap_direction()

    def swap_direction(self):
        if self.state == 'two-way':
            temp = self.to_node
            self.to_node = self.from_node
            self.from_node = temp

    def click(self, clicker, button):
        super().click(clicker, button)
        if button == 3:
            if not self.contested and (self.to_node.owner == clicker or self.from_node.owner == clicker):
                self.click_swap()

    def check_status(self):
        if self.from_node.owner is None and self.to_node.owner != None:
            self.natural_swap()

    def update(self):
        # check to see if edge should swap on its own. This only occurs when its contested
        # point to the node with a lower status
        # if equal status, point to the node with a lower value
        super().update()
        if self.contested:
            to_status = self.to_node.swap_status
            from_status = self.from_node.swap_status
            if from_status < to_status:
                self.natural_swap()
            elif to_status == from_status and self.from_node.value < self.to_node.value:
                self.natural_swap()

    def freeze(self):
        self.state = 'one-way'

    def controlled_by(self, player):
        return super().controlled_by(player) or (self.to_node.owner == player and self.from_node.owner is None)

    def can_be_controlled_by(self, player):
        return self.to_node.owner == player or self.to_node.owner == player
    


    