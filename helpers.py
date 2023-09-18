import math
from node import Node
from edge import Edge
from dynamicEdge import DynamicEdge
from resourceNode import ResourceNode
import re
from constants import *

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq))
    
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    return distance

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def do_intersect(p1, q1, p2, q2):

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True
    return False

def angle_between_edges(edge1, edge2):
    dx1 = edge1[1][0] - edge1[0][0]
    dy1 = edge1[1][1] - edge1[0][1]
    dx2 = edge2[1][0] - edge2[0][0]
    dy2 = edge2[1][1] - edge2[0][1]
    
    dot_product = dx1 * dx2 + dy1 * dy2
    magnitude1 = math.sqrt(dx1 ** 2 + dy1 ** 2)
    magnitude2 = math.sqrt(dx2 ** 2 + dy2 ** 2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    angle = math.acos(dot_product / (magnitude1 * magnitude2))
    return math.degrees(angle)

def unwrap_board(s):
    node_to_edge = {}
    dynamic_edges = {}
    nodes = {}
    edges = []

    player = int(s[0])
    player_count = int(s[2])
    s = s[3:]

    node_matches = re.findall(r"Node\((\d+), (-?\d+\.?\d*), (-?\d+\.?\d*)\)", s)
    for match in node_matches:
        id, x, y = int(match[0]), int(match[1]), int(match[2])
        node_to_edge[id] = {'coord': (x, y), 'out': [], 'out_ids': [], 'in': [], 'dynamic': [], 'island': True, 'nearby': False}

    edge_matches = re.findall(r"Edge\((\d+), (\d+), (\d+), (True|False)\)", s)
    for match in edge_matches:
        id1, id2, id3, dynamic = int(match[0]), int(match[1]), int(match[2]), (match[3])
        if dynamic == 'True':
            dynamic_edges[id3] = (id1, id2)
            node_to_edge[id2]["dynamic"].append(id1)
            node_to_edge[id1]["dynamic"].append(id2)
        else:
            node_to_edge[id2]["out"].append(id1)
            node_to_edge[id1]["in"].append(id2)
            node_to_edge[id2]["out_ids"].append(id3)
        node_to_edge[id1]["island"] = False
        node_to_edge[id2]["island"] = False

    network_resources = 0
    island_resources = 0
    for id, data in node_to_edge.items():

        for other_id in data['out'] + data['in'] + data['dynamic']:
            if other_id in nodes and isinstance(nodes[other_id], ResourceNode):
                data['nearby'] = True
                print("found a nearby")
                break
        if data["island"]:
            if island_resources < ISLAND_RESOURCE_COUNT:
                nodes[id] = ResourceNode(id, data['coord'], True)
                island_resources += 1
        elif network_resources < NETWORK_RESOURCE_COUNT and not data['out'] and \
             data['in']:

            nodes[id] = ResourceNode(id, data['coord'], False)
            network_resources += 1
        else:
            nodes[id] = Node(id, data["coord"])

    for id, data in node_to_edge.items():
        for i in range(len(data['out'])):
            edges.append(Edge(nodes[data['out'][i]], nodes[id], data['out_ids'][i]))

    for id, data in dynamic_edges.items():
        if isinstance(nodes[data[0]], ResourceNode):
            edges.append(DynamicEdge(nodes[data[0]], nodes[data[1]], id))
        else:
            edges.append(DynamicEdge(nodes[data[1]], nodes[data[0]], id))

    return (player, (player_count, list(nodes.values()), edges))
    