from node import Node
from math import atan2, pi
from nodeEffect import Burning
from constants import PORT_NODE, BROWN, BLACK
from random import random
from numpy import sort

class PortNode(Node):
    def __init__(self, id, pos, port_count):
        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.port_count = port_count
        self.ports_angles = []

        self.start_values = self.start_values | {'port_count'}

    def start_serialization(self):
        return (self.pos, self.state_name, self.port_count)

    @property
    def is_port(self):
        return self.port_count != 0

    def new_effect(self, effect_name):
        if effect_name == 'burn':
            return Burning(self.lose_ports)
        else:
            return super().new_effect(effect_name)

    def acceptBridge(self):
        return self.port_count > 0 and 'burn' not in self.effects and self.state.acceptBridge

    def new_edge(self, edge, dir, initial):
        if not initial and edge not in self.edges:
            self.port_count -= 1
        super().new_edge(edge, dir, initial)

    def lose_ports(self):
        self.port_count = 0

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        elif self.is_port:
            return BROWN
        return BLACK
    
    def set_port_angles(self, min_angular_distance=0.4):
        """
        Determines and sets the angles for the ports, ensuring they do not overlap with each other or the edges extending from the node.
        `min_angular_distance` is the minimum angular distance between ports and between ports and edges.
        Returns a list of two angles for the ports.
        """

        # choose two randomly spaced out angles
        first = random.uniform(0, pi)
        second = first + pi
        self.ports_angles = [first, second]

        # edge_angles = self.calculate_edge_angles()
        # valid_angles = self.find_valid_angles(edge_angles, min_angular_distance)

        # opts = []
        # if len(valid_angles) == 1:
        #     opts = valid_angles[0]
        # elif len(valid_angles) > 1:
        #     opts = sorted(valid_angles, key=len, reverse=True)[:2]
        #     if len(opts[0]) > len(opts[1]) * 2:
        #         opts = [opts[0]]

        #     rf = len(opts) // 3
        #     rs = (len(opts) // 3) * 2
        #     self.ports_angles = [opts[rf], opts[rs]]
        # elif len(valid_angles) > 1:

            
        #     self.ports_angles = [opts[0][len(opts[0]) // 2], opts[1][len(opts[1]) // 2]]
            
        # else:
        #     # Fallback if no valid angles found - consider a more sophisticated approach
        #     self.ports_angles = [random.uniform(0, 2 * pi), random.uniform(0, 2 * pi)]

    def calculate_edge_angles(self):
        """
        Calculates and returns a list of angles for all edges connected to this node.
        """
        angles = []
        for edge in self.outgoing.union(self.incoming):
            other_node = edge.opposite(self)
            dx = other_node.pos[0] - self.pos[0]
            dy = other_node.pos[1] - self.pos[1]
            angle = atan2(dy, dx)
            angles.append(angle)
        
        return angles

    def find_valid_angles(self, edge_angles, min_angular_distance):
        """
        Finds valid angles for ports that do not overlap with existing edge angles.
        """
        valid_angles = []
        sub_edges = []
        for angle in [i * min_angular_distance for i in range(int(2 * pi / (min_angular_distance / 4)))]:
            if all(abs(angle - edge_angle) >= min_angular_distance for edge_angle in edge_angles):
                sub_edges.append(angle)
            elif len(sub_edges) >= 1:
                valid_angles.append(sub_edges.copy())
                sub_edges.clear()
        if len(sub_edges) >= 1:
            if len(valid_angles) == 0:
                valid_angles.append(sub_edges.copy())
            else:
                valid_angles[0] = sort(valid_angles[0] + sub_edges.copy())
        return valid_angles

    def find_next_valid_angle(self, base_angle, valid_angles, min_angular_distance):
        """
        Finds the next valid angle for the second port, ensuring minimum angular distance from the first port's angle.
        """
        for angle in valid_angles:
            if abs(angle - base_angle) >= min_angular_distance:
                return angle
        # Fallback, might need a better solution if this scenario is likely
        return base_angle + min_angular_distance