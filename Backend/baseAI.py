from player import DefaultPlayer, RoyalePlayer, CreditPlayer
from playerStateEnums import PlayerStateEnum as PSE
from abc import abstractmethod, ABC
from node import Node
from constants import SPAWN_CODE, BOT_START_DELAY


type_to_class = {
    "credits": CreditPlayer,
    "royale": RoyalePlayer
}


class BaseAI(ABC):

    def __init__(self, board, effect_method, event_method):
        self.ticks = 0
        self.board = board
        self.effect_method = effect_method
        self.event_method = event_method

    def choose_start(self):
        self.ticks += 1
        if self.ticks == BOT_START_DELAY:
            options = self.get_start_options()
            self.select_start(options)

    def select_start(self, options):
        for node in options:
            if node.owner is None:
                if self.effect_method(SPAWN_CODE, self.id, [node.id]):
                    break

    @abstractmethod
    def get_start_options(self) -> list[Node]:
        pass

    @abstractmethod
    def make_decisions(self):
        pass

    def update(self):
        super().update()
        self.make_decisions()

    def most_outgoing_nodes(self):
        return sorted(self.board.nodes, key=lambda node: len(node.possible_outgoing), reverse=True)


def create_ai(id, settings, board, effect_method, event_method):
    class_type = type_to_class[settings["ability_type"]]

    class IanAI(BaseAI, class_type):

        def get_start_options(self):
            return self.most_outgoing_nodes()
        
        def make_decisions(self):
            pass

        def __init__(self):
            BaseAI.__init__(self, board, effect_method, event_method)
            class_type.__init__(self, id, settings)
            self.name = "Trainer Ian"
    
    return IanAI()



    
            
    