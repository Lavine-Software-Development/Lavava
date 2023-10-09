import pygame as p
from network import Network
from board import Board
from draw import Draw
from map_builder import MapBuilder
from randomGenerator import RandomGenerator
from player import Player
from constants import *
import sys

class Client:
    def __init__(self):
        p.init()

        self.board = None
        self.running = True

        self.n = Network(self.action)
        self.player_num = int(self.n.data[0])
        self.player_count = int(self.n.data[2])
        self.players = {i: Player(COLOR_DICT[i], i) for i in range(self.player_count)}
        self.player = self.players[self.player_num]

        self.board = Board(self.players, self.player_num)
        self.generator = RandomGenerator(int(self.n.data[4:]))

        self.start_game()

        self.d = Draw(self.board, self.player_num)

        self.main_loop()

    def start_game(self):
        for player in self.players.values():
            player.default_values()
        map = MapBuilder(self.generator)
        self.board.reset(map.node_objects, map.edge_objects)
        self.position = None

    def action(self, key, acting_player, data):
        if key == RESTART_GAME_VAL:
            self.start_game()
        elif key == TICK:
            self.tick()
        else:
            self.board.action(key, acting_player, data)

    def tick(self):
        if self.board and not self.board.victor:
            self.board.update()

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
                if event.key in ABILITY_CODES:
                    self.board.select(event.key)
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
                            self.mouse_button_down_event(event.button)

                        elif event.type == p.MOUSEMOTION:
                            self.position = event.pos
                            self.board.hover(event.pos)

            self.d.wipe()
            self.d.blit(self.position)

        self.n.stop()
        self.d.close_window()
        sys.exit()

    def mouse_button_down_event(self, button):
        if self.board.highlighted:
            if (data := self.board.use_ability()) and button != STANDARD_RIGHT_CLICK:
                self.n.send((self.board.mode, self.player_num, *data))
                self.board.update_ability()
            elif id := self.board.click_edge():
                self.n.send((button, self.player_num, id))    

if __name__ == "__main__":
    Client()
