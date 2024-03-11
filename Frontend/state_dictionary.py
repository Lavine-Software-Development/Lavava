from drawClasses import State, MineState, CapitalState
from constants import DARK_YELLOW, ISLAND_RESOURCE_BUBBLE, RESOURCE_BUBBLE, YELLOW

state_dict = {
    0: State('default'),
    1: State('zombie'),
    2: CapitalState('capital', False),
    3: MineState('mine', RESOURCE_BUBBLE, DARK_YELLOW),
    4: MineState('mine', ISLAND_RESOURCE_BUBBLE, YELLOW)
}