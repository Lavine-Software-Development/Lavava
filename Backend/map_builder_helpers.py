from constants import (
    ISLAND_RESOURCE_COUNT,
    NETWORK_RESOURCE_COUNT,
    CAPITAL_START_COUNT,
    CAPITAL_ISLAND_COUNT,
    PORT_PERCENTAGE,
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

def create_nodes(node_list: list[tuple]) -> list[PortNode]:
    return [PortNode(node[0], node[1]) for node in node_list]

def random_choose_starter_ports(node_list):
    total_nodes = len(node_list)
    ports_count = round(total_nodes * PORT_PERCENTAGE)
    
    for i, node in enumerate(node_list):
        node.is_port = i < ports_count

def outsider_choose_starter_ports(node_list):
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
    random_choose_starter_ports(sorted_nodes)


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
                and sum(1 for edge in node.edges if (edge.dynamic or edge.to_node == node))
                and capitals < CAPITAL_START_COUNT
                and not any(
                    1 for neigh in node.neighbors if neigh.state_name == "capital"
                )
            ):
                node.set_state("capital", True)
                node.value = CAPITAL_START_SIZE
                capitals += 1
            return_nodes.append(node)
        else:
            if islands < CAPITAL_ISLAND_COUNT and (node.item_type == NODE or node.is_port):
                node.set_state("capital", True)
                node.value = CAPITAL_START_SIZE
                islands += 1
                return_nodes.append(node)
    return return_nodes
