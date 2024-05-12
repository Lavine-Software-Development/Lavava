class Event():
    def __init__(self, validation_func, effect_func):
        self.validation_func = validation_func
        self.effect_func = effect_func

    def can_use(self, player, data):
        return self.validation_func(player, data)
    
    def use(self, player, data):
        self.effect_func(player, data)