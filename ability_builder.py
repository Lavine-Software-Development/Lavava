from ability import *
from constants import *

class AbilityBuilder:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.abilities = {}
        self.build_abilities()

    def build_abilities(self):
        spawn = Spawn(self.player.color)
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(self.board.check_new_edge, self.board.buy_new_edge)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(self.board.remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison()
        self.abilities[POISON_CODE] = poison