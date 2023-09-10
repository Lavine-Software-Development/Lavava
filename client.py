import pygame as p
from network import Network
from board import Board
from draw import Draw

class Client:
    def __init__(self):
        p.init()

        self.counter = 0
        self.hovered_node = None

        self.n = Network(self.action, self.tick, self.eliminate, self.reset_game)
        print("network done")

    def reset_game(self):
        self.player_num = self.n.player
        self.board = Board(*(self.n.board))
        self.players = self.board.player_dict
        self.player = self.players[self.player_num]
        self.d = Draw(self.board, self.player_num, [self.players[x] for x in self.players])

        self.in_draw = False
        self.active = False
        self.closest = None
        self.position = None

        self.main_loop()

    def action(self, id, acting_player, button):
        if id in self.board.id_dict:
            self.board.id_dict[id].click(self.players[acting_player], button)
        else:
            self.board.buy_new_edge(id, acting_player, button)

    def tick(self):
        if not self.board.over:
            self.board.update()

    def eliminate(self, id):
        self.board.eliminate(id)

    def eliminate_send(self):
        self.n.send((-1, self.player_num, -1))

    def restart_send(self):
        self.n.send((-2, self.player_num, -2))

    def keydown(self, event):
        if event.type == p.KEYDOWN:
            if event.key == p.K_a:
                self.player.switch_considering()
            elif event.key == p.K_x:
                self.eliminate_send()
            elif event.key == p.K_r and self.player.victory:
                self.restart_send()

    def main_loop(self):
        while not self.board.over:

            if not self.player.eliminated:

                for event in p.event.get():
                    self.d.wipe()
            
                    if event.type == p.QUIT:
                        self.running = False

                    self.keydown(event)

                    if event.type == p.MOUSEBUTTONDOWN:
                        self.position = event.pos
                        button = event.button
                        self.mouse_button_down_event(button)

                    elif event.type == p.MOUSEMOTION:
                        self.position = event.pos
                        self.mouse_motion_event()

            self.d.blit(self.position)

        
    
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
