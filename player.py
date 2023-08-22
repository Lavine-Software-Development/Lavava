class Player:

    def __init__(self, color):
        self.score = 1000
        self.begun = False
        self.color = color

    def buy_node(self, node):
        if self.score >= 1000:
            self.score -= 1000
            node.owner = self
            node.check_edge_stati()
            return True
        return False