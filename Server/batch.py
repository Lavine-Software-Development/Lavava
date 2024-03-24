import json
from game_state import GameState
from game import ServerGame
import json_abilities
from json_helpers import convert_keys_to_int

class Batch:
    def __init__(self, count, mode, conn):
        self.connections = [conn]
        self.player_count = count
        self.mode = mode
        self.gs = GameState()

    def add_player(self, conn):
        self.connections.append(conn)

    def ready_to_tick(self):
        return self.game.all_player_abilities_set

    def build(self):
        self.gs.next()
        self.game = ServerGame(self.player_count, self.mode, self.gs)
        self.gs.next()

    def is_ready(self):
        return len(self.connections) == self.player_count

    def repr(self, player) -> str:
        game_dict = self.game.start_json()
        game_dict["player_count"] = self.player_count
        game_dict["player_id"] = player
        game_dict["abilities"] = json_abilities.start_json()
        return json.dumps(game_dict)
    
    def tick_ready(self, player):
        return self.game.player_dict[player].ps.value >= 2
    
    def tick_json(self, player):
        return json.dumps(self.game.tick_json(player))
    
    def process(self, player, data):
        data = convert_keys_to_int(data)
        if data['type'] == 'ability_start':
            if json_abilities.validate_ability_selection(data['body']):
                self.game.set_abilities(player, data['body'])
                return False
            else:
                self.game.set_abilities(player, {})
                return "CHEATING: INVALID ABILITY SELECTION"
        elif data['type'] == 'ability':
            pass
            # self.game.action(data)
