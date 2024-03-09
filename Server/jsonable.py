class Jsonable:
    def __init__(self, id):
        self.id = id
        self.start_data = set()
        self.tick_data = set()
        self.validate_data = set()

    def to_json(self, included=None):
        if included is None:
            included = set(vars(self)) - {'id'}
            
        return {
            self.id: {
                k: v if isinstance(v, (int, float, str, bool)) else v.id
                for k, v in vars(self).items()
                if k in included
            }
        }
    
    @property
    def start_json(self):
        return self.to_json(self.start_data)
    
    @property
    def tick_json(self):
        return self.to_json(self.tick_data)
    
    @property
    def validate_json(self):
        return self.to_json(self.validate_data)