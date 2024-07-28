from typing import Optional

from ability import CreditAbility, RoyaleAbility
from constants import (
    GREY,
    START_MONEY,
    START_MONEY_RATE,
    CAPITAL_BONUS,
    BREAKDOWNS,
    KILL_BONUS,
    OVERTIME_BONUS,
    TIME_AMOUNT,
    ELIXIR_CAP,
)
from ae_validators import make_ability_validators
from player_state import PlayerState
from jsonable import JsonableTick
from math import floor

class DefaultPlayer(JsonableTick):
    def __init__(self, id):

        recurse_values = {'abilities'}
        tick_values = {'ps', 'credits'}
        # tick_values = {'ps', 'count'}
        super().__init__(id, set(), recurse_values, tick_values)

        self.default_values()

    def killed_event(self, player):
        self.killer = player

    def set_abilities(self, chosen_abilities, ability_effects, board, settings):
        pass

    def use_ability(self, key, data) -> Optional[dict]:
        if self.abilities[key].can_use(data):
            self.abilities[key].use(data)
        else:
            print("failed to use ability, ", key)

    def default_values(self):
        self.killer = None
        self.count = 0
        self.abilities = dict()
        self.ps = PlayerState()
        self.rank = 0
        self.credits = 0

    def eliminate(self, rank):
        self.rank = rank
        self.ps.eliminate()
        self.color = GREY

    def win(self):
        self.rank = 1
        self.ps.victory()

    def lose(self, rank=None):
        if rank:
            self.rank = rank
        self.ps.defeat()

    def capital_handover(self, gain):
        pass

    def overtime_bonus(self):
        pass

    def update(self):
        pass


class CreditPlayer(DefaultPlayer):

    def update(self):
        for ability in self.abilities.values():
            ability.update()

    def default_values(self):
        super().default_values()
        self.credits = 0

    def eliminate(self, rank):
        super().eliminate(rank)
        for ability in self.abilities.values():
            ability.load_amount = 0

    def killed_event(self, player):
        super().killed_event(player)
        player.kill_bonus()

    def kill_bonus(self):
        self.credits += KILL_BONUS

    def overtime_bonus(self):
        self.credits += OVERTIME_BONUS

    def set_abilities(self, chosen_abilities, ability_effects, board, settings):
        validators = make_ability_validators(board, self, settings)

        for ab in chosen_abilities:
            self.abilities[ab] = CreditAbility(ab, validators[ab], ability_effects[ab], BREAKDOWNS[ab].reload, self, chosen_abilities[ab])


class RoyalePlayer(DefaultPlayer):

    def default_values(self):
        super().default_values()
        self.mini_counter = 0
        self.elixir = 0

    def set_abilities(self, chosen_abilities, ability_effects, board, settings):
        validators = make_ability_validators(board, self, settings)

        for ab in chosen_abilities:
            self.abilities[ab] = RoyaleAbility(ab, validators[ab], ability_effects[ab], BREAKDOWNS[ab].elixir, self)

    def update(self):
        if self.elixir < ELIXIR_CAP:
            pre_count = self.mini_counter
            self.mini_counter += TIME_AMOUNT

            # iff we went to a new integer
            if floor(pre_count) != floor(self.mini_counter):
                self.elixir += 1
                for ability in self.abilities.values():
                    if self.elixir <= ability.in_game_cost:
                        ability.update()

class MoneyPlayer(DefaultPlayer):
    def default_values(self):
        self.money = START_MONEY
        self.tick_production = START_MONEY_RATE
        super().default_values()

    def change_tick(self, amount):
        self.tick_production += amount

    def capital_handover(self, gain):
        if gain:
            self.tick_production += CAPITAL_BONUS
        else:
            self.tick_production -= CAPITAL_BONUS
        super().capital_handover(gain)

    # def eliminate(self):
    #     self.money = 0
    #     super().eliminate()

    def update(self):
        self.money += self.tick_production
        super().update()

    @property
    def production_per_second(self):
        return self.tick_production * 10
