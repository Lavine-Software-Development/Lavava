from make_board import board
import pygame as p
import math
from player import Player

nodes, edges = board()
player1 = Player((255,0,0))
player2 = Player((0,0,255))
player = player1

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

def size_factor(x):
    if x<5:
        return 0
    if x>=200:
        return 1
    return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq))
    
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    
    return distance

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
        
        # dx = edge.to_node.pos[0] - edge.from_node.pos[0]
        # dy = edge.to_node.pos[1] - edge.from_node.pos[1]
        # magnitude = math.sqrt(dx*dx + dy*dy)
        
        # dx /= magnitude
        # dy /= magnitude
        # linelength = np.sqrt((edge.nodes[0].pos[0]-edge.nodes[1].pos[0])**2+(edge.nodes[0].pos[1]-edge.nodes[1].pos[1])**2)

        # p.draw.line(screen,(50,50,50), edge.to_node.pos, edge.from_node.pos,2)
        # make a perpendicular line to the edge
        # if edge.directed:
        #     draw_arrow(edge,(50,50,50),
        #                 (edge.from_node.pos[0]+dx*(max(5,min(23,int(3*math.log(edge.from_node.value+1))))-5),edge.from_node.pos[1]+dy*(max(5,min(23,int(3*math.log(edge.from_node.value+1))))-5)),
        #                 (edge.to_node.pos[0]-dx*(max(5,min(23,int(3*math.log(edge.to_node.value+1))))-5),edge.to_node.pos[1]-dy*(max(5,min(23,int(3*math.log(edge.to_node.value+1))))-5)))
        # else:
        #     draw_circle(edge,(50,50,50), (edge.to_node.pos[0]-dx*(max(5,min(23,int(3*math.log(edge.to_node.value+1))))-5),edge.to_node.pos[1]-dy*(max(5,min(23,int(3*math.log(edge.to_node.value+1))))-5)),
        #                 (edge.from_node.pos[0]+dx*(max(5,min(23,int(3*math.log(edge.from_node.value+1))))-5),edge.from_node.pos[1]+dy*(max(5,min(23,int(3*math.log(edge.from_node.value+1))))-5)))
        if edge.directed:
            draw_arrow(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)
                        
        else:
            draw_circle(edge,(50,50,50),edge.from_node.pos,edge.to_node.pos)
        
 

def blit_nodes():

    for spot in nodes:
        p.draw.circle(screen, spot.color, spot.pos, int(5+size_factor(spot.value)*18))
        # if spot.owner==None:
        #     p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)
        # else:
        #     p.draw.circle(screen, spot.color, spot.pos, spot.value + 5)


font = p.font.Font(None, 60)

def blit_score():
    p.draw.rect(screen,WHITE,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT/13))
    screen.blit(font.render(str(int(player.score)),True,player.color),(20,20))

running=True
shitcount = 0

holding_down = [False, False]
holding_timer = 0
clicked_node = None
held_edge = None

while running:

    if holding_down[0] and not holding_down[1]:
        if shitcount-holding_timer >=200:
            holding_down[1]=True
            clicked_node.pressed = holding_down[0]

    for event in p.event.get():

        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:
            if event.key == p.K_a:
                if player == player1:
                    player = player2
                else:
                    player = player1

        elif event.type == p.MOUSEBUTTONDOWN:
             position=event.pos
             button = event.button
             for i in range(len(nodes)):
                 if ((position[0] - nodes[i].pos[0])**2 + (position[1] - nodes[i].pos[1])**2) < 10:
                    clicked_node = nodes[i]
                    if clicked_node.owner == player:
                        holding_down[0] = button
                        holding_timer = shitcount
                    else:
                        clicked_node.click(player)
                    break

             if not clicked_node:

                for j in range(len(edges)):
                    dist = distance_point_to_segment(position[0],position[1],edges[j].from_node.pos[0],edges[j].from_node.pos[1],edges[j].to_node.pos[0],edges[j].to_node.pos[1])
                    if dist < 5:
                        held_edge = edges[j].click(button, player)
                        break

        elif event.type == p.MOUSEMOTION:
             position=event.pos
             if clicked_node:
                 if math.sqrt((position[0]-clicked_node.pos[0])**2 + (position[1]-clicked_node.pos[1])**2) >= int(5+size_factor(clicked_node.value)*18)+1:
                     holding_down = [False,False]
                     clicked_node.pressed = False
                     clicked_node = None
            # equivalent for held edge
                     
        elif event.type == p.MOUSEBUTTONUP:
            holding_down=[False,False]
            held_edge = None
            if clicked_node:
                clicked_node.pressed = False
                clicked_node = None
        # if a click is detected, check if it's on a node. If it is, call click() on that node.
    screen.fill(WHITE)
    blit_edges()
    blit_nodes()
    blit_score()
    p.display.update()
    clock.tick()
    shitcount+=1
    if shitcount %10==0:
        for spot in nodes:
            spot.calculate_threatened_score()
            if spot.owner:
                spot.grow()
            if spot.pressed == 1:
                spot.absorb()
            elif spot.pressed == 3:
                spot.expel()
        if held_edge:
            held_edge.flow()