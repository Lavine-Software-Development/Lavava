from playerStateEnums import PlayerStateEnum as PSE

class PlayerState:

    def __init__(self):
        self._state = PSE.WAITING

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            print(f"{self._state} to {new_state}")
            self._state = new_state
            
    def next(self):
        if self.state == PSE.WAITING:
            self.state = PSE.ABILITIES_SELECTED
        elif self.state == PSE.ABILITIES_SELECTED:
            self.state = PSE.START_SELECTED
        elif self.state == PSE.START_SELECTED:
            self.state = PSE.PLAYING

    def eliminate(self):
        self.state = PSE.ELIMINATED

    def victory(self):
        self.state = PSE.VICTORY

    def restart(self):
        self.state = PSE.WAITING
