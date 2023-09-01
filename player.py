class Player:

    def __init__(self, color, id):
        self.money = 1000
        self.count = 0
        self.begun = False
        self.color = color
        self.id = id
        self.autoplay = True
        self.auto_attack = False

    def buy_node(self):
        if self.money >= 1000:
            self.money -= 1000
            return True
        return False

    def buy_edge(self):
        if self.money >= 500:
            self.money -= 500
            return True
        return False

    def switch_autoplay(self):
        self.autoplay = not self.autoplay