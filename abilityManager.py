from constants import *
from abc import ABC, abstractmethod
from ability import *
from ability_factory import make_abilities
from chooseUI import choose_abilities_ui

class AbstractAbilityManager(ABC):
    def __init__(self, board):
        self.ability_codes = choose_abilities_ui()
        self.abilities = self.create_abilities(board)
        self.mode = DEFAULT_ABILITY_CODE

    def set_box_numbers(self, stat):
        for ability in self.abilities.values():
            ability.box.set_stat_func(lambda key=ability.key: stat[key])

    def choose_abilities(self):
        while True:
            print("Choose 4 Abilities by letter. Caps unnecessary. List without spaces:")
            for code in CONTEXT['all_ability_codes']:
                print(f'{BREAKDOWNS[code]["letter"]} - {BREAKDOWNS[code]["name"]}')
            choices = input("Choose: ")
            split_choices = {x.upper() for x in choices}
            if len(split_choices) == 4 and all(x in LETTER_TO_CODE for x in split_choices):
                codes = [LETTER_TO_CODE[x] for x in split_choices]
                if all(x in CONTEXT['all_ability_codes'] for x in codes):
                    CONTEXT['all_ability_codes'].add(SPAWN_CODE)
                    return [SPAWN_CODE] + codes
            print('Oops bad input. Try again!')

    def create_abilities(self, board):
        codes = self.ability_codes
        all_dict = make_abilities(board)
        return {k: all_dict[k] for k in codes}

    def use_ability(self, item, color):
        if self.ability.click_type == item.type and self.box.color == color:
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

    @property
    def ability(self):
        return self.abilities[self.mode]

    @property
    def box(self):
        return self.ability.box

class MoneyAbilityManager(AbstractAbilityManager):
    def __init__(self, board):
        super().__init__(board)
        self.costs = {code: BREAKDOWNS[code]['cost'] for code in self.ability_codes}
        self.set_box_numbers(self.costs)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif CONTEXT['main_player'].money >= self.costs[key]:
            self.mode = key

    def update_ability(self):
        CONTEXT['main_player'].money -= self.costs[self.mode]
        if self.costs[self.mode] > CONTEXT['main_player'].money:
            self.mode = DEFAULT_ABILITY_CODE

    def default_validate(self):
        return CONTEXT['main_player'].money >= self.costs[SPAWN_CODE]

class ReloadAbilityManager(AbstractAbilityManager):
    def __init__(self, board):
        super().__init__(board)
        self.load_count = {code: 0 for code in self.ability_codes}
        self.load_count[SPAWN_CODE] = SPAWN_RELOAD
        self.remaining_usage = {code: BREAKDOWNS[code]['total'] for code in self.ability_codes}
        self.full_reload = {code: BREAKDOWNS[code]['reload'] for code in self.ability_codes}
        self.set_box_numbers(self.remaining_usage)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif self.full(key):
            self.mode = key

    def update_ability(self):
        self.load_count[self.mode] = 0
        self.remaining_usage[self.mode] -= 1
        self.mode = DEFAULT_ABILITY_CODE

    def update(self):
        for key in self.load_count:
            if self.remaining_usage[key] > 0:
                if not self.full(key):
                    self.load_count[key] += 0.1

    def default_validate(self):
        return self.full(DEFAULT_ABILITY_CODE)

    def full(self, key):
        return self.load_count[key] >= self.full_reload[key]