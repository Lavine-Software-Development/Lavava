import pygame as py
from constants import VISUALS
from drawClasses import Node, Edge, Port, OtherPlayer, MyPlayer
from port_position import opposite
from chooseUI import ChooseReloadUI
from draw2 import Draw2
from state_dictionary import state_dict

class Main:

    def __init__(self, start_data: dict):
        py.init()

        # start_data = Network(self.update)
        pi = start_data["player_id"]
        p = start_data["players"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]

        self.drawer = Draw2()

        self.my_player = MyPlayer(str(pi), p[pi])
        self.players = {id: OtherPlayer(str(id), p[id]) for id in p if id != pi} | {pi: self.my_player}
        self.nodes = {id: Node(n[id]["pos"], self.make_ports(n[id]["port_count"]), state_dict[n[id]["state_visual_id"]]) for id in n}
        self.edges = {id: Edge(self.nodes[e[id]["to_node"]], self.nodes[e[id]["from_node"]], e[id]["state"] != 'one-way') for id in e}

        self.boxes = VISUALS
        for box in self.boxes.values():
            if box.color[0] is None:
                box.color = self.my_player.color
        ui = ChooseReloadUI(self.boxes)
        # self.ability_codes = ui.choose_abilities()
        self.ability_codes = []
        self.drawer.set_data(self.my_player, self.players, self.nodes.values(), self.edges.values(), self.ability_codes)

        self.run()

    def make_ports(self, count):
        angles = opposite()[:count]
        return [Port(angle) for angle in angles]
    
    def update(self):
        pass

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return
                elif event.type == py.VIDEORESIZE:
                    self.drawer.relocate(event.w, event.h)

            self.drawer.blit()
            py.display.flip()