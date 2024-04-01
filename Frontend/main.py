from typing import Any, Union, Tuple, get_type_hints
import pygame as py
from constants import BURN_CODE, BURN_TICKS, CAPITAL_CODE, RAGE_CODE, PORT_COUNT, BRIDGE_CODE, NUKE_CODE, SPAWN_CODE, FREEZE_CODE, ZOMBIE_CODE
from highlight import Highlight
from constants import ABILITIES_SELECTED, EDGE_CODE, SPAWN_CODE, STANDARD_RIGHT_CLICK, OVERRIDE_RESTART_CODE, RESTART_CODE, FORFEIT_CODE
from drawClasses import Node, Edge, OtherPlayer, MyPlayer, ReloadAbility, IDItem, State
from port_position import port_angles
from chooseUI import ChooseReloadUI
from draw2 import Draw2
from state_dictionary import state_dict
from SettingsUI import settings_ui
from temp_network import Network
from default_abilities import VISUALS, CLICKS
from default_colors import PLAYER_COLORS
from abilityManager import AbstractAbilityManager
from ability_validators import make_ability_validators, unowned_node
from logic import Logic, distance_point_to_segment
from playerStateEnums import PlayerStateEnum as PSE
from clickTypeEnum import ClickType
from collections import defaultdict

class SafeNestedDict(dict):
    def __getitem__(self, key):
        if key in self:
            # Directly access the dictionary to avoid recursion
            nested_dict = dict.__getitem__(self, key)
            return lambda k: nested_dict[k]
        else:
            # If the key doesn't exist, return a function that just returns the key it was given
            return lambda k: k

def get_adjusted_type_hints(obj):
    hints = get_type_hints(obj)
    adjusted_hints = {}

    for name, type_hint in hints.items():
        # Check if this is an Optional or Union type with NoneType as one of the options
        if hasattr(type_hint, '__origin__') and type_hint.__origin__ is Union and type(None) in type_hint.__args__:
            # Assume there's exactly one non-NoneType, use it directly
            adjusted_hints[name] = next(t for t in type_hint.__args__ if t is not type(None))
        else:
            adjusted_hints[name] = type_hint

    return adjusted_hints

