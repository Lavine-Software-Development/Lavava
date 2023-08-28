from map_builder import MapBuilder
from player import Player

class Game:
    def __init__(self, game_size=2):
        self.game_size = game_size
        self.connections = []
        self.graph = MapBuilder()

    def add_player(self, conn):
        self.connections.append(conn)

    def is_ready(self):
        return len(self.connections) == self.game_size