from game import Game
from network import SoloNetwork
from playerManager import SoloPlayerManager
from Backend.randomGenerator import RandomGenerator
import Server.mode as mode
from SettingsUI import settings_ui


class SoloGame(Game):

    def setup(self):
        self.gs = GameState()
        self.network = SoloNetwork(self.action, self.gs, [2])

        self.player_num = 0
        self.pcount = 1
        mode.MODE = self.network.game_type
        self.generator = RandomGenerator(self.network.board_generator_value)

        self.player_manager = SoloPlayerManager(self.gs)


if __name__ == "__main__":
    SoloGame()