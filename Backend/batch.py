from constants import ALL_ABILITIES, EVENTS, RESTART_GAME_VAL, ELIMINATE_VAL, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ABILITIES_SELECTED
from game_state import GameState
from gameStateEnums import GameStateEnum as GS
from playerStateEnums import PlayerStateEnum as PS
from game import ServerGame
import json_abilities
from json_helpers import all_levels_dict_and_json_cost, convert_keys_to_int, json_cost, plain_json


class Batch:
    def __init__(self, count, mode, conn):
        self.connections = [conn]
        self.player_count = count
        self.mode = mode
        self.gs = GameState()
        self.tick_dict = dict()

    def add_player(self, conn):
        self.connections.append(conn)

    def build(self):
        print("build 1")
        self.gs.next()
        self.game = ServerGame(self.player_count, self.gs)
        print("build 2")
        self.gs.next()

    def is_ready(self):
        return len(self.connections) == self.player_count

    def start_repr_json(self, player) -> str:
        start_dict = self.game.start_json
        start_dict["player_count"] = self.player_count
        start_dict["player_id"] = player
        start_dict["abilities"] = json_abilities.start_json()
        start_json = plain_json(start_dict)
        return start_json
    
    def send_ready(self, player):
        return self.game.player_dict[player].ps.value >= PS.ABILITY_WAITING.value
    
    def tick_repr_json(self, player):
        self.tick_dict["player"] = self.player_tick_repr(player)
        tick_json = plain_json(self.tick_dict)
        return tick_json

    def set_group_tick_repr(self):
        self.tick_dict = self.game.tick_json
        
    def player_tick_repr(self, player):
        return self.game.player_dict[player].tick_json
    
    def tick(self):
        if self.game.gs.value >= GS.START_SELECTION.value:
            self.game.tick()
        self.set_group_tick_repr()
    
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
            self.game.effect(key, player, data['items'])
        elif key in EVENTS:
            self.game.event(key, player, data['items'])
        else:
            print("NOT ALLOWED")
        
