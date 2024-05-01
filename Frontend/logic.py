from collections import defaultdict
import math

class Logic:
    
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def neighbors(self, node):
        neighbors = []
        for edge in self.edges.values():
            try:
                neighbor = edge.other(node)
                neighbors.append(neighbor)
            except ValueError:
                continue
        return neighbors

    def check_new_edge(self, node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in self.edges.values()}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not self.check_all_overlaps((node_to, node_from)):
            return False
        return True
    
    def check_all_overlaps(self, edge):
        edgeDict = defaultdict(set)
        self.nodeDict = {node.id: (node.pos) for node in self.nodes.values()}
        for e in self.edges.values():
            edgeDict[e.to_node.id].add(e.from_node.id)
            edgeDict[e.from_node.id].add(e.to_node.id)

        for key in edgeDict:
            for val in edgeDict[key]:
                if (
                    edge[0] != val
                    and edge[0] != key
                    and edge[1] != val
                    and edge[1] != key
                ):
                    if self.overlap(edge, (key, val)):
                        return False
        return True
    
    def overlap(self, edge1, edge2):
        return do_intersect(
            self.nodeDict[edge1[0]],
            self.nodeDict[edge1[1]],
            self.nodeDict[edge2[0]],
            self.nodeDict[edge2[1]],
        )
    
    def player_capitals(self, player):
        return [node for node in self.nodes.values() if node.owner == player and node.state_name == "capital"]
    
def on_segment(p, q, r):
    return (
        q[0] <= max(p[0], r[0])
        and q[0] >= min(p[0], r[0])
        and q[1] <= max(p[1], r[1])
        and q[1] >= min(p[1], r[1])
    )


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

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    t = max(
        0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq)
    )

    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)

    distance = math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
    return distance

    
