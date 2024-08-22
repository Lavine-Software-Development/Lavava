from edge import Edge
from constants import DYNAMIC_EDGE
from tracking_decorator.track_changes import track_changes

@track_changes('to_node', 'from_node')
class DynamicEdge(Edge):
    def __init__(self, node1, node2, id):

        super().__init__(node1, node2, id)

        self.dynamic = True
        self.item_type = DYNAMIC_EDGE

    def update_nodes(self):
        self.to_node.new_edge(self)
        self.from_node.new_edge(self)

    def click_swap(self):
        self.on = True
        self.swap_direction()

    def natural_swap(self):
        self.swap_direction()
        self.on = self.contested and self.from_node.owner.auto_attack

    def swap_direction(self):
        if self.dynamic:
            temp = self.to_node
            self.to_node = self.from_node
            self.from_node = temp

    def valid_right_click(self, clicker):
        return self.to_node.owner == clicker and (self.owned or self.to_node.full() or self.to_node.value > self.from_node.value)

    def check_status(self):
        if self.dynamic and self.from_node.owner is None and self.to_node.owner is not None:
            self.natural_swap()

    def update(self):
        # check to see if edge should swap on its own. This only occurs when its contested.
        # point to the node with a lower status
        # if equal status, only swap if from_node is not full and smaller than to_node*
        # note that if flowing, a slight advantage is given to from_node (momentum)
        super().update()
        if self.dynamic and self.contested:
            to_status = self.to_node.swap_status
            from_status = self.from_node.swap_status
            if from_status < to_status:
                self.natural_swap()
            elif to_status == from_status and not self.from_node.full():
                to_value = self.to_node.value
                from_value = self.from_node.value
                if self.flowing:
                    from_value *= 1.05
                if from_value < to_value:
                    self.natural_swap()

    def controlled_by(self, player):
        return super().controlled_by(player) or (
            self.to_node.owner == player and self.from_node.owner is None
        )

    def can_be_controlled_by(self, player):
        return self.to_node.owner == player
