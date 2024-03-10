import numbers
import collections.abc

class Jsonable:
    def __init__(self, id):
        self.id = id
        self.start_values = set()
        self.tick_values = set()
        self.validate_values = set()

    def to_json(self, included=None):
        if included is None:
            print(self.start_values)
            # print(set(vars(self)) - {'id'})
            included = set(vars(self)) - {'id'}
            
        return {
            self.id: {
                k: v if self.is_basic_type(v) else v.id
                for k, v in vars(self).items()
                if k in included
            }
        }
    
    @property
    def start_json(self):
        return self.to_json(self.start_values)
    
    @property
    def tick_json(self):
        return self.to_json(self.tick_values)
    
    @property
    def validate_json(self):
        return self.to_json(self.validate_values)
    
    def is_basic_type(self, obj):
        return isinstance(obj, (numbers.Number, str, bool, type(None), collections.abc.Sequence, collections.abc.Set, collections.abc.Mapping))