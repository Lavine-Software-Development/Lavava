from constants import ALL_ABILITIES, EVENTS, FORFEIT_CODE, RESTART_GAME_VAL, ELIMINATE_VAL, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ABILITIES_SELECTED
from game_state import GameState
from gameStateEnums import GameStateEnum as GS
from playerStateEnums import PlayerStateEnum as PS
from game import ServerGame
import json_abilities
from json_helpers import all_levels_dict_and_json_cost, convert_keys_to_int, json_cost, plain_json
import requests
from pympler import asizeof
import json

class Batch:
    def __init__(self, count, mode, token, websocket, ability_data):
        self.full_tick_count = 0
        self.token_ids = {}
        self.id_sockets = {}
        self.elo_changes = {}
        self.ending_count = 0
        self.player_count = count
        self.mode = mode
        self.gs = GameState()
        self.game = ServerGame(self.player_count, self.gs)
        self.add_player(token, websocket, ability_data)
        self.tick_dict = dict()

    def update_elo(self):
        
        connection_ranks = [(token, self.game.player_dict[self.token_ids[token]].rank) for token in self.token_ids]
        connection_ranks = [item[0] for item in sorted(connection_ranks, key=lambda x: x[1])]
        # this ends up as player token, player id, in order of rank

        url = 'http://localhost:5001/elo'
        data = {"ordered_players": connection_ranks}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                for token, elos in response_data.get("new_elos").items():
                    player_id = self.token_ids[token]
                    self.elo_changes[player_id] = elos
            except ValueError:
                print("Response is not valid JSON:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")

    def add_player(self, token, websocket, ability_data):
        player_id = len(self.token_ids)
        if self.ability_process(player_id, ability_data):
            self.token_ids[token] = player_id
            self.id_sockets[player_id] = websocket
            return False
        else:
            return "CHEATING: INVALID ABILITY SELECTION"
        
    def remove_player(self, token):
        removed_id = self.token_ids.pop(token)
        for othertoken in self.token_ids:
            if self.token_ids[othertoken] > removed_id:
                self.token_ids[othertoken] = self.token_ids[othertoken] - 1
        self.id_sockets.pop(removed_id)

    def reconnect_player(self, token, websocket):
        player_id = self.token_ids[token]
        self.id_sockets[player_id] = websocket
        game_dict = self.game.full_tick_json
        game_dict["player"] = self.player_tick_repr(player_id)
        game_dict["isFirst"] = False
        return plain_json(game_dict)
        
    def start(self):
        self.gs.next()
        self.game.all_player_next()

    def is_ready(self):
        return len(self.token_ids) == self.player_count

    def start_repr_json(self, player_id) -> str:
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
        return self.mode != "LADDER" and self.gs.value == GS.GAME_OVER.value
    
    def tick_repr_json(self, player_id):
        self.tick_dict["player"] = self.player_tick_repr(player_id)
        if GS.GAME_OVER.value == self.game.gs.value and self.elo_changes != {} and self.mode == "LADDER":
            self.tick_dict["new_elos"] = self.elo_changes[player_id]
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
        if self.game.gs.value == GS.GAME_OVER.value and self.elo_changes == {} and self.mode == "LADDER":
            self.update_elo()

    def ability_process(self, player, data):
        data = convert_keys_to_int(data)
        if json_abilities.validate_ability_selection(data):
            self.game.set_abilities(player, data)
            return True
        else:
            self.game.set_abilities(player, {})
            return 

    def process(self, token, data): 
        player_id = self.token_ids[token]
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
        
