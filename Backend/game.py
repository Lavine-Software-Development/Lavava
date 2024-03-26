from constants import SPAWN_CODE
from playerStateEnums import PlayerStateEnum as PSE
from board import Board
from map_builder import MapBuilder
from ability_effects import make_ability_effects
from player import DefaultPlayer

class ServerGame:
    def __init__(self, player_count, gs):

        self.running = True
        self.gs = gs
        self.board = Board(self.gs)
        self.ability_effects = make_ability_effects(self.board)
        self.player_dict = {
            i: DefaultPlayer(i) for i in range(player_count)
        }
        self.restart()

    def start_json(self):
        return {
            "board": self.board.start_json()
        }
    
    def tick_json(self, player):
        return {
            "board": self.board.tick_json(),
            "player": self.player_dict[player].tick_json()
        }
    
    def effect(self, key, player_id, data):
        player = self.player_dict[player_id]

        if player.ps.state == PSE.START_SELECTION:
            if key == SPAWN_CODE:
                data_items = [self.board.id_dict[d] for d in data]
                self.ability_effects[key](data_items, player)
            else:
                return False
        else:  
            new_data = [self.board.id_dict[d] if d in self.board.id_dict else d for d in data]
            return player.use_ability(key, new_data)
        
    def click(self, key, player_id, item_id):
        player = self.player_dict[player_id]
        self.board.id_dict[item_id].click(player, key)
    
    def eliminate(self, player):
        self.remaining.remove(player)
        self.player_dict[player].eliminate()
        self.board.eliminate(self.player_dict[player])

    def restart(self):

        for player in self.player_dict.values():
            player.default_values()
        self.remaining = {i for i in range(len(self.player_dict))}

        self.timer = 60

        map_builder = MapBuilder()
        map_builder.build()
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)

    def set_abilities(self, player, abilities):
        self.player_dict[player].set_abilities(abilities, self.board)
        if self.all_player_abilities_set:
            self.gs.next()
            for player in self.player_dict.values():
                player.ps.next()

    @property
    def all_player_abilities_set(self):
        return all([p.ps.state == PSE.ABILITY_WAITING for p in self.player_dict.values()])
    
    @property
    def all_player_starts_selected(self):
        return all([p.ps.state == PSE.START_WAITING for p in self.player_dict.values()])
    
    def update_timer(self):
        if self.timer > 0:
            self.timer -= 0.1

            if self.timer > 3 and self.all_player_starts_selected:
                self.timer = 3
            return True

        self.gs.next()
        return False

    def tick(self):
        if not self.update_timer():
            self.board.update()
            self.player_update()
            # self.player_manager.check_over()

    def player_update(self):
        for player in self.player_dict.values():
            if not player.ps.value < PSE.ELIMINATED.value:
                player.update()
                # if player.count == 0:
                #     self.eliminate(player.id)
    