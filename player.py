class Player:

    def __init__(self, color, id):
        self.score = 2000
        self.begun = False
        self.color = color
        self.id = id
        self.autoplay = True

    def buy_node(self, node):
        if self.score >= 1000:
            self.score -= 1000
            node.owner = self
            node.check_edge_stati()
            return True
        return False

    def switch_autoplay(self):
        self.autoplay = not self.autoplay