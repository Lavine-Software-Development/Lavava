from abc import ABC, abstractmethod
import numbers
import collections.abc
from tracking_decorator.track_changes import track_changes
from tracking_decorator.trash_collections import TrashList

class JsonableSkeleton(ABC):

    @property
    @abstractmethod
    def json_repr(self):
        pass

class JsonableBasic(JsonableSkeleton):
    def __init__(self, id, start_values=set(), recurse_values=set()):
        self.id = id
        self.start_values = start_values
        self.recurse_values = recurse_values

    def to_json(self, recursive_method, included=None):
        if included is None:
            print("Error: included is None")
            return {}

        attributes = {k: getattr(self, k) for k in dir(self) 
                      if k in included and not k.startswith('__') and not callable(getattr(self, k))}
        
        final_attributes = {}
        for k, v in attributes.items():

            if k in self.recurse_values:
                if isinstance(v, JsonableBasic):
                    dog = getattr(v, recursive_method)
                    #print("here is the dog", dog)
                    final_attributes[k] = dog
                    #print("isinstance(v, Jsonable).", f"Key: {k}")
                elif isinstance(v, dict):
                    final_attributes[k] = {}
                    for id, obj in v.items():
                        inner_dict = getattr(obj, recursive_method)
                        if inner_dict or recursive_method in ('start_json', 'full_tick_json'):
                            final_attributes[k][id] = inner_dict
                elif isinstance(v, TrashList):
                    final_attributes[k] = {}
                    for obj in v:
                        inner_dict = getattr(obj, recursive_method)
                        if inner_dict or recursive_method in ('start_json', 'full_tick_json'):
                            final_attributes[k][obj.id] = inner_dict
                    for deleted in v.trash:
                        print("deleted -------------------------------", deleted.id)
                        final_attributes[k][deleted.id] = 'Deleted'
                    v.clear_trash()
                else:
                    print("Error: Recurse value not a dict or Jsonable", f"Key: {k}")
                    print(type(v))
        
            else:
                if isinstance(v, JsonableSkeleton):
                    final_attributes[k] = v.json_repr
                elif isinstance(v, (dict, set)):
                    final_attributes[k] = list(v)
                elif self.is_basic_type(v):
                    final_attributes[k] = v
                elif isinstance(v, numbers.Number):
                    final_attributes[k] = round(v, ndigits=1)
                else:
                    print("Error: base value not basic or a dict or JsonableSkeletable", f"Key: {k}")

        return final_attributes
    
    @property
    def json_repr(self):
        return self.id
    
    @property
    def start_json(self):
        return self.to_json('start_json', self.start_values)
    
    @property
    @abstractmethod
    def tick_json(self):
        pass

    @property
    @abstractmethod
    def full_tick_json(self):
        pass

    def is_basic_type(self, obj):
        return isinstance(obj, (str, bool, type(None), collections.abc.Sequence, collections.abc.Set))

class Jsonable(JsonableBasic):
    def __init__(self, id, start_values=set(), recurse_values=set(), tick_values=set()):
        super().__init__(id, start_values, recurse_values)
        self.tick_values = tick_values

    @property
    def tick_json(self):
        return self.to_json('tick_json', self.tick_values | self.recurse_values)
    
    @property
    def full_tick_json(self):
        return self.to_json('full_tick_json', self.tick_values | self.recurse_values)
    
# tick values are tracked. Only send those which have changed since last tick, then erase
@track_changes()
class JsonableTracked(JsonableBasic):
    def __init__(self, id, start_values=set(), recurse_values=set(), full_values=set()):
        super().__init__(id, start_values, recurse_values)
        self.full_values = full_values

    @property
    def tick_json(self):
        tick_json = self.to_json('tick_json', self.tracked_attributes | self.recurse_values)
        self.clear()
        return tick_json
    
    @property
    def full_tick_json(self):
        return self.to_json('full_tick_json', self.full_values)