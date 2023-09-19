from map_builder import MapBuilder
import random

class Game:
    def __init__(self, count, code, conn):
        self.connections = [conn]
        self.game_code = code
        self.player_count = count

    def add_player(self, conn):
        self.connections.append(conn)

    def build(self):
        self.seed = random.randint(0, 10000)
        
    def is_ready(self):
        return len(self.connections) == self.player_count

    def repr(self, player) -> str:
        return f"{player},{self.player_count},{self.seed}"