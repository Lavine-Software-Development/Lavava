from constants import (
    ISLAND_RESOURCE_COUNT,
    NETWORK_RESOURCE_COUNT,
    CAPITAL_START_COUNT,
    CAPITAL_ISLAND_COUNT,
    PORT_LAYOUT,
    NODE
)
from node import Node
from portNode import PortNode

def starter_default_nodes(node_list):
    nodes = []
    for node in node_list:
        nodes.append(Node(node[0], node[1]))
    return nodes


def starter_port_nodes(node_list):
    nodes = []
    port_list_count = len(PORT_LAYOUT)
    for index, node in enumerate(node_list):
        port_list_index = index % port_list_count
        nodes.append(PortNode(node[0], node[1], PORT_LAYOUT[port_list_index]))
    return nodes


def starter_mines(nodes):
    return_nodes = []
    island_mines = 0
    network_mines = 0
    for node in nodes:
        if len(node.edges) == 0:
            if island_mines < ISLAND_RESOURCE_COUNT:
                node.set_state("mine", True)
                return_nodes.append(node)
                island_mines += 1
        else:
            if (
                sum(1 for edge in node.incoming if not edge.dynamic)
                and network_mines < NETWORK_RESOURCE_COUNT
                and not any(1 for neigh in node.neighbors if neigh.state_name == "mine")
            ):
                node.set_state("mine", False)
                network_mines += 1
            return_nodes.append(node)

    return return_nodes


def starter_capitals(nodes):
    return_nodes = []
    capitals = 0
    islands = 0
    for node in nodes:
        if len(node.edges) != 0:
            if (
                (node.item_type == NODE or not node.is_port)
                and sum(1 for edge in node.incoming if not edge.dynamic)
                and capitals < CAPITAL_START_COUNT
                and not any(
                    1 for neigh in node.neighbors if neigh.state_name == "capital"
                )
            ):
                node.set_state("capital", True)
                node.value = 50
                capitals += 1
            return_nodes.append(node)
        else:
            if islands < CAPITAL_ISLAND_COUNT and (node.item_type == NODE or node.is_port):
                node.set_state("capital", True)
                node.value = 50
                islands += 1
                return_nodes.append(node)
    return return_nodes
