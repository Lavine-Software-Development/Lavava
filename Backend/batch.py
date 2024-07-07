from constants import ALL_ABILITIES, EVENTS, FORFEIT_CODE, RESTART_GAME_VAL, ELIMINATE_VAL, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ABILITIES_SELECTED
from game_state import GameState
from gameStateEnums import GameStateEnum as GS
from playerStateEnums import PlayerStateEnum as PS
from game import ServerGame
import json_abilities
from json_helpers import all_levels_dict_and_json_cost, convert_keys_to_int, json_cost, plain_json
import requests
import json


class Batch:
    def __init__(self, count, mode, conn, ability_data, userToken):
        self.connections = {}
        self.elo_changes = {}
        self.tokens = {}
        self.ending_count = 0
        self.player_count = count
        self.mode = mode
        self.gs = GameState()
        self.game = ServerGame(self.player_count, self.gs)
        self.add_player(conn, ability_data, userToken)
        self.tick_dict = dict()

    def update_elo(self):
        
        connection_ranks = [(self.tokens[conn], self.connections[conn], self.game.player_dict[self.connections[conn]].rank) for conn in self.connections]
        connection_ranks = [(item[0], item[1]) for item in sorted(connection_ranks, key=lambda x: x[2])]
        # this ends up as player token, player id, in order of rank

        url = 'http://localhost:5001/elo'
        data = {"ordered_players": connection_ranks}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                self.elo_changes = response_data.get("new_elos")
            except ValueError:
                print("Response is not valid JSON:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")

    def add_player(self, conn, ability_data, userToken):
        player_id = len(self.connections)
        if self.ability_process(player_id, ability_data):
            self.connections[conn] = player_id
            if userToken:
                self.tokens[conn] = userToken
            return False
        else:
            return "CHEATING: INVALID ABILITY SELECTION"
        
    def remove_player(self, conn):
        removed_id = self.connections.pop(conn)
        if conn in self.tokens:
            self.tokens.pop(conn)
        for conn in self.connections:
            if self.connections[conn] > removed_id:
                self.connections[conn] = self.connections[conn] - 1
        
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
    
    def done(self):
        if self.elo_changes != {}:
            self.ending_count += 1
            return self.ending_count == 5
        return False
    
    def tick_repr_json(self, conn):
        player_id = self.connections[conn]
        self.tick_dict["player"] = self.player_tick_repr(player_id)
        if GS.GAME_OVER.value == self.game.gs.value and self.elo_changes != {}:
            self.tick_dict["new_elos"] = self.elo_changes[str(player_id)]
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
        if self.game.gs.value == GS.GAME_OVER.value and self.elo_changes == {}:
            self.update_elo()

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
        
