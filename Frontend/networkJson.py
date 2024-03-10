import pygame as p
from constants import VISUALS
from drawClasses import Node, Edge, Port, OtherPlayer, MyPlayer, GameState
from port_position import opposite
from chooseUI import ChooseUI

class Main:

    def __init__(self, start_data: dict):
        p.init()

        # start_data = Network(self.update)
        p = start_data["players"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]

        self.players = {id: OtherPlayer(str(id), p[id]) for id in p}
        self.nodes = {id: Node(n[id]["pos"], self.make_ports(n[id]["port_count"]), n[id]["state_name"]) for id in n}
        self.edges = {id: Edge(self.nodes[e[id]["to_node"]], self.nodes[e[id]["from_node"]], e[id]["state"]) for id in e}

        ui = ChooseUI(VISUALS)
        self.ability_codes = ui.choose_abilities()
        

    def make_ports(self, count):
        angles = opposite()[:count]
        return [Port(angle) for angle in angles]
    
    def update(self):
        pass