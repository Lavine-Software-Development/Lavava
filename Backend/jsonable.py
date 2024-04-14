from abc import ABC, abstractmethod
import numbers
import collections.abc

from track_change_decorator import track_changes

class JsonableSkeleton(ABC):

    @property
    @abstractmethod
    def json_repr(self):
        pass

# tick values predetermined. Recurse values are also sent every tick
class Jsonable(JsonableSkeleton):
    def __init__(self, id, start_values=set(), recurse_values=set(), tick_values=set()):
        self.id = id
        self.start_values = start_values
        self.tick_values = tick_values
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
                if isinstance(v, Jsonable):
                    dog = getattr(v, recursive_method)
                    #print("here is the dog", dog)
                    final_attributes[k] = dog
                    #print("isinstance(v, Jsonable).", f"Key: {k}")
                elif isinstance(v, dict):
                    final_attributes[k] = {}
                    for id, obj in v.items():
                        final_attributes[k][id] = getattr(obj, recursive_method)
                elif isinstance(v, list):
                    final_attributes[k] = {}
                    for obj in v:
                        final_attributes[k][obj.id] = getattr(obj, recursive_method)
                else:
                    print("Error: Recurse value not a dict or Jsonable", f"Key: {k}")
        
            else:
                if isinstance(v, JsonableSkeleton):
                    final_attributes[k] = v.json_repr
                elif isinstance(v, (dict, set)):
                    final_attributes[k] = list(v)
                elif self.is_basic_type(v):
                    final_attributes[k] = v
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
    def tick_json(self):
        return self.to_json('tick_json', self.tick_values | self.recurse_values)

    def is_basic_type(self, obj):
        return isinstance(obj, (numbers.Number, str, bool, type(None), collections.abc.Sequence, collections.abc.Set))
    
# tick values are tracked. Only send those which have changed since last tick, then erase
@track_changes('tick_values')
class JsonableTracked(Jsonable):
    def __init__(self, id, start_values=set(), recurse_values=set()):
        super().__init__(id, start_values, recurse_values)

    @property
    def tick_json(self):
        tick_json = self.to_json('tick_json', self.tick_values)
        self.tick_values.clear()
        return tick_json