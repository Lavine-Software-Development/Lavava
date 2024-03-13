import json
import random
from game import ServerGame

class Batch:
    def __init__(self, count, mode, conn):
        self.connections = [conn]
        self.player_count = count
        self.mode = mode

    def add_player(self, conn):
        self.connections.append(conn)

    def build(self):
        self.game = ServerGame(self.player_count, self.mode)
        self.seed = random.randint(0, 10000)

    def is_ready(self):
        return len(self.connections) == self.player_count

    def repr(self, player) -> str:
        game_dict = self.game.start_json()
        game_dict["player_id"] = player
        return json.dumps(game_dict)
