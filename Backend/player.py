from typing import Optional

from ability import ReloadAbility
from constants import (
    GREY,
    CAPITAL_WIN_COUNT,
    START_MONEY,
    START_MONEY_RATE,
    CAPITAL_BONUS,
    BREAKDOWNS,
)
from ae_validators import make_ability_validators
from player_state import PlayerState
from jsonable import JsonableTick

class DefaultPlayer(JsonableTick):
    def __init__(self, id):

        recurse_values = {'abilities'}
        tick_values = {'ps'}
        # tick_values = {'ps', 'count'}
        super().__init__(id, set(), recurse_values, tick_values)

        self.default_values()

    def set_abilities(self, chosen_abilities, ability_effects, board):
        validators = make_ability_validators(board, self)

        for ab in chosen_abilities:
            self.abilities[ab] = ReloadAbility(ab, validators[ab], ability_effects[ab], BREAKDOWNS[ab].reload, self, chosen_abilities[ab])

    def use_ability(self, key, data) -> Optional[dict]:
        if self.abilities[key].can_use(data):
            self.abilities[key].use(data)

    def default_values(self):
        self.count = 0
        self.abilities = dict()
        self.ps = PlayerState()
        self.rank = 0
        self.full_capital_count = 0

    def eliminate(self, rank):
        self.rank = rank
        self.ps.eliminate()
        self.color = GREY
        for ability in self.abilities.values():
            ability.load_amount = 0

    def update(self):
        for ability in self.abilities.values():
            ability.update()

    def win(self):
        self.rank = 1
        self.ps.victory()

    def lose(self, rank=None):
        if rank:
            self.rank = rank
        self.ps.defeat()

    def capital_handover(self, gain):
        pass

    def check_capital_win(self):
        return self.full_capital_count == CAPITAL_WIN_COUNT


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