class Main:

    def __init__(self):
        py.init() 

        self.ps = PSE.ABILITY_SELECTION
        self.timer = 60
        self.highlight = Highlight()
        self.effect_visuals = defaultdict(dict)

        self.drawer = Draw2(self.highlight, self.effect_visuals)
        self.can_draw = False

        data, server = self.settings()
        self.network = Network(self.setup, self.update, data, server)
        self.network.receive_board_data()

        self.run()

    def setup(self, start_data):
        pi = start_data["player_id"]
        pc = start_data["player_count"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]
        abi, credits = start_data["abilities"]['values'], start_data["abilities"]['credits']

        self.my_player = MyPlayer(str(pi), PLAYER_COLORS[pi])
        self.players = {id: OtherPlayer(str(id), PLAYER_COLORS[id]) for id in range(pc) if id != pi} | {pi: self.my_player}
        self.nodes = {id: Node(id, ClickType.NODE, n[id]["pos"], n[id]["is_port"], *self.make_ports(n[id]["is_port"]), state_dict[n[id]["state_visual"]], n[id]['value']) for id in n}
        self.edges = {id: Edge(id, ClickType.EDGE, self.nodes[e[id]["from_node"]], self.nodes[e[id]["to_node"]], e[id]["dynamic"]) for id in e}

        self.types = SafeNestedDict({OtherPlayer: self.players, Node: self.nodes, Edge: self.edges, State: state_dict})

        self.logic = Logic(self.nodes, self.edges)

        chosen_boxes = self.choose_abilities(abi, credits)
        self.send_abilities(chosen_boxes)
        self.ability_manager = AbstractAbilityManager(chosen_boxes)

        self.drawer.set_data(self.my_player, self.players, self.nodes.values(), self.edges.values(), self.ability_manager)
        self.can_draw = True

    def settings(self):
        return settings_ui()
    
    def make_ports(self, is_port):
        if is_port:
            return 1, port_angles(PORT_COUNT)
        return 0, []
    
    def update(self, update_data):

        self.ps = update_data['player']['ps']
        self.timer = update_data['timer']

        self.parse(self.ability_manager.abilities, update_data['player']['abilities'])
        self.parse(self.nodes, update_data['board']['nodes'])
        self.parse(self.edges, update_data['board']['edges'])

    #     self.effect_tick()

    # def effect_tick(self):
    #     for key, effect in list(self.effect_visuals.items()):
    #         for node, ticks in list(effect.items()):
    #             if ticks == 0:
    #                 self.effect_visuals[key].pop(node)
    #             else:
    #                 ticks -= 1
    #         if not self.effect_visuals[key]:
    #             self.effect_visuals.pop(key)

    # def update_priority(self, priority):

    #     if PriorityEnum.NEW_EDGE.value in priority:
    #         e = priority[PriorityEnum.NEW_EDGE.value]
    #         new_edges = {id: Edge(id, ClickType.EDGE, self.nodes[e[id]["from_node"]], self.nodes[e[id]["from_node"]], e[id]["dynamic"]) for id in e}
    #         self.edges.update(new_edges)

    #     if PriorityEnum.BURNED_NODE.value in priority:
    #         n = priority[PriorityEnum.BURNED_NODE.value]
    #         self.effect_visuals[PriorityEnum.BURNED_NODE.value].update({self.nodes[id]: BURN_TICKS for id in n})

    def parse(self, items: dict[int, Any], updates, most_complex_item=None):

        deleted_items = set(items) - set(updates)
        new_items = set(updates) - set(items)
        for d in deleted_items:
            items.pop(d)

        if new_items:
            new_edges = {id: Edge(id, ClickType.EDGE, self.nodes[updates[id]["from_node"]], self.nodes[updates[id]["to_node"]], updates[id]["dynamic"]) for id in new_items}
            self.edges.update(new_edges)

        if most_complex_item is None:
            # select an arbitrary item to get the type hints
            most_complex_item = next(iter(items.values()))

        i_t = get_adjusted_type_hints(type(most_complex_item))
        # update_types = {key: self.types[i_t[key]] for key in updates[0] if not is_prim(i_t[key])}
        for u in updates:
            obj = items[u]

            for key, val in updates[u].items():
                if hasattr(obj, key):

                    update_val = val

                    if update_val is not None:

                        desired_type = i_t[key]
                        update_val = self.types[desired_type](val)
                            
                    setattr(obj, key, update_val)

                else:
                    print(f"key {key} not in {type(obj)}")


    def send_abilities(self, boxes):
        self.chosen_abilities = {ab: boxes[ab].remaining for ab in boxes}
        self.network.send({'code': ABILITIES_SELECTED} | {'body': self.chosen_abilities})

    def choose_abilities(self, abi, credits):
        av = make_ability_validators(self.logic, self.my_player)
        boxes = {ab: ReloadAbility(VISUALS[ab], *(CLICKS[ab]), av[ab], abi[ab]['credits'], abi[ab]['reload']) for ab in abi}
        for box in boxes.values():
            if box.visual.color[0] is None:
                box.visual.color = self.my_player.color
        ui = ChooseReloadUI(boxes, credits)
        ui.choose_abilities()
        return {b: v for b, v in boxes.items() if v.remaining > 0}

    def valid_hover(self, position) -> Union[Tuple[IDItem, int], bool]:
        if node := self.find_node(position):
            if self.ps == PSE.START_SELECTION.value:
                if unowned_node([node]):
                    return node, SPAWN_CODE
            elif self.ps == PSE.PLAY.value:
                if self.ability_manager.ability:
                    return self.ability_manager.validate(node)
                
        elif edge := self.find_edge(position):
            if self.ps == PSE.PLAY.value:
                if self.ability_manager.ability:
                    if edge_highlight := self.ability_manager.validate(edge):
                        return edge_highlight
                if edge.controlled_by(self.my_player):
                    return edge, EDGE_CODE
                
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
    
    def mouse_button_down_event(self, button):
        if self.highlight:
            if self.ps == PSE.START_SELECTION.value:
                self.network.send(self.highlight.send_format())
            else:
                if (data := self.ability_manager.use_ability(self.highlight)) \
                        and button != STANDARD_RIGHT_CLICK:
                    self.network.send(self.highlight.send_format(items=data))
                elif self.highlight.type == ClickType.EDGE:
                    self.network.send(self.highlight.send_format(code=button))

    def keydown(self, event):
        if event.key == OVERRIDE_RESTART_CODE:
            self.network.simple_send(RESTART_CODE)
        elif self.ps == PSE.VICTORY:
            if event.key == RESTART_CODE:
                self.network.simple_send(RESTART_CODE)
        elif self.ps == PSE.PLAY.value:
            if event.key in self.ability_manager.abilities:
                if self.ability_manager.select(event.key):
                    self.network.simple_send(event.key)
            elif event.key == FORFEIT_CODE:
                self.network.simple_send(FORFEIT_CODE)
        else:
            print("not playing")

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return
                elif event.type == py.VIDEORESIZE:
                    self.drawer.relocate(event.w, event.h)
                elif event.type == py.MOUSEMOTION:
                    if hover_result := self.valid_hover(event.pos):
                        self.highlight(*hover_result) 
                    else:
                        self.highlight.wipe()
                elif event.type == py.MOUSEBUTTONDOWN:
                    self.mouse_button_down_event(event.button)
                elif event.type == py.KEYDOWN:
                    print("keydown")
                    self.keydown(event)
            if self.can_draw:
                self.drawer.blit(self.ps, self.timer)
                py.display.flip()


class TestMain(Main):

    def settings(self):
        return ["HOST", 1, 2], str(self.get_local_ip())

    def choose_abilities(self, abi, credits):
        av = make_ability_validators(self.logic, self.my_player)
        counts = {CAPITAL_CODE: 1, RAGE_CODE: 2, ZOMBIE_CODE: 2, BURN_CODE: 2}
        return {ab: ReloadAbility(VISUALS[ab], *(CLICKS[ab]), av[ab], abi[ab]['credits'], abi[ab]['reload'], counts[ab]) for ab in counts}

    def get_local_ip(self):
        import socket
        try:
            # Create a socket connection to determine the local IP address
            # The address '8.8.8.8' and port 80 are used here as an example and do not need to be reachable
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None



if __name__ == "__main__":
   TestMain()