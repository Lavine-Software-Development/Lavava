from game import Game
from network import SoloNetwork
from playerManager import SoloPlayerManager
from randomGenerator import RandomGenerator
import mode


class SoloGame(Game):

    def setup(self):

        self.network = SoloNetwork(self.action)

        self.player_num = 0
        self.pcount = 1
        mode.MODE = self.network.game_type
        self.generator = RandomGenerator(self.network.board_generator_value)

        self.player_manager = SoloPlayerManager()


if __name__ == "__main__":
    SoloGame()