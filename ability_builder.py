from ability import *
from constants import *

class AbilityBuilder:

    def __init__(self, board):
        self.board = board
        self.abilities = {}
        self.build_abilities()

    def build_abilities(self):
        bridge = Bridge(self.board.check_new_edge, self.board.buy_new_edge)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(self.board.remove_node)
        self.abilities[NUKE_CODE] = nuke