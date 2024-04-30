def trash_collection(cls):
    if isinstance(cls, list):
        return TrashList(cls)
    elif isinstance(cls, set):
        return TrashSet(cls)
    elif isinstance(cls, dict):
        return TrashDict(cls)
    else:
        # error handling
        print("Invalid class type")


class TrashDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trash = {}

    def __delitem__(self, key):
        self.trash[key] = self[key]
        super().__delitem__(key)

    def pop(self, key, *args):
        value = super().pop(key, *args)
        self.trash[key] = value
        return value

    def popitem(self):
        key, value = super().popitem()
        self.trash[key] = value
        return key, value

    def clear_trash(self):
        self.trash.clear()

class TrashList(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.trash = set()

    def remove(self, value):
        self.trash.add(value)
        super().remove(value)

    def pop(self, index=-1):
        item = super().pop(index)
        self.trash.add(item)
        return item

    def __delitem__(self, key):
        if isinstance(key, slice):
            removed_items = self[key]
            for idx, val in enumerate(removed_items, start=key.start if key.start else 0):
                self.trash.add(val)
        else:
            self.trash.add(self[key])
        super().__delitem__(key)

    def clear_trash(self):
        self.trash.clear()

class TrashSet(set):
    def __init__(self, *args):
        super().__init__(*args)
        self.trash = set()

    def remove(self, element):
        super().remove(element)
        self.trash.add(element)

    def discard(self, element):
        if element in self:
            self.trash.add(element)
        super().discard(element)

    def clear_trash(self):
        self.trash.clear()
