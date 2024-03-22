import pygame as py
from drawClasses import Node, Edge, Port, OtherPlayer, MyPlayer, ReloadAbility
from port_position import opposite
from chooseUI import ChooseReloadUI
from draw2 import Draw2
from state_dictionary import state_dict
from SettingsUI import settings_ui
from temp_network import Network
from default_abilities import VISUALS
from default_colors import PLAYER_COLORS

class Main:

    def __init__(self):
        py.init()

        self.drawer = Draw2()
        self.can_draw = False

        data, server = settings_ui()
        self.network = Network(self.setup, self.update, data, server)
        self.network.receive_board_data()

        self.run()

    # def setup(self):
    #     data, server = settings_ui()
    #     self.network = Network(self.action, self.gs, data, server)

    def make_ports(self, count):
        angles = opposite()[:count]
        return [Port(angle) for angle in angles]
    
    def update(self):
        pass

    def ability_setup(self):
        pass

    def send_abilities(self):
        chosen_abilities = {ab: self.boxes[ab].count for ab in self.boxes if self.boxes[ab].count > 0}
        self.network.send({'type': 'ability_start'} | {'body': chosen_abilities})

    def setup(self, start_data):

        pi = start_data["player_id"]
        pc = start_data["player_count"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]
        abi, credits = start_data["abilities"]['values'], start_data["abilities"]['credits']

        self.my_player = MyPlayer(str(pi), PLAYER_COLORS[pi])
        self.players = {id: OtherPlayer(str(id), PLAYER_COLORS[id]) for id in range(pc) if id != pi} | {pi: self.my_player}
        self.nodes = {id: Node(n[id]["pos"], self.make_ports(n[id]["port_count"]), state_dict[n[id]["state_visual_id"]]) for id in n}
        self.edges = {id: Edge(self.nodes[e[id]["to_node"]], self.nodes[e[id]["from_node"]], e[id]["state"] != 'one-way') for id in e}

        self.boxes = {ab: ReloadAbility(VISUALS[ab], abi[ab]['credits'], abi[ab]['reload']) for ab in abi}
        for box in self.boxes.values():
            if box.visual.color[0] is None:
                box.visual.color = self.my_player.color
        ui = ChooseReloadUI(self.boxes, credits)
        ability_codes = ui.choose_abilities()
        self.send_abilities()

        self.drawer.set_data(self.my_player, self.players, self.nodes.values(), self.edges.values())
        # self.can_draw = True

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return
                elif event.type == py.VIDEORESIZE:
                    self.drawer.relocate(event.w, event.h)
            if self.can_draw:
                self.drawer.blit()
                py.display.flip()


if __name__ == "__main__":
    Main()