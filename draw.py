import math
import pygame as py

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)

class Draw:
    def __init__(self, edges, nodes, player):
        self.edges = edges
        self.nodes = nodes
        self.screen = py.display.set_mode(size)
        self.font = py.font.Font(None, 60)
        py.display.set_caption("Lavava")
        self.player = player

    def size_factor(self, x):
        if x<5:
            return 0
        if x>=200:
            return 1
        return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

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
                py.draw.lines(self.screen, color, True, [point1, point2, point3])
            else:
                py.draw.polygon(self.screen, (120,120,120), [point1, point2, point3])

    def draw_circle(self, edge, color, start, end, circle_radius=3, spacing=6):
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_circles = int((magnitude-10) / spacing)
        
        for i in range(1, num_circles + 1):
            pos = (start[0] + i * spacing * dx+5*dx, start[1] + i * spacing * dy+5*dy)
            if edge.flowing:
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius, 1)
            else:
                py.draw.circle(self.screen, (120,120,120), (int(pos[0]), int(pos[1])), circle_radius)
                
    def blit_edges(self):
        for edge in self.edges:
            if edge.directed:
                self.draw_arrow(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)         
            else:
                self.draw_circle(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:
            py.draw.circle(self.screen, spot.color, spot.pos, int(5+self.size_factor(spot.value)*18))

    def blit_score(self):
        py.draw.rect(self.screen,WHITE,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT/13))
        self.screen.blit(self.font.render(str(int(self.player.score)),True,self.player.color),(20,20))

    def blit(self):
        self.screen.fill(WHITE)
        self.blit_nodes()
        self.blit_edges()
        self.blit_score()
        py.display.update() 