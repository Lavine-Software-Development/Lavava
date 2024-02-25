from constants import (
    BREAKDOWNS,
    SPAWN_RELOAD,
    RAGE_CODE,
    CONTEXT,
    SPAWN_CODE,
)
from abc import ABC, abstractmethod
from ability_factory import make_abilities
from chooseUI import choose_abilities_ui


class AbstractAbilityManager(ABC):
    def __init__(self, board, gs):
        self.ability_codes = choose_abilities_ui(gs)
        self.abilities = self.create_abilities(board)
        self.mode = None

    def set_box_numbers(self, stat):
        for ability in self.abilities.values():
            ability.box.set_stat_func(lambda key=ability.key: stat[key])

    def create_abilities(self, board):
        codes = self.ability_codes
        all_dict = make_abilities(board)
        return {k: all_dict[k] for k in codes}

    def use_ability(self, item, color):
        if not self.ability:
            return False
        if self.ability.click_type == item.type and self.box_col == color:
            return self.ability.complete(item)
        return False

    def switch_to(self, key):
        self.mode = key
        return self.ability.complete_check()

    def update(self):
        pass

    @abstractmethod
    def select(self, key):
        pass

    @abstractmethod
    def update_ability(self):
        pass

    @property
    def ability(self):
        if not self.mode:
            return None
        return self.abilities[self.mode]

    @property
    def box_col(self):
        if not self.ability:
            return CONTEXT["main_player"].default_color
        return self.ability.box.color


class MoneyAbilityManager(AbstractAbilityManager):
    def __init__(self, board, gs):
        super().__init__(board, gs)
        self.costs = {code: BREAKDOWNS[code]["cost"] for code in self.ability_codes}
        self.set_box_numbers(self.costs)

    def select(self, key):
        if self.ability:
            self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = None
        elif CONTEXT["main_player"].money >= self.costs[key]:
            return self.switch_to(key)
        return False

    def update_ability(self):
        CONTEXT["main_player"].money -= self.costs[self.mode]
        if (
            self.costs[self.mode] > CONTEXT["main_player"].money
            or self.mode == RAGE_CODE
        ):
            self.mode = None


class ReloadAbilityManager(AbstractAbilityManager):
    def __init__(self, board, gs):
        super().__init__(board, gs)
        self.load_count = {code: 0.0 for code in self.ability_codes}
        self.load_count[SPAWN_CODE] = SPAWN_RELOAD
        self.remaining_usage = {
            code: BREAKDOWNS[code]["total"] for code in self.ability_codes
        }
        self.full_reload = {
            code: BREAKDOWNS[code]["reload"] for code in self.ability_codes
        }
        self.set_box_numbers(self.remaining_usage)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = None
        elif self.full(key):
            return self.switch_to(key)
        return False

    def update_ability(self):
        self.load_count[self.mode] = 0
        self.remaining_usage[self.mode] -= 1
        self.mode = None

    def update(self):
        for key in self.load_count:
            if self.remaining_usage[key] > 0:
                if not self.full(key):
                    self.load_count[key] += 0.1

    def full(self, key):
        return self.load_count[key] >= self.full_reload[key]
