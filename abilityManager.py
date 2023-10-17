from constants import *
from abilityFactory import AbilityFactory

class AbilityManager:
    def __init__(self, player, board):
        self.main_player = player
        self.abilities = AbilityFactory(self.main_player, board).abilities
        self.mode = DEFAULT_ABILITY_CODE

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif self.main_player.money >= self.abilities[key].cost:
            self.mode = key

    def update_ability(self):
        if self.ability.cost * 2 > self.main_player.money:
            self.mode = DEFAULT_ABILITY_CODE

    def use_ability(self, item, color):
        if self.ability.click_type == item.type and self.ability.color == color:
            return self.ability.complete(item)
        return False

    @property
    def ability(self):
        return self.abilities[self.mode]
