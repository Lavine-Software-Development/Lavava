class Event():
    def __init__(self, id, validation_func, effect_func):
        self.validation_func = validation_func
        self.effect_func = effect_func

        super().__init__(id)

    def can_use(self, data):
        return self.validation_func(data)
    
    def use(self, data):
        self.effect_func(data)