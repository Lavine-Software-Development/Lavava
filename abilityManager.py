from constants import *
from abilityFactory import create_money_abilities, create_reload_abilities
from abc import ABC, abstractmethod

class AbstractAbilityManager(ABC):
    def __init__(self, board, ability_maker):
        self.abilities = ability_maker(board)
        self.mode = DEFAULT_ABILITY_CODE

    def use_ability(self, item, color):
        if self.ability.click_type == item.type and self.ability.color == color:
            return self.ability.complete(item)
        return False

    @abstractmethod
    def select(self, key):
        pass

    @abstractmethod
    def update_ability(self):
        pass

    @property
    def ability(self):
        return self.abilities[self.mode]

class MoneyAbilityManager:
    def __init__(self, board):
        super().__init__(board, create_money_abilities)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif CONTEXT['main_player'].money >= self.abilities[key].cost:
            self.mode = key

    def update_ability(self):
        if self.ability.cost * 2 > CONTEXT['main_player'].money:
            self.mode = DEFAULT_ABILITY_CODE


class ReloadAbilityManager:

