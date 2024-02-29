from gameStateEnums import GameStateEnum as GSE

class GameState:

    def __init__(self):
        self._state = GSE.SETTINGS_SELECTION

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            print(f"{self._state} to {new_state}")
            self._state = new_state
            
    def next(self):
        if self.state == GSE.SETTINGS_SELECTION:
            self.state = GSE.BUILING_GAME
        elif self.state == GSE.BUILING_GAME:
            self.state = GSE.ABILITY_SELECTION
        elif self.state == GSE.ABILITY_SELECTION:
            self.state = GSE.START_SELECTION
        elif self.state == GSE.START_SELECTION:
            self.state = GSE.PLAY

    def restart(self):
        self.state = GSE.BUILING_GAME

    def killed_or_forfeit(self):
        self.state = GSE.ELIMINATED

    def win_or_lose(self):
        self.state = GSE.GAME_OVER
