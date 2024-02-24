from constants import (
    SPAWN_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    POISON_CODE,
    NUKE_CODE,
    CAPITAL_CODE,
    BURN_CODE,
    FREEZE_CODE,
    RAGE_CODE,
    ZOMBIE_CODE,
    EDGE,
)
from ability import Ability
from ability_validators import (
    new_edge_validator,
    standard_node_attack,
    capital_logic,
    standard_port_node,
    dynamic_edge_own_either,
    no_click,
    unowned_node,
    my_node,
)
from ability_return import make_new_edge
from powerBox_factory import make_boxes


def make_abilities(board):
    boxes = make_boxes()

    return {
        SPAWN_CODE: Ability(SPAWN_CODE, unowned_node, 1, boxes[SPAWN_CODE]),
        BRIDGE_CODE: Ability(
            BRIDGE_CODE,
            new_edge_validator(board.check_new_edge),
            2,
            boxes[BRIDGE_CODE],
            make_new_edge(board.new_edge_id),
        ),
        D_BRIDGE_CODE: Ability(
            D_BRIDGE_CODE,
            new_edge_validator(board.check_new_edge),
            2,
            boxes[D_BRIDGE_CODE],
            make_new_edge(board.new_edge_id),
        ),
        POISON_CODE: Ability(POISON_CODE, standard_node_attack, 1, boxes[POISON_CODE]),
        NUKE_CODE: Ability(NUKE_CODE, standard_node_attack, 1, boxes[NUKE_CODE]),
        CAPITAL_CODE: Ability(CAPITAL_CODE, capital_logic, 1, boxes[CAPITAL_CODE]),
        BURN_CODE: Ability(BURN_CODE, standard_port_node, 1, boxes[BURN_CODE]),
        FREEZE_CODE: Ability(
            FREEZE_CODE, dynamic_edge_own_either, 1, boxes[FREEZE_CODE], None, EDGE
        ),
        RAGE_CODE: Ability(RAGE_CODE, no_click, 0, boxes[RAGE_CODE]),
        ZOMBIE_CODE: Ability(ZOMBIE_CODE, my_node, 1, boxes[ZOMBIE_CODE])
    }