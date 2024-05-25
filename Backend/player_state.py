from jsonable import JsonableSkeleton
from playerStateEnums import PlayerStateEnum as PSE

class PlayerState(JsonableSkeleton):

    def __init__(self):
        self._state = PSE.ABILITY_SELECTION

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            print(f"{self._state} to {new_state}")
            self._state = new_state
            
    def next(self):
        if self.state == PSE.ABILITY_SELECTION:
            self.state = PSE.ABILITY_WAITING
        elif self.state == PSE.ABILITY_WAITING:
            self.state = PSE.START_SELECTION
        elif self.state == PSE.START_SELECTION:
            self.state = PSE.START_WAITING
        elif self.state == PSE.START_WAITING:
            self.state = PSE.PLAY

    @property
    def value(self):
        return self.state.value
    
    @property
    def json_repr(self):
        return self.value

    def eliminate(self):
        self.state = PSE.ELIMINATED

    def victory(self):
        self.state = PSE.VICTORY

    def defeat(self):
        self.state = PSE.LOSER

    def restart(self):
        self.state = PSE.ABILITY_SELECTION
