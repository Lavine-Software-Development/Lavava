import pygame as p
from network import Network
from board import Board
from draw import Draw
from map_builder import MapBuilder
from randomGenerator import RandomGenerator
from player import Player
from constants import *
from ability_builder import AbilityBuilder
import sys

class Client:
    def __init__(self):
        p.init()

        self.counter = 0
        self.hovered_node = None
        self.board = None
        self.running = True

        self.n = Network(self.action)
        self.player_num = int(self.n.data[0])
        self.player_count = int(self.n.data[2])
        self.players = {i: Player(COLOR_DICT[i], i) for i in range(self.player_count)}
        self.player = self.players[self.player_num]

        self.generator = RandomGenerator(int(self.n.data[4:]))

        self.start_game()
        self.d = Draw(self.board, self.player_num, [self.players[x] for x in self.players], self.abilities)
        self.main_loop()

    def reset_game(self):
        for player in self.players.values():
            player.default_values()
        self.start_game()
        self.d.set_data(self.board, self.player_num, [self.players[x] for x in self.players], self.abilities)

    def start_game(self):
        map = MapBuilder(self.generator)
        self.board = Board(self.players, map.node_objects, map.edge_objects)
        self.abilities = AbilityBuilder(self.board, self.player).abilities
        self.in_draw = False
        self.active = False
        self.closest = None
        self.position = None

    def action(self, key, acting_player, data):
        if key == TICK:
            self.tick()
        elif key in self.abilities:
            new_data = (self.board.id_dict[d] if d in self.board.id_dict else d for d in data)
            self.abilities[key].input(self.players[acting_player], new_data)
        elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
            self.board.id_dict[data[0]].click(self.players[acting_player], key)
        elif key == ELIMINATE_VAL:
            self.eliminate(acting_player)
        elif key == RESTART_GAME_VAL:
            self.reset_game()

    def tick(self):
        if self.board and not self.board.victor:
            self.board.update()

    def eliminate(self, id):
        self.board.eliminate(id)

    def eliminate_send(self):
        self.n.send((ELIMINATE_VAL, self.player_num, 0))

    def restart_send(self):
        self.n.send((RESTART_GAME_VAL, 0, 0))

    def keydown(self, event):
        if event.type == p.KEYDOWN:
            if self.player.victory:
                if event.key == p.K_r:
                    self.restart_send()
            else:
                if event.key in self.abilities:
                    self.abilities[self.player.mode].wipe()
                    self.abilities[event.key].select(self.player)
                elif event.key == p.K_x:
                    self.eliminate_send()

    def main_loop(self):
        while self.running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False

                elif event.type == p.VIDEORESIZE:
                    width, height = event.w, event.h
                    for node in self.board.nodes:
                        node.relocate(width, height)
                    self.d.relocate(width, height)

                if not self.player.eliminated:
                    self.keydown(event)

                    if not self.player.victory:
                        if event.type == p.MOUSEBUTTONDOWN:
                            self.position = event.pos
                            button = event.button
                            self.mouse_button_down_event(button)

                        elif event.type == p.MOUSEMOTION:
                            self.position = event.pos
                            self.mouse_motion_event()

            self.d.wipe()
            self.d.blit(self.position)

        self.n.stop()
        self.d.close_window()
        sys.exit()

    def mouse_button_down_event(self, button):
        if id := self.board.find_node(self.position):
            if data := self.abilities[self.player.mode].use(self.player, self.board.id_dict[id]):
                self.n.send((self.player.mode, self.player_num, *data))
                self.player.mode = DEFAULT_ABILITY_CODE
        elif id := self.board.find_edge(self.position):
            self.n.send((button, self.player_num, id))

    def mouse_motion_event(self):
        if id := self.board.find_node(self.position):
            self.player.highlighted_node = self.board.id_dict[id]
        else:
            self.player.highlighted_node = None

if __name__ == "__main__":
    Client()
