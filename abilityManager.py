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

    def update(self):
        pass

    @abstractmethod
    def select(self, key):
        pass

    @abstractmethod
    def update_ability(self):
        pass

    @abstractmethod
    def default_validate(self):
        pass

    def input(self, key, player, data):
        return self.abilities[key].effect(player, data)

    @property
    def ability(self):
        return self.abilities[self.mode]

class MoneyAbilityManager(AbstractAbilityManager):
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

    def input(self, key, player, data):
        player.money -= self.abilities[key].cost
        return super().input(key, player, data)

    def default_validate(self):
        return CONTEXT['main_player'].money >= self.ability.cost

class ReloadAbilityManager(AbstractAbilityManager):
    def __init__(self, board):
        super().__init__(board, create_reload_abilities)
        self.load_count = {SPAWN_CODE: SPAWN_RELOAD, BRIDGE_CODE: 0, FREEZE_CODE: 0}
        self.remaining_usage = {SPAWN_CODE: SPAWN_TOTAL, BRIDGE_CODE: BRIDGE_TOTAL, FREEZE_CODE: FREEZE_TOTAL}

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif self.full(key):
            self.mode = key

    def update_ability(self):
        self.mode = DEFAULT_ABILITY_CODE

    def input(self, key, player, data):
        if player == CONTEXT['main_player']:
            self.load_count[key] = 0
            self.remaining_usage[key] -= 1
        return super().input(key, player, data)

    def update(self):
        for key in self.load_count:
            if self.remaining_usage[key] > 0:
                if not self.full(key):
                    self.load_count[key] += 0.1

    def default_validate(self):
        return self.full(DEFAULT_ABILITY_CODE)

    def full(self, key):
        return self.load_count[key] == self.abilities[key].cost