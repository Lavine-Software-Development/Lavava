from playerStateEnums import PlayerStateEnum as PSE
from gameStateEnums import GameStateEnum as GS
import mode
from board import Board
from map_builder import MapBuilder
from constants import ALL_ABILITIES, RESTART_GAME_VAL, ELIMINATE_VAL, ABILITIES_CHOSEN_VAL, TICK, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK
from ability_effects import make_ability_effects
from player import DefaultPlayer

class ServerGame:
    def __init__(self, player_count, mode_num, gs):

        self.running = True
        self.gs = gs
        mode.MODE = mode_num
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
            "player": self.player_dict[player].tick_json
        }

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

    @property
    def all_player_abilities_set(self):
        return all([p.ps.state == PSE.ABILITIES_SELECTED for p in self.player_dict.values()])
    
    @property
    def all_player_starts_selected(self):
        return all([p.ps.state == PSE.START_SELECTED for p in self.player_dict.values()])

    # def action(self, key, acting_player, data):

    #     if key == RESTART_GAME_VAL:
    #         self.restart()
    #     elif key == ELIMINATE_VAL:
    #         self.player_manager.eliminate(acting_player)
    #         self.board.eliminate(self.get_player(acting_player))
    #     elif key == ABILITIES_CHOSEN_VAL:
    #         self.player_manager.chosen(acting_player, data)
    #     elif key == TICK:
    #         if self.gs.state.value >= GS.START_SELECTION.value:
    #             self.tick()
    #     elif key in self.ability_options:
    #         new_data = [
    #             self.board.id_dict[d] if d in self.board.id_dict else d for d in data
    #         ]
    #         self.ability_effects[key](
    #             new_data, self.get_player(acting_player)
    #         )
    #     elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
    #         self.board.click(data[0],
    #             self.get_player(acting_player), key
    #         )
    #     else:
    #         print("NOT ALLOWED")

    # def tick(self):
    #     if (
    #         self.board
    #         and not self.player_manager.victor
    #         and not self.player_manager.update_timer()
    #     ):
    #         self.board.update()
    #         self.player_manager.update()
    #         self.player_manager.check_over()

    # @property
    # def ability_options(self):
    #     return ALL_ABILITIES
    
    # def get_player(self, player_num):
    #     return self.player_manager.player_dict[player_num]
    
