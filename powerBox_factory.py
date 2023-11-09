from powerBox import PowerBox
from constants import *

def make_boxes():
    return {
        'PoisonBox': PowerBox('Poison', PURPLE, 'circle'),
        'FreezeBox': PowerBox('Freeze', LIGHT_BLUE, 'triangle'),
        'NukeBox': PowerBox('Nuke', BLACK, 'square'),
        'BurnBox': PowerBox('Burn', DARK_ORANGE, 'square'),
        'SpawnBox': PowerBox('Spawn', CONTEXT['main_player'].default_color, 'circle', ''),
        'BridgeBox': PowerBox('Bridge', YELLOW, 'triangle', 'A'),
        'D-BridgeBox': PowerBox('D-Bridge', YELLOW, 'circle'),
        'CapitalBox': PowerBox('Capital', PINK, 'star'),
    }