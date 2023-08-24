import pygame as p
import math
from network import Network

p.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = p.display.set_mode(size)
p.display.set_caption("Lavava")

WHITE = (255, 255, 255)

n = Network()
player = n.getPlayer()
board = n.getBoard()
nodes = board.nodes
edges = board.edges

def size_factor(x):
    if x<5:
        return 0
    if x>=200:
        return 1
    return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

def draw_arrow(edge, color, start, end, triangle_size=5, spacing=9):
    
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
            p.draw.lines(screen, color, True, [point1, point2, point3])
        else:
            p.draw.polygon(screen, (120,120,120), [point1, point2, point3])

def draw_circle(edge, color, start, end, circle_radius=3, spacing=6):
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    magnitude = math.sqrt(dx*dx + dy*dy)
    
    dx /= magnitude
    dy /= magnitude
    
    num_circles = int((magnitude-10) / spacing)
    
    for i in range(1, num_circles + 1):
        pos = (start[0] + i * spacing * dx+5*dx, start[1] + i * spacing * dy+5*dy)
        if edge.flowing:
            p.draw.circle(screen, color, (int(pos[0]), int(pos[1])), circle_radius, 1)
        else:
            p.draw.circle(screen, (120,120,120), (int(pos[0]), int(pos[1])), circle_radius)
            
def blit_edges():

    for edge in edges:
        if edge.directed:
            draw_arrow(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)
                        
        else:
            draw_circle(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)
        
 

def blit_nodes():

    for spot in nodes:
        p.draw.circle(screen, spot.color, spot.pos, int(5+size_factor(spot.value)*18))

running = True

while running:

    for event in p.event.get():

        if event.type == p.QUIT:
            running = False

    screen.fill(WHITE)
    blit_edges()
    blit_nodes()
    p.display.update()