from node import Node 
from edge import Edge
import time
from make_board import board
import pygame as p
import math

nodes, edges , player = board()

p.init()


SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 1000

size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = p.display.set_mode(size)


p.display.set_caption("Lavava")

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

YELLOW = (255,255,51)


screen.fill(WHITE)
p.display.update()
clock = p.time.Clock()

def draw_arrow(color, start, end, triangle_size=4, spacing=10):
    
    # Calculate the direction vector and its magnitude
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    magnitude = math.sqrt(dx*dx + dy*dy)
    
    # Normalize the direction vector
    dx /= magnitude
    dy /= magnitude
    
    # Calculate the number of triangles based on the spacing
    num_triangles = int(magnitude / spacing)
    
    # Length factor for the two longer edges of the triangle
    length_factor = 1.5
    
    for i in range(1, num_triangles + 1):
        # Calculate the position along the line for each triangle
        pos = (start[0] + i * spacing * dx, start[1] + i * spacing * dy)
        
        # Calculate the points of the triangle
        point1 = pos
        point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
        point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
    
    # Draw the triangle
        p.draw.lines(screen, color, True, [point1, point2, point3])

def blit_edges():

    for edge in edges:

        # linelength = np.sqrt((edge.nodes[0].pos[0]-edge.nodes[1].pos[0])**2+(edge.nodes[0].pos[1]-edge.nodes[1].pos[1])**2)

        # p.draw.line(screen,(50,50,50), edge.to_node.pos, edge.from_node.pos,2)
        # make a perpendicular line to the edge
        draw_arrow((50,50,50), edge.to_node.pos, edge.from_node.pos)
        
 

def blit_nodes():

    for spot in nodes:
        p.draw.circle(screen, spot.color, spot.pos, max(5,min(23,int(3*math.log(spot.value+1)))))
        # if spot.owner==None:
        #     p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)
        # else:
        #     p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)

    p.display.update()

font = p.font.Font(None, 60)
def blit_score():
    p.draw.rect(screen,WHITE,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT/13))
    screen.blit(font.render(str(player.score),True,BLACK),(20,20))
running=True
shitcount = 0

while running:

    for event in p.event.get():

        if event.type == p.QUIT:

            running = False

        elif event.type == p.MOUSEBUTTONDOWN:
             position=event.pos
             for i in range(len(nodes)):
                 if ((position[0] - nodes[i].pos[0])**2 + (position[1] - nodes[i].pos[1])**2) < 10:
                     nodes[i].click(player)
                     player.score-=1000

        # if a click is detected, check if it's on a node. If it is, call click() on that node.
    blit_edges()
    blit_nodes()
    blit_score()
    p.display.update()
    clock.tick()
    shitcount+=1
    if shitcount %10==0:
        for spot in nodes:
            if spot.owner == player:
                spot.value+=1
                player.score+=1




# This is a demonstration of clicking. First node can be selected, others only work if they're neighbor has
# been selected. \/
# player = Player(BLUE)
# owned = []

# for spot in nodes:
#     if spot.click(player):
#         owned.append(spot)

# print(len(owned))


#         # p.draw.circle(screen, BLACK, (position[0],position[1]), 20, 0)
# for spot in owned:
#     spot.grow()