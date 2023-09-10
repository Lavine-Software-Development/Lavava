from map_builder import MapBuilder

class Game:
    def __init__(self):
        self.connections = []
        self.graph = MapBuilder()

    def add_player(self, conn):
        self.connections.append(conn)

    def restart(self):
        self.graph = MapBuilder()