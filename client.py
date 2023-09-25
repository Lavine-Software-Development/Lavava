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

        self.counter = 0
        self.hovered_node = None
        self.board = None
        self.running = True

        self.n = Network(self.action, self.tick, self.eliminate, self.reset_game)
        self.player_num = int(self.n.data[0])
        self.player_count = int(self.n.data[2])
        self.players = {i: Player(COLOR_DICT[i], i) for i in range(self.player_count)}
        self.player = self.players[self.player_num]

        self.generator = RandomGenerator(int(self.n.data[4:]))

        self.start_game()
        self.d = Draw(self.board, self.player_num, [self.players[x] for x in self.players])
        self.main_loop()

    def reset_game(self):
        self.start_game()
        self.d.set_data(self.board, self.player_num, [self.players[x] for x in self.players])
        for player in self.players.values():
            player.default_values()

    def start_game(self):
        map = MapBuilder(self.generator)
        self.board = Board(self.players, map.node_objects, map.edge_objects)

        self.in_draw = False
        self.active = False
        self.closest = None
        self.position = None

    def action(self, id, acting_player, button):
        if id in self.board.id_dict:
            self.board.id_dict[id].click(self.players[acting_player], button)
        else:
            self.board.buy_new_edge(id, acting_player, button)

    def tick(self):
        if self.board and not self.board.victor:
            self.board.update()

    def eliminate(self, id):
        self.board.eliminate(id)

    def eliminate_send(self):
        self.n.send((-1, self.player_num, -1))

    def restart_send(self):
        self.n.send((-2, -2, -2))

    def keydown(self, event):
        if event.type == p.KEYDOWN:
            if self.player.victory:
                if event.key == p.K_r:
                    self.restart_send()
            else:
                if event.key == p.K_a:
                    self.player.switch_considering()
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
            if self.player.considering_edge:
                if self.player.new_edge_started():
                    if new_edge_id := self.board.check_new_edge(self.player.new_edge_start.id, id):
                        self.n.send((new_edge_id, self.player.new_edge_start.id, id))
                        self.player.switch_considering()
                else:
                    if self.board.id_dict[id].owner == self.player:
                        self.player.new_edge_start = self.board.id_dict[id]
            else:
                self.n.send((id, self.player_num, button))
        elif id := self.board.find_edge(self.position):
            self.n.send((id, self.player_num, button))
        elif self.player.considering_edge:
            self.player.new_edge_start = None

    def mouse_motion_event(self):
        if id := self.board.find_node(self.position):
            self.player.highlighted_node = self.board.id_dict[id]
        else:
            self.player.highlighted_node = None

if __name__ == "__main__":
    Client()
