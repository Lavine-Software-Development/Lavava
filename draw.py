import math
import pygame as py
from dynamicEdge import DynamicEdge

SCREEN_WIDTH = 800
SCREEN_HEIGHT =800
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)

class Draw:
    def __init__(self, board, player, players):
        self.edges = board.edges
        self.nodes = board.nodes
        self.screen = py.display.set_mode(size)
        self.font = py.font.Font(None, 60)
        self.small_font = py.font.Font(None, 45)
        py.display.set_caption("Lavava")
        self.player = player
        self.players = players
        self.highlighted_node = None
        self.temp_line = None

    def size_factor(self, x):
        if x<5:
            return 0
        if x>=200:
            return 1
        return max(min(math.log10(x/10)/2+x/800+0.15,1),0)

    def draw_arrow(self, edge, color, start, end, triangle_size=5, spacing=9):
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_triangles = int((magnitude-10) / spacing)
        
        length_factor = 1.5
        
        for i in range(1, num_triangles + 1):
            pos = (start[0] + i * spacing * dx +5*dx, start[1] + i * spacing * dy+5*dy)
            
            point1 = pos
            point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
            point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)

            if edge.flowing:
                py.draw.polygon(self.screen, color, [point1, point2, point3])               
            else:
                py.draw.lines(self.screen, color, True, [point1, point2, point3])

    def draw_circle(self, edge, color, start, end, circle_radius=3, spacing=6):

        length_factor = 1.5
        triangle_size = 7
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_circles = int((magnitude-10) / spacing)
        
        for i in range(1, num_circles):
            pos = (start[0] + i * spacing * dx+5*dx, start[1] + i * spacing * dy+5*dy)
            if edge.flowing:
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius)
            else:
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius, 1)

        point1 = pos
        point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
        point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
        py.draw.polygon(self.screen, (153, 255, 51), [point1, point2, point3])
        py.draw.lines(self.screen, color, True, [point1, point2, point3])               
                
    def blit_edges(self):
        for edge in self.edges:
            if not isinstance(edge, DynamicEdge):
                self.draw_arrow(edge,edge.color,edge.from_node.pos,edge.to_node.pos)         
            else:
                self.draw_circle(edge,edge.color,edge.from_node.pos,edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:
            py.draw.circle(self.screen, spot.color, spot.pos, spot.size)

    def blit_numbers(self):
        py.draw.rect(self.screen,WHITE,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT/13))
        self.screen.blit(self.font.render(str(int(self.player.money)),True,(205, 204, 0)),(20,20))
        self.screen.blit(self.small_font.render(str(int(self.players[0].count)),True,self.players[0].color),(SCREEN_WIDTH/2 - 30,20))
        self.screen.blit(self.small_font.render("/",True,(0,0,0)),(SCREEN_WIDTH/2 ,20))
        self.screen.blit(self.small_font.render(str(int(self.players[1].count)),True,self.players[1].color),(SCREEN_WIDTH/2 + 20,20))

    def blit_close(self):
        py.draw.line(self.screen,(80,80,80),self.temp_line[0],self.temp_line[1],2)

    def set_close(self, poss):
        self.temp_line = poss

    def wipe(self):
        self.screen.fill(WHITE)

    def highlight_node(self):
        if self.highlighted_node:
            py.draw.circle(self.screen, (0,0,200), self.highlighted_node.pos, self.highlighted_node.size + 5,2)

    def set_highlight(self, node):
        self.highlighted_node = node

    def edge_build(self):
        start=self.temp_line[0]
        end=self.temp_line[1]
        triangle_size=5
        spacing=9
        color = (80, 80, 80)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_triangles = int((magnitude-10) / spacing)
        
        length_factor = 1.5
        
        for i in range(1, num_triangles + 1):
            pos = (start[0] + i * spacing * dx +5*dx, start[1] + i * spacing * dy+5*dy)
            
            point1 = pos
            point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
            point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)

            py.draw.polygon(self.screen, color, [point1, point2, point3])

    def blit(self):
        self.screen.fill(WHITE)
        self.blit_nodes()
        self.blit_edges()
        self.blit_numbers()
        self.highlight_node()
        if self.temp_line:
            if self.player.drawing:
                self.edge_build()
            else:
                self.blit_close()
        py.display.update() 