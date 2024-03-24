import json
from Frontend.constants import SPAWN_CODE
from constants import ALL_ABILITIES, RESTART_GAME_VAL, ELIMINATE_VAL, TICK, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ABILITIES_SELECTED
from game_state import GameState
from gameStateEnums import GameStateEnum as GS
from playerStateEnums import PlayerStateEnum as PS
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
    
    def send_ready(self, player):
        return self.game.player_dict[player].ps.value >= PS.ABILITY_WAITING.value

    def tick_json(self, player):
        return json.dumps(self.game.tick_json(player))
    
    def tick(self):
        if self.game.gs.value >= GS.START_SELECTION.value:
            self.game.tick()
    
    def process(self, player, data):
        data = convert_keys_to_int(data)
        key = data['code']

        if key == ABILITIES_SELECTED:
            if json_abilities.validate_ability_selection(data['body']):
                self.game.set_abilities(player, data['body'])
                return False
            else:
                self.game.set_abilities(player, {})
                return "CHEATING: INVALID ABILITY SELECTION"
            
        elif key == RESTART_GAME_VAL:
            self.game.restart()
        elif key == ELIMINATE_VAL:
            self.game.eliminate(player)
        elif key in ALL_ABILITIES:
            self.game.effect(key, player, data)
        elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
            self.game.click(data[0], player, key)
        else:
            print("NOT ALLOWED")
        
