import math

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq))
    
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    return distance

def size_factor(x):
    if x<5:
        return 0
    if x>=200:
        return 1
    return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

class Board:

    def __init__(self, nodes, edges, players):
        self.nodes = nodes
        self.edges = edges
        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.player_dict = {player.id: player for player in players}

    def update(self):
        for spot in self.nodes:
            if spot.owner:
                spot.grow()
                spot.calculate_threatened_score()
            if spot.pressed == 1:
                spot.absorb()
            elif spot.pressed == 3:
                spot.expel()
        for edge in self.edges:
            if edge.pressed:
                edge.flow()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) < 10:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
                return edge.id
        return None

    def stray_from_node(self, node_id, position):
        node = self.id_dict[node_id]
        if math.sqrt((position[0]-node.pos[0])**2 + (position[1]-node.pos[1])**2) >= int(5+size_factor(node.value)*18)+1:
            return True
        return False
