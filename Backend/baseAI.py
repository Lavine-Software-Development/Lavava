from player import DefaultPlayer, RoyalePlayer, CreditPlayer
from playerStateEnums import PlayerStateEnum as PSE
from abc import abstractmethod, ABC
from node import Node
from constants import SPAWN_CODE, BOT_START_DELAY, FREEZE_CODE, NUKE_CODE, AI_WAIT_TIME, BRIDGE_CODE, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK


type_to_class = {
    "credits": CreditPlayer,
    "elixir": RoyalePlayer
}


class AI(ABC):

    def __init__(self, board, effect_method, event_method, ability_process):
        self.ticks = 0
        self.board = board
        self.effect_method = effect_method
        self.event_method = event_method
        self.auto_attack = False
        self.auto_spread = True
        self.name = "Trainer " + self.trainer_name()
        self.ability_process = ability_process
        self.nodes = {}

    def choose_start(self):
        self.ticks += 1
        if self.ticks == BOT_START_DELAY:
            options = self.get_start_options()
            self.select_start(options)
            self.ability_process(self.id, self.choose_abilities())

    def select_start(self, options):
        for node in options:
            if node.owner is None and node.state_name == "default":
                if self.effect_method(SPAWN_CODE, self.id, [node.id]):
                    break

    def can_afford_ability(self, key):
        return self.abilities[key].can_afford

    def capture_event(self, node, gain):
        if gain:
            self.nodes[node.id] = (node)
        else:
            self.nodes.pop(node.id)

    def bridgable_nodes(self, unclaimed=False):
        accessible = self.board.unclaimed_nodes()
        if unclaimed:
            accessible = accessible & self.board.unclaimed_nodes()
        bridge_options = []
        for my_node in self.nodes:
            for new_node in accessible:
                if self.board.check_new_edge(my_node, new_node.id):
                    bridge_options.append((my_node, new_node.id))
        return bridge_options

    def update(self):
        super().update()
        self.ticks += 1
        if self.ticks % AI_WAIT_TIME == 0:
            self.make_decisions()

    def effect(self, key, data):
        self.effect_method(key, self.id, data)

    def event(self, key, data):
        self.event_method(key, self.id, data)

    # pass 'incoming' or 'outgoing' to get the respective neighbors, or neither to get all
    def neighbor_enemies(self, direction='edges'):
        enemies = {}
        safe = {self, None}
        for node in self.nodes.values():
            for neighbor in node.neighbors_(direction):
                if neighbor.owner not in safe:
                    enemies.add(neighbor)
        return enemies

    def enemy_edges_dictionary(self, direction='edges'):
        enemies = {}
        for id, node in self.nodes.items():
            for edge in getattr(node, direction):
                if edge.contested:
                    enemies[id] = edge
        return enemies
    
    def enemy_edges(self, direction='edges'):
        enemies = set()
        for id, node in self.nodes.items():
            for edge in getattr(node, direction):
                if edge.contested:
                    enemies.add(edge)
        return enemies
    
    def specific_enemy_edges(self, direction='edges', flowing=None, dynamic=None):
        edges = self.enemy_edges(direction)
        return {edge for edge in edges if (flowing is None or edge.flowing == flowing) and (dynamic is None or edge.dynamic == dynamic)}
    
    def freeze_dangerous_edges(self, direction='edges'):
        if self.can_afford_ability(FREEZE_CODE):
            for edge in self.specific_enemy_edges(direction, None, True):
                self.effect(FREEZE_CODE, [edge.id])
                if not self.can_afford_ability(FREEZE_CODE):
                    break

    def nuke_dangerous_nodes(self):
        if self.can_afford_ability(NUKE_CODE):
            for edge in self.specific_enemy_edges('incoming', False, False):
                self.effect(NUKE_CODE, [edge.from_node.id])
                if not self.can_afford_ability(NUKE_CODE):
                    break

    def bridge(self, unclaimed=False):
        if self.can_afford_ability(BRIDGE_CODE):
            for my_node, new_node in self.bridgable_nodes(unclaimed):
                self.effect(BRIDGE_CODE, [my_node, new_node])
                if not self.can_afford_ability(BRIDGE_CODE):
                    break

    def get_backup(self, node):
        for edge in node.incoming:
            if edge.from_node.owner == self:
                self.event(STANDARD_LEFT_CLICK, [edge.id])
        for edge in node.outgoing:
            if edge.dynamic and edge.to_node.owner == self:
                self.event(STANDARD_RIGHT_CLICK, [edge.id])

    def switch_offense_edges(self):
        for edge in self.enemy_edges('outgoing'):
            if not edge.on and edge.to_node.value < edge.from_node.value:
                self.event(STANDARD_LEFT_CLICK, [edge.id])
                self.get_backup(edge.from_node)

    @abstractmethod
    def get_start_options(self) -> list[Node]:
        pass

    @abstractmethod
    def make_decisions(self):
        pass

    @abstractmethod
    def trainer_name(self) -> str:
        pass

    @abstractmethod
    def choose_abilities(self) -> list[int]:
        pass

    def most_outgoing_nodes(self):
        return sorted(self.board.nodes, key=lambda node: len(node.possible_outgoing), reverse=True)


def create_ai(id, settings, board, effect_method, event_method, ability_process):
    class_type = type_to_class[settings["ability_type"]]

    class NothingAI(AI, class_type):

        def get_start_options(self):
            return self.most_outgoing_nodes()
        
        def choose_abilities(self):
            return []
        
        def make_decisions(self):
            pass

        def trainer_name(self):
            return "Stationary"

        def __init__(self):
            class_type.__init__(self, id, settings)
            AI.__init__(self, board, effect_method, event_method, ability_process)

    class IanAI(AI, class_type):

        def get_start_options(self):
            return self.most_outgoing_nodes()
        
        def choose_abilities(self):
            return {str(FREEZE_CODE): 1, str(NUKE_CODE): 1, str(BRIDGE_CODE): 1}
        
        def make_decisions(self):
            self.nuke_dangerous_nodes()
            self.freeze_dangerous_edges('incoming')
            self.freeze_dangerous_edges()
            self.switch_offense_edges()
            self.bridge(True)
            self.bridge()

        def trainer_name(self):
            return "Ian"

        def __init__(self):
            class_type.__init__(self, id, settings)
            AI.__init__(self, board, effect_method, event_method, ability_process)
    
    return IanAI()



    
            
    