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
from Backend.ae_validators import make_ability_validators
from Backend.ae_effects import make_ability_effects
from player_state import PlayerState
from jsonable import Jsonable

class DefaultPlayer(Jsonable):
    def __init__(self, id):

        recurse_values = {'abilities'}
        tick_values = {'ps'}
        super().__init__(id, set(), recurse_values, tick_values)

        self.default_values()

    def set_abilities(self, abilities, board):
        validators = make_ability_validators(board, self)

        effects = make_ability_effects(board)
        for ab in abilities:
            self.abilities[ab] = ReloadAbility(ab, validators[ab], effects[ab], BREAKDOWNS[ab].reload, self, abilities[ab])
        self.ps.next()

    def use_ability(self, key, data) -> Optional[dict]:
        if self.abilities[key].can_use(data):
            self.abilities[key].use(data)

    def default_values(self):
        self.count = 0
        self.abilities = dict()
        self.effects = set()
        self.ps = PlayerState()
        self.full_capital_count = 0

    def eliminate(self):
        self.ps.eliminate()
        self.color = GREY

    def update(self):
        self.effects = set(filter(lambda effect : (effect.count()), self.effects))
        for ability in self.abilities.values():
            ability.update()

    def pass_on_effects(self, node):
        for effect in self.effects:
            effect.spread(node)

    def win(self):
        self.ps.victory()

    def lose(self):
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

    def eliminate(self):
        self.money = 0
        super().eliminate()

    def update(self):
        self.money += self.tick_production
        super().update()

    @property
    def production_per_second(self):
        return self.tick_production * 10
