from collections import defaultdict
import numpy as np
from constants import (
    NODE_COUNT,
    EDGE_COUNT,
    ONE_WAY_COUNT,
    MAX_EDGE_LENGTH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MIN_ANGLE,
)
from helpers import do_intersect, angle_between_edges
from edge import Edge
from dynamicEdge import DynamicEdge
from map_builder_helpers import starter_port_nodes, starter_capitals
from random import randint

class MapBuilder:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_objects = []
        self.edge_objects = []
        self.edgeDict = defaultdict(set)

    def build(self):
        self.make_nodes()
        self.make_edges()
        self.convert_to_objects()

    def make_nodes(self):  # assumes global list nodes is empty
        count = 0
        while count < NODE_COUNT:
            spot = [
                randint(
                    int(SCREEN_WIDTH / 10), int(9 * SCREEN_WIDTH / 10)
                ),
                randint(
                    int(SCREEN_HEIGHT / 10), int(9 * SCREEN_HEIGHT / 10)
                ),
            ]

            works = True

            for node in self.nodes:
                if np.sqrt(
                    (spot[0] - node[1][0]) ** 2 + (spot[1] - node[1][1]) ** 2
                ) < 3 * min(SCREEN_WIDTH, SCREEN_HEIGHT) / (NODE_COUNT / 1.5):
                    works = False

            if works:
                self.nodes.append((count, spot))
                count += 1

    def make_edges(self):
        checklist = []
        edge_set = set()

        count = 0

        while count < EDGE_COUNT:
            num1 = randint(0, NODE_COUNT - 1)
            num2 = randint(0, NODE_COUNT - 1)

            while num2 == num1:
                num2 = randint(0, NODE_COUNT - 1)

            combo = (min(num1, num2), max(num1, num2))

            if (
                combo not in edge_set
                and self.nearby(combo)
                and self.check_all_overlaps(combo)
                and self.check_angle_constraints(combo)
            ):
                checklist.append(combo)
                edge_set.add(combo)
                self.edgeDict[num1].add(num2)
                self.edgeDict[num2].add(num1)
                myedge = (
                    self.nodes[num1][0],
                    self.nodes[num2][0],
                    len(self.edges) + NODE_COUNT,
                    count >= ONE_WAY_COUNT,
                )
                self.edges.append(myedge)

                count += 1

    def overlap(self, edge1, edge2):
        return do_intersect(
            self.nodes[edge1[0]][1],
            self.nodes[edge1[1]][1],
            self.nodes[edge2[0]][1],
            self.nodes[edge2[1]][1],
        )

    def check_all_overlaps(self, edge):
        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if (
                    edge[0] != val
                    and edge[0] != key
                    and edge[1] != val
                    and edge[1] != key
                ):
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def check_angle_constraints(self, new_edge):
        p1 = self.nodes[new_edge[0]][1]
        p2 = self.nodes[new_edge[1]][1]

        for key in self.edgeDict:
            for val in self.edgeDict[key]:
                if new_edge[0] == key or new_edge[0] == val:
                    q1 = self.nodes[key][1]
                    q2 = self.nodes[val][1]
                    angle = angle_between_edges((p1, p2), (q1, q2))
                    if angle < MIN_ANGLE:
                        return False
                if new_edge[1] == key or new_edge[1] == val:
                    q1 = self.nodes[key][1]
                    q2 = self.nodes[val][1]
                    angle = angle_between_edges((p1, p2), (q1, q2))
                    if angle < MIN_ANGLE:
                        return False
        return True

    def nearby(self, edge):
        return np.sqrt(
            (self.nodes[edge[0]][1][0] - self.nodes[edge[1]][1][0]) ** 2
            + (self.nodes[edge[0]][1][1] - self.nodes[edge[1]][1][1]) ** 2
        ) < MAX_EDGE_LENGTH * min(SCREEN_WIDTH, SCREEN_HEIGHT) / (NODE_COUNT / 1.5)

    def convert_to_objects(self):
        edges = []

        nodes = self.node_function(self.nodes)

        for edge in self.edges:
            id1, id2, id3, dynamic = edge[0], edge[1], edge[2], edge[3]
            if dynamic:
                edges.append(DynamicEdge(nodes[id1], nodes[id2], id3, True))
            else:
                edges.append(Edge(nodes[id1], nodes[id2], id3, True))

        nodes = self.starter_states(nodes)

        self.edge_objects = edges
        self.node_objects = nodes

    @property
    def starter_states(self):
        return starter_capitals
    
    @property
    def node_function(self):
        return starter_port_nodes