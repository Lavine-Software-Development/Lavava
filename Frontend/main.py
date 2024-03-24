import pygame as py
from constants import GREY
from drawClasses import Node, Edge, Port, OtherPlayer, MyPlayer, ReloadAbility
from port_position import opposite
from chooseUI import ChooseReloadUI
from draw2 import Draw2
from state_dictionary import state_dict
from SettingsUI import settings_ui
from temp_network import Network
from default_abilities import VISUALS, CLICKS
from default_colors import PLAYER_COLORS
from abilityManager import AbstractAbilityManager
from ability_validators import make_ability_validators
from logic import Logic, distance_point_to_segment
from playerStateEnums import PlayerStateEnum as PSE

class Main:

    def __init__(self):
        py.init() 

        self.ps = PSE.ABILITY_SELECTION

        self.drawer = Draw2(self.ps)
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
    
    def update(self, update_data):
        self.ps = update_data['player']['ps']

    def ability_setup(self):
        pass

    def send_abilities(self, boxes):
        self.chosen_abilities = {ab: boxes[ab].count for ab in boxes}
        self.network.send({'type': 'ability_start'} | {'body': self.chosen_abilities})

    def setup(self, start_data):

        pi = start_data["player_id"]
        pc = start_data["player_count"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]
        abi, credits = start_data["abilities"]['values'], start_data["abilities"]['credits']

        self.my_player = MyPlayer(str(pi), PLAYER_COLORS[pi])
        self.players = {id: OtherPlayer(str(id), PLAYER_COLORS[id]) for id in range(pc) if id != pi} | {pi: self.my_player}
        self.nodes = {id: Node(id, n[id]["pos"], self.make_ports(n[id]["port_count"]), state_dict[n[id]["state_visual_id"]], n[id]['value']) for id in n}
        self.edges = {id: Edge(id, self.nodes[e[id]["to_node"]], self.nodes[e[id]["from_node"]], e[id]["state"] != 'one-way') for id in e}

        self.logic = Logic(self.nodes, self.edges)

        av = make_ability_validators(self.logic, self.my_player)

        boxes = {ab: ReloadAbility(VISUALS[ab], *(CLICKS[ab]), av[ab], abi[ab]['credits'], abi[ab]['reload']) for ab in abi}
        for box in boxes.values():
            if box.visual.color[0] is None:
                box.visual.color = self.my_player.color
        ui = ChooseReloadUI(boxes, credits)
        ui.choose_abilities()
        chosen_boxes = {b: v for b, v in boxes.items() if v.count > 0}

        self.send_abilities(chosen_boxes)

        self.ability_manager = AbstractAbilityManager(chosen_boxes, self.my_player.color)

        self.drawer.set_data(self.my_player, self.players, self.nodes.values(), self.edges.values(), self.ability_manager)
        self.can_draw = True

    def valid_hover(self, position):
        if node := self.find_node(position):
            print('node found')
            print(self.ps)
            print(PSE.START_SELECTION)
            if self.ps == PSE.START_SELECTION.value:
                print('start selection')
                if not node.owner:
                    print('no owner')
                    return node, self.my_player.color
            elif self.ps == PSE.PLAY:
                if self.ability_manager.ability:
                    return self.ability_manager.validate(node)
                
        elif edge := self.find_edge(position):
            if self.ps == PSE.PLAY:
                if self.ability_manager.ability:
                    if edge_highlight := self.ability_manager.validate(edge):
                        return edge_highlight
                if edge.controlled_by(self.my_player):
                    return edge, GREY
                
        return False
    
    def find_node(self, position):
        for node in self.nodes.values():
            if (
                (position[0] - node.pos[0]) ** 2 + (position[1] - node.pos[1]) ** 2
            ) <= (node.size) ** 2 + 3:
                return node
        return None

    def find_edge(self, position):
        for edge in self.edges.values():
            if (
                distance_point_to_segment(
                    position[0],
                    position[1],
                    edge.from_node.pos[0],
                    edge.from_node.pos[1],
                    edge.to_node.pos[0],
                    edge.to_node.pos[1],
                )
                < 5
            ):
                return edge
        return None

    def run(self):
        highlight_data = None
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return
                elif event.type == py.VIDEORESIZE:
                    self.drawer.relocate(event.w, event.h)
                elif event.type == py.MOUSEMOTION:
                    highlight_data = self.valid_hover(event.pos)
            if self.can_draw:
                self.drawer.blit(highlight_data)
                py.display.flip()



if __name__ == "__main__":
    Main()