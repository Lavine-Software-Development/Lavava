from constants import (
    BREAKDOWNS,
    RAGE_CODE,
    CONTEXT,
    VISUALS,
)
from abc import ABC, abstractmethod
from ability_factory import make_abilities
from chooseUI import ChooseUI, ChooseReloadUI
import mode

class AbstractAbilityManager(ABC):
    def __init__(self, board, gs, ui_class):
        from modeConstants import ABILITY_OPTIONS
        self.boxes = {key: val for key, val in VISUALS.items() if key in ABILITY_OPTIONS[mode.MODE]}
        for box in self.boxes.values():
            if box.color[0] is None:
                box.color = CONTEXT["main_player"].default_color

        UI = ui_class(self.boxes, gs)
        self.ability_codes = UI.choose_abilities()
        self.abilities = make_abilities(board, self.ability_codes)
        self.mode = None

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

    @abstractmethod
    def display_nums(self):
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
        super().__init__(board, gs, ChooseUI)
        self.costs = {code: BREAKDOWNS[code].cost for code in self.ability_codes}

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

    @property
    def display_nums(self):
        return self.costs


class ReloadAbilityManager(AbstractAbilityManager):
    def __init__(self, board, gs):
        super().__init__(board, gs, ChooseReloadUI)
        self.load_count = {code: 0.0 for code in self.ability_codes}
        self.remaining_usage = {
            code: self.boxes[code].count for code in self.ability_codes
        }
        self.full_reload = {
            code: BREAKDOWNS[code].reload for code in self.ability_codes
        }

    def select(self, key):
        if self.ability:
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
    
    @property
    def display_nums(self):
        return self.remaining_usage
