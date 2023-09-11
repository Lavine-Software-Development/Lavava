from map_builder import MapBuilder

class Game:
    def __init__(self, count, code, conn):
        self.connections = [conn]
        self.game_code = code
        self.player_count = count

    def add_player(self, conn):
        self.connections.append(conn)

    def  build(self):
        self.graph = MapBuilder()

    def is_ready(self):
        return len(self.connections) == self.player_count