# from abc import ABC, abstractmethod

from drawClasses import IDItem
from typing import Union, Tuple


class AbstractAbilityManager():
    def __init__(self, abilities, events):
        self.abilities = abilities
        self.events = events
        self.mode = None
        self.clicks = []

    def use_event(self, highlight):
        if self.mode:
            self.reset()
        self.clicks.append(highlight.item)
        if self.complete_check(highlight.usage):
            clicks = [click.id for click in self.clicks]
            self.reset()
            return clicks
        return False

    def use_ability(self, highlight):
        if not self.ability:
            return False
        if highlight.usage == self.mode:
            self.clicks.append(highlight.item)
            if self.complete_check():
                clicks = [click.id for click in self.clicks]
                self.reset()
                return clicks
            return False
        return False
    
    def reset(self):
        self.wipe()
        self.mode = None
    
    def wipe(self):
        self.clicks = []

    def switch_to(self, key):
        self.mode = key
        if self.complete_check():
            self.reset()
            return True
        return False
    
    def complete_check(self, event=None):
        if self.ability:
            return self.ability.click_count == len(self.clicks)
        elif event:
            return self.events[event].click_count == len(self.clicks)
        print("ERROR, No ability or event")
        return False

    def select(self, key):
        if self.ability:
            self.wipe()
        if self.mode == key:
            self.mode = None
        elif self.abilities[key].selectable:
            return self.switch_to(key)
        return False
    
    def validate(self, item: IDItem, event: int=0) -> Union[Tuple[IDItem, int], bool]:
        if event:
            if self.events[event].verification_func(self.clicks + [item]):
                return item, event
        elif self.ability and self.mode and item.type == self.ability.click_type and self.ability.verification_func(self.clicks + [item]):
            return item, self.mode
        else:
            for code, ev in self.events.items():
                if item.type == ev.click_type and ev.verification_func([item]):
                    return item, code

        return False

    @property
    def ability(self):
        if self.mode:
            return self.abilities[self.mode]
        return None
 
# class MoneyAbilityManager(AbstractAbilityManager):

#     def select(self, key):
#         if self.ability:
#             self.abilities[self.mode].wipe()
#         if self.mode == key:
#             self.mode = None
#         elif CONTEXT["main_player"].money >= self.costs[key]:
#             return self.switch_to(key)
#         return False

#     def update_ability(self):
#         CONTEXT["main_player"].money -= self.costs[self.mode]
#         if (
#             self.costs[self.mode] > CONTEXT["main_player"].money
#             or self.mode == RAGE_CODE
#         ):
#             self.mode = None

#     @property
#     def display_nums(self):
#         return self.costs


# class ReloadAbilityManager(AbstractAbilityManager):



#     def update_ability(self):
#         self.load_count[self.mode] = 0
#         self.remaining_usage[self.mode] -= 1
#         self.mode = None

#     def full(self, key):
#         return self.load_count[key] >= self.full_reload[key]
    
#     def percent_complete(self, key): 
#         return min(1, self.load_count[key] / self.full_reload[key])
        
#     @property
#     def display_nums(self):
#         return self.remaining_usage
