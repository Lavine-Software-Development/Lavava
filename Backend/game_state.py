from gameStateEnums import GameStateEnum as GSE

class GameState:
    def __init__(self):
        self._state = GSE.LOBBY

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            print(f"{self._state} to {new_state}")
            self._state = new_state
            
    def next(self):
        if self.state == GSE.LOBBY:
            self.state = GSE.START_SELECTION
        elif self.state == GSE.START_SELECTION:
            self.state = GSE.PLAY
        elif self.state == GSE.PLAY:
            self.state = GSE.END_GAME
        elif self.state == GSE.END_GAME:
            self.state = GSE.GAME_OVER

    @property
    def value(self):
        return self.state.value
