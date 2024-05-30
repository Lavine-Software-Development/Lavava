from drawClasses import IDItem
from typing import Union, Tuple


class AbstractAbilityManager():
    def __init__(self, abilities, events):
        self.abilities = abilities
        self.events = events
        self.mode = None
        self.backup_mode = None
        self.clicks = []

    def use_event(self, highlight):
        if self.mode and self.mode != highlight.usage:
            self.backup_reset()
        self.mode = highlight.usage
        self.clicks.append(highlight.item)
        if self.complete_check(highlight.usage):
            clicks = [click.id for click in self.clicks]
            self.backup_reset()
            return clicks
        return False

    def use_ability(self, highlight):
        if self.ability:
            if highlight.usage == self.mode and highlight.item.type == self.ability.click_type:
                self.clicks.append(highlight.item)
                return True
        return False
    
    def complete_ability(self):
        if self.complete_check():
            clicks = [click.id for click in self.clicks]
            self.reset()
            return clicks
        return False
    
    def backup_reset(self):
        if self.backup_mode:
            self.mode = self.backup_mode
            self.backup_mode = None
            self.wipe()
        else:
            if self.ability:
                self.backup_mode = self.mode
            self.reset()
    
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
        if self.mode:
            self.wipe()
        if self.mode == key:
            self.mode = None
        elif self.abilities[key].selectable:
            return self.switch_to(key)
        return False
    
    def validate(self, item: IDItem) -> Union[Tuple[IDItem, int], bool]:
        if self.event and item.type == self.event.click_type and self.event.verification_func(self.clicks + [item]):
            return item, self.mode
        elif self.ability and item.type == self.ability.click_type and self.ability.verification_func(self.clicks + [item]):
            return item, self.mode
        else:
            for code, ev in self.events.items():
                if item.type == ev.click_type and ev.verification_func([item]):
                    return item, code
                
        return False

    @property
    def ability(self):
        if self.mode in self.abilities:
            return self.abilities[self.mode]
        return None
    
    @property
    def event(self):
        if self.mode in self.events:
            return self.events[self.mode]
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
