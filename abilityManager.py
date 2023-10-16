from constants import *
from abilityFactory import AbilityFactory

class AbilityManager:
    def __init__(self, player_dict, player_num, board):
        self.player_dict = player_dict
        self.player = player_dict[player_num]
        self.board = board
        self.abilities = AbilityFactory(self.player, self.board).abilities
        self.mode = DEFAULT_ABILITY_CODE

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif self.player.money >= self.abilities[key].cost:
            self.mode = key

    def update_ability(self):
        if self.ability.cost * 2 > self.player.money:
            self.mode = DEFAULT_ABILITY_CODE

    def action(self, key, acting_player, data):
        if key in self.abilities:
            new_data = (self.board.id_dict[d] if d in self.board.id_dict else d for d in data)
            self.abilities[key].input(self.player_dict[acting_player], new_data)
        elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
            self.board.id_dict[data[0]].click(self.player_dict[acting_player], key)
        elif key == ELIMINATE_VAL:
            self.eliminate(acting_player)

    def use_ability(self):
        if self.ability.click_type == self.board.highlighted.type and self.ability.color == self.board.highlighted_color:
            return self.ability.complete(self.board.highlighted)
        return False

    @property
    def ability(self):
        return self.abilities[self.mode]
