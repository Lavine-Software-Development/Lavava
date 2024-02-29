from game import Game
from game_state import GameState
from network import SoloNetwork
from playerManager import SoloPlayerManager
from randomGenerator import RandomGenerator
import mode
from SettingsUI import settings_ui


class SoloGame(Game):

    def setup(self):
        data = settings_ui()
        self.gs = GameState()
        self.network = SoloNetwork(self.action, self.gs, data)

        self.player_num = 0
        self.pcount = 1
        mode.MODE = self.network.game_type
        self.generator = RandomGenerator(self.network.board_generator_value)

        self.player_manager = SoloPlayerManager(self.gs)


if __name__ == "__main__":
    SoloGame()