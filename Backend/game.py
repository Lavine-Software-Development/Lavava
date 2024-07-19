from jsonable import JsonableTick
from constants import COUNTDOWN_LENGTH, END_GAME_LENGTH, MAIN_GAME_LENGTH, SECTION_LENGTHS, SPAWN_CODE, EVENTS
from playerStateEnums import PlayerStateEnum as PSE
from gameStateEnums import GameStateEnum as GSE
from board import Board
from map_builder import MapBuilder
from ae_effects import make_ability_effects
from player import DefaultPlayer
from ae_effects import make_event_effects
from ae_validators import make_effect_validators
from event import Event

class ServerGame(JsonableTick):
    def __init__(self, player_count, gs):

        self.running = True
        self.gs = gs
        self.extra_info = []
        self.board = Board(self.gs)
        self.player_dict = {
            i: DefaultPlayer(i) for i in range(player_count)
        }

        start_values = {'board'}
        tick_values = {'countdown_timer', 'gs', 'extra_info'}
        recurse_values = {'board'}
        super().__init__('game', start_values, recurse_values, tick_values)

        self.restart()

    @property
    def countdown_timer(self):
        return self.times[self.current_section]

    def effect(self, key, player_id, data):
        player = self.player_dict[player_id]
        print(player.ps.state, PSE.START_SELECTION)
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
        event = self.events[key]
        if event.can_use(player, data):
            event.use(player, data)
        else:
            print("failed to use event")
    
    def eliminate(self, player, forced=False):
        rank = len(self.remaining)
        self.remaining.remove(player)
        self.player_dict[player].eliminate(rank)
        # Forced when they already have no nodes
        # Voluntary when they quit, thus the board needs to clean up what they have that still exists
        if not forced:
            self.board.eliminate(self.player_dict[player])

    def update_extra_info(self, data):
        self.extra_info.append(data)

    def restart(self):

        for player in self.player_dict.values():
            player.default_values()
        self.remaining = {i for i in range(len(self.player_dict))}

        self.times = SECTION_LENGTHS.copy()
        self.current_section = 0

        map_builder = MapBuilder()
        map_builder.build()
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)

        self.ability_effects = make_ability_effects(self.board)
        self.events = self.make_events_dict()

        
    def make_events_dict(self):
        validators = make_effect_validators(self.board)
        effects = make_event_effects(self.board, self.update_extra_info)
        return {code: Event(validators[code], effects[code]) for code in EVENTS}

    def set_abilities(self, player, abilities):
        self.player_dict[player].set_abilities(abilities, self.ability_effects, self.board)

    def all_player_next(self):
        for player in self.player_dict.values():
            player.ps.next()
    
    @property
    def all_player_starts_selected(self):
        return all([p.ps.state in (PSE.START_WAITING, PSE.ELIMINATED) for p in self.player_dict.values()])
    
    def update_timer(self):

        if self.countdown_timer > 0:
            self.times[self.current_section] -= 0.1

            if self.gs.value == GSE.START_SELECTION.value and self.countdown_timer > 3 and self.all_player_starts_selected:
                self.times[self.current_section] = 3

            if self.countdown_timer <= 0:

                if self.gs.value < GSE.END_GAME.value:
                    self.current_section += 1

                    if self.gs.value == GSE.START_SELECTION.value:
                        self.all_player_next()
                    else:
                        self.board.end_game()
                else:
                    self.determine_ranks_from_capitalize_or_timeout()
                
                self.gs.next()

    def tick(self):
        self.update_timer()
        # print("remaining player:", self.remaining)
        if self.gs.value >= GSE.PLAY.value:
            self.board.update()
            self.player_update()

        if self.board.victory_check():
            self.determine_ranks_from_capitalize_or_timeout()
        elif len(self.remaining) == 1:

            self.determine_ranks_from_elimination(self.remaining.pop())

    def post_tick(self):
        self.extra_info.clear()

    def player_update(self):
        for player in self.player_dict.values():
            if player.ps.value < PSE.ELIMINATED.value:
                player.update()
                if player.count == 0:
                    self.eliminate(player.id, True)
                    self.update_extra_info(("player_elimination", (player.id, player.killer.id)))
                    print("the killer is", player.killer)

    def determine_ranks_from_capitalize_or_timeout(self):
        # total owned nodes: a
        # theoretical maximum of 65
        player_nodes = {player.id: player.count for player in self.player_dict.values()}

        # total owned full capitals: b
        # maximum of 3
        player_capitals = {player.id: player.full_capital_count for player in self.player_dict.values()}

        # score equals 100b + a
        # effectively, the player with the most full capitals wins, with total nodes as a tiebreaker
        player_scores = {key: val * 100 + player_nodes[key] for key, val in player_capitals.items()}
        sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        self.player_dict[sorted_scores[0][0]].win()
        for i in range(1, len(sorted_scores)):
            self.player_dict[sorted_scores[i][0]].lose(i + 1)

        self.gs.end()

    def determine_ranks_from_elimination(self, winner):
        self.player_dict[winner].win()
        for player in self.player_dict.values():
            # all other players should be eliminated so theoretically this gets the rest
            if player.ps.value == PSE.ELIMINATED.value:
                player.lose()

        self.gs.end()

        
