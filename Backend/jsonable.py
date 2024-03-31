import numbers
import collections.abc

class Jsonable:
    def __init__(self, id, tick_values=set(), start_values=set()):
        self.id = id
        self.start_values = start_values
        self.tick_values = tick_values
        self.tick_extras = set()

    def to_json(self, included=None):
        if included is None:
            included = set(vars(self)) - {'id'}

        attributes = {k: getattr(self, k) for k in dir(self) 
                      if k in included and not k.startswith('__') and not callable(getattr(self, k))}
            
        return { self.id: 
                    {k: v if self.is_basic_type(v) else v.id
                    for k, v in attributes.items()}
                }
        
    
    @property
    def start_json(self):
        return self.to_json(self.start_values)
    
    @property
    def tick_json(self):
        tick_json = self.to_json(self.tick_values | self.tick_extras)
        self.tick_extras.clear()
        return tick_json

    def is_basic_type(self, obj):
        return isinstance(obj, (numbers.Number, str, bool, type(None), collections.abc.Sequence, collections.abc.Set, collections.abc.Mapping))