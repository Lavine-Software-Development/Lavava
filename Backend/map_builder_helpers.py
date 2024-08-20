from constants import (
    ISLAND_RESOURCE_COUNT,
    NETWORK_RESOURCE_COUNT,
    NODE,
    DYNAMIC_EDGE,
    CAPITAL_START_SIZE
)
from node import Node
from portNode import PortNode

def starter_default_nodes(node_list):
    nodes = []
    for node in node_list:
        nodes.append(Node(node[0], node[1]))
    return nodes

def create_nodes(node_class, node_list: list[tuple], growth_rate, transfer_rate, default_full_size, structures_grow) -> list[PortNode]:
    return [node_class(node[0], node[1], growth_rate, transfer_rate, default_full_size, structures_grow) for node in node_list]

def random_choose_accessible_nodes(node_list, percentage, settings):
    total_nodes = len(node_list)
    ports_count = round(total_nodes * percentage)
    
    for i, node in enumerate(node_list):
        node.bridge_access(i < ports_count, settings)

def outsider_choose_accessible_nodes(node_list, percentage, settings):
    # Calculate possible_incoming_count for each node
    incoming_counts = {}
    for node in node_list:
        incoming_counts[node] = sum(
            1 for edge in node.edges 
            if edge.item_type == DYNAMIC_EDGE or edge.to_node == node
        )
    
    # Sort nodes based on possible_incoming_count (ascending order)
    sorted_nodes = sorted(node_list, key=lambda node: incoming_counts[node])
    
    # Calculate the number of ports needed
    random_choose_accessible_nodes(sorted_nodes, percentage, settings)


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


def starter_capitals(nodes, settings):
    return_nodes = []
    capitals = 0
    islands = 0
    for node in nodes:
        if len(node.edges) != 0:
            if (
                (node.item_type == NODE or not node.is_port)
                and sum(1 for edge in node.edges if (edge.dynamic or edge.to_node == node))
                and capitals < settings["starting_land_capitals"]
                and not any(
                    1 for neigh in node.neighbors if neigh.state_name == "capital"
                )
            ):
                node.set_state("capital", True)
                node.value = CAPITAL_START_SIZE
                capitals += 1
            return_nodes.append(node)
        else:
            if islands < settings["starting_island_capitals"] and (node.item_type == NODE or node.is_port):
                node.set_state("capital", True)
                node.value = CAPITAL_START_SIZE
                islands += 1
                return_nodes.append(node)
    return return_nodes

def just_remove_lonely_nodes(nodes, settings):
    return [node for node in nodes if len(node.edges) > 0]
