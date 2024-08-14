from jsonable import JsonableTick
from constants import COUNTDOWN_LENGTH, OVERTIME_BONUS, SPAWN_CODE, EVENTS
from playerStateEnums import PlayerStateEnum as PSE
from gameStateEnums import GameStateEnum as GSE
from board import Board
from map_builder import MapBuilder
from ae_effects import make_ability_effects
from player import CreditPlayer, RoyalePlayer
from ae_effects import make_event_effects
from ae_validators import make_effect_validators
from event import Event
import sys
from baseAI import create_ai, AI

class ServerGame(JsonableTick):
    def __init__(self, player_count, gs, settings):

        self.running = True
        self.gs = gs
        self.settings = settings
        self.extra_info = []
        self.counts = [0] * player_count
        self.board = Board(self.gs, settings['ability_type'] == "credits")
        if settings["ability_type"] == "credits":
            self.player_dict = {
                i: CreditPlayer(i) for i in range(player_count)
            }
        else:
            self.player_dict = {
                i: RoyalePlayer(i, settings) for i in range(player_count)
            }

        start_values = {'board'}
        tick_values = {'countdown_timer', 'gs', 'extra_info', 'counts'}
        recurse_values = {'board'}
        super().__init__('game', start_values, recurse_values, tick_values)

        self.restart()

    @property
    def countdown_timer(self):
        return self.times[self.current_section]
    
    def get_ordered_counts(self):
        return sorted(self.counts, reverse=True)
    
    def create_bot(self, player_id, ability_process):
        self.player_dict[player_id] = create_ai(player_id, self.settings, self.board, self.effect, self.event, self.get_ordered_counts, self.eliminate, ability_process)
        return self.player_dict[player_id].name

    @property
    def bots(self):
        return [player for player in self.player_dict.values() if isinstance(player, AI)]

    def effect(self, key, player_id, data):
        player = self.player_dict[player_id]
        if player.ps.state == PSE.START_SELECTION:
            if key == SPAWN_CODE:
                data_items = [self.board.id_dict[d] for d in data]
                self.ability_effects[key](data_items, player)
                player.ps.next()
                return True
            else:
                return False
        else:
            try:
                new_data = [self.board.id_dict[d] for d in data]
                return player.use_ability(key, new_data)
            except KeyError:
                print("failed to use ability because item no longer exists")
                return False
        
    def event(self, key, player_id, data):
        player = self.player_dict[player_id]
        event = self.events[key]
        if event.can_use(player, data):
            event.use(player, data)
            return True
        else:
            print("failed to use event")
            return False
    
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

        self.accessibility_times = self.settings['accessibility_times'] if self.settings['iterative_make_accessible'] else []

        for player in self.player_dict.values():
            player.default_values()
        self.remaining = {i for i in range(len(self.player_dict))}

        self.times = [COUNTDOWN_LENGTH, self.settings["main_time"], self.settings["overtime"]]
        self.current_section = 0

        map_builder = MapBuilder()
        map_builder.build(self.settings)
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)

        self.ability_effects = make_ability_effects(self.board, self.settings)
        self.events = self.make_events_dict()

        
    def make_events_dict(self):
        validators = make_effect_validators(self.board)
        effects = make_event_effects(self.board, self.update_extra_info)
        return {code: Event(validators[code], effects[code]) for code in EVENTS}

    def set_abilities(self, player, abilities, settings):
        print("setting abilities for player", player, "with abilities", abilities)
        self.player_dict[player].set_abilities(abilities, self.ability_effects, self.board, settings)

    def set_player_settings(self, player, settings):
        self.player_dict[player].set_settings(settings) 

    def all_player_next(self):
        for player in self.player_dict.values():
            player.ps.next()
    
    @property
    def all_player_starts_selected(self):
        return all([p.ps.state in (PSE.START_WAITING, PSE.ELIMINATED) for p in self.player_dict.values()])
    
    @property 
    def no_player_starts_selected(self):
        return all([p.ps.state == PSE.START_SELECTION for p in self.player_dict.values()]) 
    
    def update_timer(self):

        if self.countdown_timer > 0:
            self.times[self.current_section] -= 0.1

            if self.accessibility_times and self.gs.value == GSE.PLAY.value:
                if self.times[self.current_section] <= self.settings['main_time'] - self.accessibility_times[0]:  
                    self.board.make_accessible()
                    self.accessibility_times.pop(0)
                    self.update_extra_info(("Walls Down"))

            if self.gs.value == GSE.START_SELECTION.value and self.countdown_timer > 3 and self.all_player_starts_selected:
                self.times[self.current_section] = 3

            if self.countdown_timer <= 0:
                if self.no_player_starts_selected:
                    print("Neither player selected start node")
                    for player in self.player_dict.values():
                        player.ps.eliminate()
                        self.update_extra_info(("Aborted"))
                    return
                
                if self.gs.value < GSE.END_GAME.value:
                    print("updating section")
                    self.current_section += 1

                    if self.gs.value == GSE.START_SELECTION.value:
                        self.all_player_next()
                    else:
                        self.end_game_events()
                else:
                    self.determine_ranks_from_capitalize_or_timeout()
                
                self.gs.next()

    def tick(self):
        self.update_timer()
        self.counts = [self.player_dict[i].count for i in range(len(self.player_dict))]
        # print("remaining player:", self.remaining)
        if self.gs.value >= GSE.PLAY.value:
            # print("Gamestaet value: " + str(self.gs.value))
            sys.stdout.flush()
            self.board.update()
            self.player_update()

        if self.gs.value == GSE.START_SELECTION.value:
            for bot in self.bots:
                bot.choose_start()

        if self.board.victory_check() or self.only_bots_remain():
            self.determine_ranks_from_capitalize_or_timeout()
        elif len(self.remaining) == 1:

            self.determine_ranks_from_elimination(self.remaining.pop())

    def only_bots_remain(self):
        return all([isinstance(self.player_dict[player], AI) for player in self.remaining])

    def post_tick(self):
        self.extra_info.clear()

    def end_game_events(self):
        self.board.end_game()
        for player in self.player_dict.values():
            player.overtime_bonus()
        self.update_extra_info(("End Game", OVERTIME_BONUS))

    def player_update(self):
        for player in self.player_dict.values():
            if player.ps.value < PSE.ELIMINATED.value:
                if self.gs.value < GSE.END_GAME.value:
                    player.update()
                if player.count == 0:
                    self.eliminate(player.id, True)
                    if player.killer:
                        self.update_extra_info(("player_elimination", (player.id, player.killer.id)))
                    else:
                        self.update_extra_info(("timed_out", (player.id)))


                    print("the killer is", player.killer)

    def determine_ranks_from_capitalize_or_timeout(self):
        # total owned nodes: a
        # theoretical maximum of 65
        player_nodes = {player.id: player.count for player in self.player_dict.values()}

        player_capitals = self.only_winner_capitals_count()

        # score equals 100b + a
        # effectively, the player with the most full capitals wins, with total nodes as a tiebreaker
        # but if already eliminated, they are effectively ranked backwards by multiplying their predetermined rank by -1000
        player_scores = {key: self.player_dict[key].rank * -1000 + val * 100 + player_nodes[key] for key, val in player_capitals.items()}
        sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        self.player_dict[sorted_scores[0][0]].win()
        for i in range(1, len(sorted_scores)):
            self.player_dict[sorted_scores[i][0]].lose(i + 1)

        self.gs.end()

    def hundred_per_capital(self):
        # total owned full capitals: b
        # maximum of 3
        return {player.id: self.board.full_player_capitals[player.id] for player in self.player_dict.values()}

    def only_winner_capitals_count(self):
        # 1 if having 3 full capitals, 0 otherwise
        return {player.id: int(self.board.full_player_capitals[player.id] >= 3) for player in self.player_dict.values()}

    def determine_ranks_from_elimination(self, winner):
        self.player_dict[winner].win()
        for player in self.player_dict.values():
            # all other players should be eliminated so theoretically this gets the rest
            if player.ps.value == PSE.ELIMINATED.value:
                player.lose()

        self.gs.end()

        
