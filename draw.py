import math
import pygame as py
from dynamicEdge import DynamicEdge
from resourceNode import ResourceNode
from constants import *

class Draw:
    def __init__(self, board, player_num, players, abilities):
        self.set_data(board, player_num, players, abilities)
        self.screen = py.display.set_mode(size, py.RESIZABLE)
        self.font = py.font.Font(None, 60)
        self.small_font = py.font.Font(None, 45)
        self.highlighted_node = None
        self.temp_line = None
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        py.display.set_caption("Lavava")

    def set_data(self, board, player_num, players, abilities):
        self.board = board
        self.edges = board.edges
        self.nodes = board.nodes
        self.player = players[player_num]
        self.players = players
        self.abilities = abilities

    def _generate_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)

    def _generate_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)

    def draw_button(self, shape, color, name, cost, letter, position, selected):
        btn_size = ABILITY_SIZE * self.height
        border_thickness = 5

        if selected:
            lighter_color = self._generate_lighter_color(color)
            py.draw.rect(self.screen, lighter_color, 
                        (position[0] - border_thickness, 
                        position[1] - border_thickness, 
                        btn_size + 2 * border_thickness, 
                        btn_size + 2 * border_thickness))

        # Draw the button background
        darker_color = self._generate_darker_color(color)
        py.draw.rect(self.screen, darker_color, (position[0], position[1], btn_size, btn_size))

        # Drawing shapes inside
        lighter_color = self._generate_lighter_color(color)
        if shape == "circle":
            py.draw.circle(self.screen, lighter_color, (position[0] + btn_size // 2, position[1] + btn_size // 2), btn_size // 3)
        elif shape == "square":
            py.draw.rect(self.screen, lighter_color, (position[0] + btn_size // 4, position[1] + btn_size // 4, btn_size // 2, btn_size // 2))
        elif shape == "triangle":
            points = [
                (position[0] + btn_size // 2, position[1] + btn_size // 4),
                (position[0] + btn_size // 4, position[1] + 3 * btn_size // 4),
                (position[0] + 3 * btn_size // 4, position[1] + 3 * btn_size // 4)
            ]
            py.draw.polygon(self.screen, lighter_color, points)
        elif shape == "hexagon":
            angle = 2 * math.pi / 6
            points = []
            for i in range(6):
                x = position[0] + btn_size // 2 + btn_size // 3 * math.cos(i * angle)
                y = position[1] + btn_size // 2 + btn_size // 3 * math.sin(i * angle)
                points.append((x, y))
            py.draw.polygon(self.screen, lighter_color, points)

        # Drawing text (name and cost)
        font = py.font.Font(None, int(self.height * ABILITY_FONT))

        letter_text = font.render(letter, True, BLACK)  # White color
        self.screen.blit(letter_text, (position[0] + (btn_size - letter_text.get_width()) // 2, 
                                   position[1] + (btn_size - letter_text.get_height()) // 2))

        text = font.render(name, True, WHITE)
        self.screen.blit(text, (position[0] + (btn_size - text.get_width()) // 2, position[1] + btn_size - (FONT_GAP * self.height)))

        cost_text = font.render(f"{cost}", True, WHITE)
        self.screen.blit(cost_text, (position[0] + 10, position[1] + 10))

    def draw_buttons(self):
        y_position = int(ABILITY_START_HEIGHT * self.height)
        for btn_data in self.abilities.values():
            selected = self.player.mode == btn_data.key or (self.player.mode == 'default' and btn_data.key == 2)
            self.draw_button(btn_data.shape, btn_data.color, btn_data.name, btn_data.cost, btn_data.letter, (self.width -  int(ABILITY_GAP * self.height), y_position), selected)
            y_position += int(ABILITY_GAP * self.height) # Vertical gap between buttons

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
            if edge.poisoned:
                py.draw.lines(self.screen, PURPLE, True, [point1, point2, point3])

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
            if edge.poisoned:
                py.draw.circle(self.screen, PURPLE, (int(pos[0]), int(pos[1])), circle_radius, 1)

        point1 = pos
        point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
        point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
        py.draw.polygon(self.screen, (153, 255, 51), [point1, point2, point3])
        py.draw.lines(self.screen, color, True, [point1, point2, point3])               
                
    def blit_edges(self):
        for edge in self.edges:
            if edge.state == 'one-way':
                self.draw_arrow(edge,edge.color,edge.from_node.pos,edge.to_node.pos)         
            else:
                self.draw_circle(edge,edge.color,edge.from_node.pos,edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:
            if spot.state == 'resource':
                if spot.bubble_owner != None:
                    angle1 = 2 * math.pi * (spot.bubble_size / spot.bubble)
                    py.draw.arc(self.screen, spot.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), -angle1 / 2, angle1 / 2, spot.size)
                    py.draw.arc(self.screen, spot.bubble_owner.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), angle1 / 2, -angle1 / 2 + 2 * math.pi, spot.size)
                else:
                    py.draw.circle(self.screen, GREY, spot.pos, spot.size)
                py.draw.circle(self.screen, spot.ring_color, spot.pos, spot.size + 6, 6)
            else:
                py.draw.circle(self.screen, spot.color, spot.pos, spot.size)
            if spot.state == 'poisoned':
                py.draw.circle(self.screen, PURPLE, spot.pos, spot.size + 6, 6)
            if spot.full:
                py.draw.circle(self.screen, BLACK, spot.pos, spot.size + 3, 3)
                
    def blit_numbers(self):
        py.draw.rect(self.screen,WHITE,(0,0,self.width,self.height/13))
        self.screen.blit(self.font.render(str(int(self.player.money)),True,self.player.color),(20,20))
        self.screen.blit(self.small_font.render(f"{self.player.production_per_second:.0f}", True, (205, 204, 0)), (23, 60))
        for i in range(self.board.player_count):
            self.screen.blit(self.small_font.render(str(int(self.players[i].count)),True,self.players[i].color),(self.width/3 + i*150,20))
        
        if self.board.victor:
            self.screen.blit(self.font.render(f"Player {self.board.victor.id} Wins!",True,self.board.victor.color),(self.width - 300,20))
            if self.player.victory:
                self.screen.blit(self.small_font.render("R to restart",True,self.player.color),(self.width - 300,60))
            else:
                self.screen.blit(self.small_font.render(f"Waiting for Player {self.board.victor.id} to restart",True,self.board.victor.color),(self.width - 450,60))
        elif self.board.timer > 0:
            if self.board.timer < 4:
                self.screen.blit(self.font.render(f"{self.board.timer + 1:.0f}",True,BLACK),(self.width - 100,20))
            else:
                self.screen.blit(self.font.render(f"{self.board.timer + 1:.0f}",True,self.player.color),(self.width - 300,20))
        elif self.player.eliminated:
            self.screen.blit(self.font.render("ELIMINATED",True,self.player.color),(self.width - 300,20))
        else:
            self.screen.blit(self.small_font.render("X to Forfeit",True,self.player.color),(self.width - 300,20))

    def wipe(self):
        self.screen.fill(WHITE)

    def highlight_node(self):
        if self.player.highlighted_node is not None:
            py.draw.circle(self.screen, self.abilities[self.player.mode].color, self.player.highlighted_node.pos, self.player.highlighted_node.size + 5,2)

    def edge_build(self, end):
        start=self.board.id_dict[self.abilities[BRIDGE_CODE].first_node].pos
        triangle_size=5
        spacing=9
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
      
            py.draw.polygon(self.screen, YELLOW, [point1, point2, point3])
            py.draw.lines(self.screen, BLACK, True, [point1, point2, point3]) 

    def blit(self, mouse_pos):
        self.screen.fill(WHITE)
        self.blit_nodes()
        self.blit_edges()
        self.blit_numbers()
        self.highlight_node()
        self.draw_buttons()
        if self.abilities[BRIDGE_CODE].first_node is not None:
            self.edge_build(mouse_pos)
        py.display.update() 

    def relocate(self, width, height):
        self.width = width
        self.height = height

    def close_window(self):
        py.display.quit()
        py.quit()
