from jsonable import Jsonable
from constants import COUNTDOWN_LENGTH, END_GAME_LENGTH, MAIN_GAME_LENGTH, SPAWN_CODE
from playerStateEnums import PlayerStateEnum as PSE
from gameStateEnums import GameStateEnum as GSE
from board import Board
from map_builder import MapBuilder
from ability_effects import make_ability_effects
from player import DefaultPlayer
from node import Node

class ServerGame(Jsonable):
    def __init__(self, player_count, gs):

        self.running = True
        self.gs = gs
        self.board = Board(self.gs)
        self.ability_effects = make_ability_effects(self.board)
        self.player_dict = {
            i: DefaultPlayer(i) for i in range(player_count)
        }

        start_values = {'board'}
        tick_values = {'countdown_timer'}
        recurse_values = {'board'}
        super().__init__('game', start_values, recurse_values, tick_values)

        self.restart()

    def end_game(self):
        Node.end_game = True

    def effect(self, key, player_id, data):
        player = self.player_dict[player_id]

        if player.ps.state == PSE.START_SELECTION:
            if key == SPAWN_CODE:
                data_items = [self.board.id_dict[d] for d in data]
                self.ability_effects[key](data_items, player)
                player.ps.next()
            else:
                return False
        else:  
            new_data = [self.board.id_dict[d] if d in self.board.id_dict else d for d in data]
            player.use_ability(key, new_data)
        
    def event(self, key, player_id, data):
        player = self.player_dict[player_id]
        event = self.board.events[key]
        if event.can_use(player, data):
            event.use(player, data)
        else:
            print("failed to use event")

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

        self.countdown_timer = COUNTDOWN_LENGTH
        self.main_timer = MAIN_GAME_LENGTH
        self.ending_timer = END_GAME_LENGTH

        map_builder = MapBuilder()
        map_builder.build()
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)

    def set_abilities(self, player, abilities):
        self.player_dict[player].set_abilities(abilities, self.board)
        if self.all_player_abilities_set:
            print("set abilities game")
            self.gs.next()
            self.all_player_next()

    def all_player_next(self):
        for player in self.player_dict.values():
            player.ps.next()

    @property
    def all_player_abilities_set(self):
        return all([p.ps.state == PSE.ABILITY_WAITING for p in self.player_dict.values()])
    
    @property
    def all_player_starts_selected(self):
        return all([p.ps.state == PSE.START_WAITING for p in self.player_dict.values()])
    
    def update_timer(self):
        if self.countdown_timer > 0:
            self.countdown_timer -= 0.1

            if self.countdown_timer <= 0:
                self.gs.next()
                self.all_player_next()

            if self.countdown_timer > 3 and self.all_player_starts_selected:
                self.countdown_timer = 3
        
        elif self.main_timer > 0:
            self.main_timer -= 0.1

            if self.main_timer <= 0:
                self.gs.next()
                self.end_game()

        elif self.ending_timer > 0:
            self.ending_timer -= 0.1

            if self.ending_timer <= 0:
                self.gs.next()

    def tick(self):
        self.update_timer()
        
        if self.gs.value >= GSE.PLAY.value:
            self.board.update()
            self.player_update()

    def player_update(self):
        for player in self.player_dict.values():
            if player.ps.value < PSE.ELIMINATED.value:
                player.update()
                # if player.count == 0:
                #     self.eliminate(player.id)
    
