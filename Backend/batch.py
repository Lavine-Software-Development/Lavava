from constants import ALL_ABILITIES, EVENTS, FORFEIT_CODE, RESTART_GAME_VAL, ELIMINATE_VAL, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ABILITIES_SELECTED
from game_state import GameState
from gameStateEnums import GameStateEnum as GS
from playerStateEnums import PlayerStateEnum as PS
from game import ServerGame
import json_abilities
from json_helpers import all_levels_dict_and_json_cost, convert_keys_to_int, json_cost, plain_json


class Batch:
    def __init__(self, count, mode, conn, ability_data):
        self.connections = {}
        self.player_count = count
        self.mode = mode
        self.gs = GameState()
        self.game = ServerGame(self.player_count, self.gs)
        self.add_player(conn, ability_data)
        self.tick_dict = dict()

    def add_player(self, conn, ability_data):
        player_id = len(self.connections)
        if self.ability_process(player_id, ability_data):
            self.connections[conn] = player_id
            return False
        else:
            return "CHEATING: INVALID ABILITY SELECTION"
        
    def start(self):
        self.gs.next()
        self.game.all_player_next()

    def is_ready(self):
        return len(self.connections) == self.player_count

    def start_repr_json(self, conn) -> str:
        player_id = self.connections[conn]
        start_dict = self.game.start_json
        start_dict["player_count"] = self.player_count
        start_dict["player_id"] = player_id
        start_dict["abilities"] = json_abilities.start_json()
        start_dict['isFirst'] = True
        start_json = plain_json(start_dict)
        return start_json
    
    # def send_ready(self, player):
    #     return self.game.player_dict[player].ps.value >= PS.WAITING.value
    
    def tick_repr_json(self, conn):
        player_id = self.connections[conn]
        self.tick_dict["player"] = self.player_tick_repr(player_id)
        self.tick_dict["isFirst"] = False 
        tick_json = plain_json(self.tick_dict)
        return tick_json

    def set_group_tick_repr(self):
        self.tick_dict = self.game.tick_json
        
    def player_tick_repr(self, player_id):
        return self.game.player_dict[player_id].tick_json
    
    def tick(self):
        # print(self.game.gs.value, GS.START_SELECTION.value)

        if self.game.gs.value >= GS.START_SELECTION.value:
            self.game.tick()
        self.set_group_tick_repr()

    def ability_process(self, player, data):
        data = convert_keys_to_int(data)
        if json_abilities.validate_ability_selection(data):
            self.game.set_abilities(player, data)
            return True
        else:
            self.game.set_abilities(player, {})
            return 

    def process(self, conn, data): 
        player_id = self.connections[conn]
        data = convert_keys_to_int(data)
        key = data["code"]
            
        if key == RESTART_GAME_VAL:
            self.game.restart()
        elif key in (ELIMINATE_VAL, FORFEIT_CODE):
            self.game.eliminate(player_id)
        elif key in ALL_ABILITIES:
            print("ABILITY")
            self.game.effect(key, player_id, data['items'])
        elif key in EVENTS:
            print("EVENT")
            self.game.event(key, player_id, data['items'])
        else:
            print("NOT ALLOWED")
        print("Done processing")
        
