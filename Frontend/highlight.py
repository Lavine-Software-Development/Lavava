from dataclasses import dataclass
from typing import Optional
from clickTypeEnum import ClickType
from constants import SPAWN_CODE
from default_abilities import VISUALS
from drawClasses import IDItem


@dataclass
class Highlight:
    item: Optional[IDItem] = None
    usage: Optional[int] = None

    def wipe(self):
        self.item = None
        self.usage = None

    @property
    def color(self):
        if self.usage:
            if self.usage in set(VISUALS) - {SPAWN_CODE}:
                return VISUALS[self.usage].color
        return None
    
    @property
    def type(self):
        if self.item:
            return self.item.type
        return ClickType.BLANK

    def send_format(self, items=None, code=None):
        code = code or self.usage
        if not items:
            items = [self.item.id]
        else:
            print(items)
        return {"code": code, "items": items}
    
    def __call__(self, new_item: IDItem, new_usage: int):
        self.item = new_item
        self.usage = new_usage

    def __bool__(self):
        return bool(self.item)