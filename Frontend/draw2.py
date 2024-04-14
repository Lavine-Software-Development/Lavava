import math
import pygame as py
from clickTypeEnum import ClickType
from constants import (
    EDGE_HIGHLIGHT_SPACING,
    ORANGE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ABILITY_SIZE,
    ABILITY_FONT,
    FONT_GAP,
    BLACK,
    WHITE,
    GREEN,
    DARK_GREEN,
    YELLOW,
    PURPLE,
    PINK,
    GREY,
    BROWN,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    BURN_TICKS,
    SIZE,
    VERTICAL_ABILITY_GAP,
    HORIZONTAL_ABILITY_GAP,
    LENGTH_FACTOR,
    TRIANGLE_SIZE,
    TRIANGLE_SPACING,
    CIRCLE_RADIUS,
    CIRCLE_SPACING,
)
from playerStateEnums import PlayerStateEnum as PSE

class Draw2:
    def __init__(self, highlight, effect_visuals):
        self.font = py.font.Font(None, 60)
        self.small_font = py.font.Font(None, 45)
        self.smaller_font = py.font.Font(None, 35)
        self.temp_line = None
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.highlight = highlight
        self.effect_visuals = effect_visuals

    def set_data(self, main_player ,players, nodes, edges, ability_manager):
        self.screen = py.display.set_mode(SIZE, py.RESIZABLE)
        py.display.set_caption("Lavava")
        self.main_player = main_player
        self.players = players
        self.edges = edges
        self.nodes = nodes
        self.ability_manager = ability_manager
        self.abilities = self.ability_manager.abilities

    def _generate_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)

    def _generate_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)

    def draw_button(
        self, shape, color, name, cost, letter, position, selected, reload_completion):
        btn_size = ABILITY_SIZE * self.height
        border_thickness = 5

        if selected:
            lighter_color = self._generate_lighter_color(color)
            py.draw.rect(
                self.screen,
                lighter_color,
                (
                    position[0] - border_thickness,
                    position[1] - border_thickness,
                    btn_size + 2 * border_thickness,
                    btn_size + 2 * border_thickness,
                ),
            )

        # Draw the button background
        darker_color = self._generate_darker_color(color)
        py.draw.rect(
            self.screen, darker_color, (position[0], position[1], btn_size, btn_size)
        )

        # Drawing shapes inside
        lighter_color = self._generate_lighter_color(color)
        if shape == "circle":
            py.draw.circle(
                self.screen,
                lighter_color,
                (position[0] + btn_size // 2, position[1] + btn_size // 2),
                btn_size // 3,
            )
        elif shape == "square":
            py.draw.rect(
                self.screen,
                lighter_color,
                (
                    position[0] + btn_size // 4,
                    position[1] + btn_size // 4,
                    btn_size // 2,
                    btn_size // 2,
                ),
            )
        elif shape == "triangle":
            points = [
                (position[0] + btn_size // 2, position[1] + btn_size // 4),
                (position[0] + btn_size // 4, position[1] + 3 * btn_size // 4),
                (position[0] + 3 * btn_size // 4, position[1] + 3 * btn_size // 4),
            ]
            py.draw.polygon(self.screen, lighter_color, points)
        elif shape == "star":
            self.draw_star(
                (position[0] + btn_size // 2, position[1] + btn_size // 2),
                btn_size,
                lighter_color,
            )
        elif shape == "x":
            self.draw_x((position[0] + btn_size // 4, position[1] + btn_size // 4), (btn_size, btn_size), lighter_color)
        elif shape == "cross":
            self.draw_cross((position[0] + btn_size // 4, position[1] + btn_size // 4), (btn_size // 2, btn_size // 2), lighter_color)
        py.draw.rect(
                self.screen, BLACK, (position[0], position[1], btn_size, btn_size - (btn_size * reload_completion))
            )

        # Drawing text (name and cost)
        font = py.font.Font(None, int(self.height * ABILITY_FONT))

        if not letter:
            letter = name[0]
        letter_text = font.render(letter, True, BLACK)  # White color
        self.screen.blit(
            letter_text,
            (
                position[0] + (btn_size - letter_text.get_width()) // 2,
                position[1] + (btn_size - letter_text.get_height()) // 2,
            ),
        )

        text = font.render(name, True, WHITE)
        self.screen.blit(
            text,
            (
                position[0] + (btn_size - text.get_width()) // 2,
                position[1] + btn_size - (FONT_GAP * self.height),
            ),
        )

        cost_text = font.render(f"{cost}", True, WHITE)
        self.screen.blit(cost_text, (position[0] + 10, position[1] + 10))

    def draw_buttons(self):
        y_position = int(VERTICAL_ABILITY_GAP * self.height / 6 + 75)
        for key, btn in self.abilities.items():
            btn_box = btn.visual
            self.draw_button(
                btn_box.shape,
                btn_box.color if btn_box.color[0] is not None else self.main_player.color,
                btn_box.name,
                btn.game_display_num,
                btn_box.letter,
                (self.width - int(HORIZONTAL_ABILITY_GAP * self.height), y_position),
                self.ability_manager.mode == key,
                btn.percentage if btn.remaining else 0
            )
            y_position += int(VERTICAL_ABILITY_GAP * self.height)  # Vertical gap between buttons

    def draw_x(self, position, size, color):
        screen = self.screen
        x = position[0]
        y = position[1]

        width = size[0]
        length = size[1]

        x_end_pos = x + 2 * (width // 4)
        y_end_pos = y + 2 * (length // 4)

        py.draw.line(screen, color, (x, y), (x_end_pos, y_end_pos), 20)
        py.draw.line(screen, color, (x, y_end_pos), (x_end_pos, y), 20)

    def draw_cross(self, position, size, color):
        py.draw.line(self.screen, color, (position[0], position[1] + size[1] // 2),
                     (position[0] + size[0], position[1] + size[1] // 2), 20)
        py.draw.line(self.screen, color, (position[0] + size[0] // 2, position[1]),
                     (position[0] + size[0] // 2, position[1] + size[1]), 20)

    def draw_star(self, position, size, color, filled=True):
        inner_radius = size // 6
        outer_radius = size // 3
        star_points = []

        for i in range(5):
            angle = math.radians(i * 72 + 55)  # Start at top point

            # Outer points
            x = position[0] + outer_radius * math.cos(angle)
            y = position[1] + outer_radius * math.sin(angle)
            star_points.append((x, y))

            # Inner points
            angle += math.radians(36)  # Halfway between outer points
            x = position[0] + inner_radius * math.cos(angle)
            y = position[1] + inner_radius * math.sin(angle)
            star_points.append((x, y))

        if filled:
            py.draw.polygon(self.screen, color, star_points)
        else:
            py.draw.lines(self.screen, color, True, star_points)


    def edge_highlight(self, dy, dx, magnitude, length_factor, start, end):
        # Calculate the angle of rotation
        angle = math.degrees(math.atan2(dy, dx))

        # Calculate the dimensions of the capsule
        width = magnitude  # Length of the row of triangles
        height = (
            length_factor * 2 + 15
        )  # Height based on the triangle size with some padding

        # Create a new surface for the capsule
        capsule_surface = py.Surface((int(width), int(height)), py.SRCALPHA)

        # Rotate the surface containing the capsule
        rotated_surface = py.transform.rotate(
            capsule_surface, -angle
        )  # Negative because Pygame's rotation is counter-clockwise

        # Calculate the new position for the rotated surface
        rotated_width, rotated_height = rotated_surface.get_size()
        screen_pos = (
            start[0] + (end[0] - start[0]) / 2 - rotated_width / 2,
            start[1] + (end[1] - start[1]) / 2 - rotated_height / 2,
        )

        # Blit the rotated surface onto the main screen
        self.screen.blit(rotated_surface, screen_pos)

    def draw_arrow(self, edge, color, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = max(math.sqrt(dx * dx + dy * dy), 1)

        dx /= magnitude
        dy /= magnitude

        num_triangles = int((magnitude - 10) / TRIANGLE_SPACING)

        for i in range(1, num_triangles + 1):
            pos = (
                start[0] + i * TRIANGLE_SPACING * dx + 5 * dx,
                start[1] + i * TRIANGLE_SPACING * dy + 5 * dy,
            )

            point1 = pos
            point2 = (
                pos[0] - LENGTH_FACTOR * TRIANGLE_SIZE * dx + TRIANGLE_SIZE * dy,
                pos[1] - LENGTH_FACTOR * TRIANGLE_SIZE * dy - TRIANGLE_SIZE * dx,
            )
            point3 = (
                pos[0] - LENGTH_FACTOR * TRIANGLE_SIZE * dx - TRIANGLE_SIZE * dy,
                pos[1] - LENGTH_FACTOR * TRIANGLE_SIZE * dy + TRIANGLE_SIZE * dx,
            )

            if edge.flowing:
                if 'rage' in edge.from_node.effects:
                    py.draw.polygon(self.screen, DARK_GREEN, [point1, point2, point3])
                else:
                    py.draw.polygon(self.screen, color, [point1, point2, point3])
            else:
                py.draw.lines(self.screen, color, True, [point1, point2, point3])

        # if self.board.highlighted == edge:
            #  self.edge_highlight(dy, dx, magnitude, length_factor, start, end, spacing)

    def draw_circle(self, edge, color, start, end):
        length_factor = 1.5
        triangle_size = TRIANGLE_SIZE + 2

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx * dx + dy * dy)

        dx /= magnitude
        dy /= magnitude

        num_circles = int((magnitude - 10) / CIRCLE_SPACING)

        for i in range(1, num_circles):
            pos = (
                start[0] + i * CIRCLE_SPACING * dx + 5 * dx,
                start[1] + i * CIRCLE_SPACING * dy + 5 * dy,
            )
            if edge.flowing:
                if 'rage' in edge.from_node.effects:
                    py.draw.circle(
                        self.screen, DARK_GREEN, (int(pos[0]), int(pos[1])), CIRCLE_RADIUS
                    )
                else:
                    py.draw.circle(
                        self.screen, color, (int(pos[0]), int(pos[1])), CIRCLE_RADIUS
                    )
            else:
                py.draw.circle(
                    self.screen, color, (int(pos[0]), int(pos[1])), CIRCLE_RADIUS, 1
                )

        # if self.board.highlighted == edge:
        #     self.edge_highlight(dy, dx, magnitude, length_factor, start, end, spacing)

        point1 = pos
        point2 = (
            pos[0] - length_factor * triangle_size * dx + triangle_size * dy,
            pos[1] - length_factor * triangle_size * dy - triangle_size * dx,
        )
        point3 = (
            pos[0] - length_factor * triangle_size * dx - triangle_size * dy,
            pos[1] - length_factor * triangle_size * dy + triangle_size * dx,
        )
        py.draw.polygon(self.screen, (153, 255, 51), [point1, point2, point3])
        py.draw.lines(self.screen, color, True, [point1, point2, point3])

    def blit_edges(self):
        for edge in self.edges:
            if not edge.dynamic:
                self.draw_arrow(edge, edge.color, edge.from_node.pos, edge.to_node.pos)
            else:
                self.draw_circle(edge, edge.color, edge.from_node.pos, edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:

            if spot.owner:
                if spot.is_port:
                    port_width, port_height = (
                        spot.size,
                        spot.size * 1.3,
                    )  # Size of the ports
                    self.blit_ports(spot, BROWN, port_width, port_height)
                elif spot.ports:
                    port_width, port_height = (
                        spot.size * spot.port_percent,
                        spot.size * spot.port_percent * 1.3,
                    )
                    spot.port_percent -= 0.005
                    if spot.port_percent < 0:
                        spot.ports = []
                    self.blit_ports(spot, ORANGE, port_width, port_height)

            if spot.state_name == "mine":
                state = spot.state
                if spot.owner is not None:
                    angle1 = 2 * math.pi * ((state.bubble - spot.value) / state.bubble)
                    py.draw.arc(
                        self.screen,
                        state.color,
                        (
                            spot.pos[0] - spot.size,
                            spot.pos[1] - spot.size,
                            spot.size * 2,
                            spot.size * 2,
                        ),
                        -angle1 / 2,
                        angle1 / 2,
                        spot.size,
                    )
                    py.draw.arc(
                        self.screen,
                        spot.owner.color,
                        (
                            spot.pos[0] - spot.size,
                            spot.pos[1] - spot.size,
                            spot.size * 2,
                            spot.size * 2,
                        ),
                        angle1 / 2,
                        -angle1 / 2 + 2 * math.pi,
                        spot.size,
                    )
                else:
                    py.draw.circle(self.screen, GREY, spot.pos, spot.size)
                py.draw.circle(
                    self.screen, spot.state.ring_color, spot.pos, spot.size + 6, 6
                )
            elif spot.state_name == "zombie":
                py.draw.rect(self.screen, spot.color,
                             (spot.pos[0] - spot.size // 2, spot.pos[1] - spot.size // 2,
                              spot.size, spot.size))
            else:
                py.draw.circle(self.screen, spot.color, spot.pos, spot.size)
            if 'poison' in spot.effects:
                py.draw.circle(self.screen, PURPLE, spot.pos, spot.size + 6, 6)
            if 'rage' in spot.effects:
                py.draw.circle(self.screen, DARK_GREEN, spot.pos, spot.size - 2, 3)
            if spot.full:
                py.draw.circle(self.screen, BLACK, spot.pos, spot.size + 3, 3)
                if spot.state_name == "capital":
                    py.draw.circle(self.screen, PINK, spot.pos, spot.size + 6, 4)
            # if self.board.highlighted == spot:
            #     py.draw.circle(
            #         self.screen,
            #         self.board.highlighted_color,
            #         spot.pos,
            #         spot.size + 5,
            #         3,
            #     )

    def blit_ports(self, spot, port_color, port_width, port_height):
        for angle in spot.ports:
            # Calculate the center of the port base on the node circumference
            port_center_x = spot.pos[0] + spot.size * math.cos(angle)
            port_center_y = spot.pos[1] + spot.size * math.sin(angle)
            
            # Create a new surface for the port (with per-pixel alpha)
            port_surface = py.Surface((port_width, port_height), py.SRCALPHA)
            port_surface.fill(port_color)
            
            # Rotate the port surface around its center
            rotated_port = py.transform.rotate(port_surface, -math.degrees(angle))
            rotated_rect = rotated_port.get_rect(center=(port_center_x, port_center_y))
            
            # Blit the rotated port surface onto the main screen
            self.screen.blit(rotated_port, rotated_rect.topleft)

    def blit_numbers(self, time):
        # py.draw.rect(self.screen, WHITE, (0, 0, self.width, self.height / 13))
        # Gross
        # if mode.MODE != 2:
        #     self.screen.blit(
        #         self.font.render(
        #             str(int(CONTEXT["main_player"].money)),
        #             True,
        #             (205, 204, 0),
        #         ),
        #         (self.width - 150, 20),
        #     )
        #     self.screen.blit(
        #         self.smaller_font.render(
        #             f"{CONTEXT['main_player'].production_per_second:.0f}/s",
        #             True,
        #             (205, 204, 0),
        #         ),
        #         (self.width - 50, 25),
        #     )
        # self.screen.blit(
        #     self.small_font.render(
        #         f"{self.board.percent_energy}%", True, CONTEXT['main_player'].color
        #     ),
        #     (self.width - 150, 65),
        # )
        # self.screen.blit(
        #     self.small_font.render(
        #         str(int(CONTEXT['main_player'].full_capital_count)), True, PINK
        #     ),
        #     (self.width - (self.width / 43), 20),
        # )

        # if self.player_manager.victor:
        #     self.screen.blit(
        #         self.font.render(
        #             f"Player {self.player_manager.victor.id} Wins!",
        #             True,
        #             self.player_manager.victor.color,
        #         ),
        #         (self.width - 450, 20),
        #     )
        if time > 0:
            if time < 4:
                self.screen.blit(
                    self.font.render(
                        f"{time + 1:.0f}", True, BLACK
                    ),
                    (20, 20),
                )
            else:
                self.screen.blit(
                    self.font.render(
                        f"{time + 1:.0f}",
                        True,
                        self.main_player.color,
                    ),
                    (20, 20),
                )
        # elif CONTEXT["main_player"].eliminated:
        #     self.screen.blit(
        #         self.font.render("ELIMINATED", True, CONTEXT["main_player"].color),
        #         (self.width - 450, 20),
        #     )
        # else:
        #     self.screen.blit(
        #         self.small_font.render(
        #             "X to Forfeit", True, CONTEXT["main_player"].color
        #         ),
        #         (self.width - 450, 20),
        #     )

    def blit_waiting(self):
        self.screen.blit(
            self.small_font.render(
                "Waiting for other Players to Choose Abilities", True, GREEN
            ),
            (self.width // 7, 20),
        )

    def wipe(self):
        self.screen.fill(WHITE)

    def edge_build(self, end, type):
        start = self.ability_manager.clicks[0].pos
        triangle_size = 5
        spacing = 9
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx * dx + dy * dy)

        dx /= magnitude
        dy /= magnitude

        num_shapes = int((magnitude - 10) / spacing)

        length_factor = 1.5

        for i in range(1, num_shapes + 1):
            pos = (
                start[0] + i * spacing * dx + 5 * dx,
                start[1] + i * spacing * dy + 5 * dy,
            )

            if type == BRIDGE_CODE:
                point1 = pos
                point2 = (
                    pos[0] - length_factor * triangle_size * dx + triangle_size * dy,
                    pos[1] - length_factor * triangle_size * dy - triangle_size * dx,
                )
                point3 = (
                    pos[0] - length_factor * triangle_size * dx - triangle_size * dy,
                    pos[1] - length_factor * triangle_size * dy + triangle_size * dx,
                )
                py.draw.polygon(self.screen, YELLOW, [point1, point2, point3])
                py.draw.lines(self.screen, BLACK, True, [point1, point2, point3])
            else:
                py.draw.circle(self.screen, YELLOW, pos, 3)
                py.draw.circle(self.screen, BLACK, (int(pos[0]), int(pos[1])), 3, 1)

    def blit_capital_stars(self):
        for spot in self.nodes:
            if spot.state_name == "capital" and spot.state.capitalized:
                self.draw_star(spot.pos, spot.size * 2, PINK)
                self.draw_star(spot.pos, spot.size * 2, BLACK, False)

    def draw_burning(self, burning):
        for spot, count in burning.items():
            percentage = count / BURN_TICKS
            port_width, port_height = (
                    spot.size / 1.5 * percentage,
                    spot.size * 1.5 * percentage,
                ) 
            self.blit_ports(spot, ORANGE, port_width, port_height)

    def highlighting(self):
        if self.highlight.type == ClickType.NODE:
            color = self.highlight.color or self.main_player.color
            py.draw.circle(
                self.screen,
                color,
                self.highlight.item.pos,
                self.highlight.item.size + 5,
                3,
            )
        else:
            color = self.highlight.color or GREY
            start, end = self.highlight.item.from_node.pos, self.highlight.item.to_node.pos
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            magnitude = math.sqrt(dx * dx + dy * dy)

            dx /= magnitude
            dy /= magnitude

            angle = math.degrees(math.atan2(dy, dx))

            width = magnitude  # Length of the row of triangles
            height = LENGTH_FACTOR * 2 + 15  # Height based on the triangle size with some padding
            capsule_surface = py.Surface((int(width), int(height)), py.SRCALPHA)

            line_start_x = int(height / 2) + EDGE_HIGHLIGHT_SPACING
            line_end_x = int(width - height / 2) - EDGE_HIGHLIGHT_SPACING

            # Draw the lines
            py.draw.line(
                capsule_surface,
                color,
                (line_start_x, 2),
                (line_end_x, 2),
                2,
            )
            py.draw.line(
                capsule_surface,
                color,
                (line_start_x, height - 2),
                (line_end_x, height - 2),
                2,
            )

            # Rotate the surface containing the capsule
            # Negative because Pygame's rotation is counter-clockwise
            rotated_surface = py.transform.rotate(capsule_surface, -angle)

            # Calculate the new position for the rotated surface
            rotated_width, rotated_height = rotated_surface.get_size()
            screen_pos = (
                start[0] + (end[0] - start[0]) / 2 - rotated_width / 2,
                start[1] + (end[1] - start[1]) / 2 - rotated_height / 2,
            )

            # Blit the rotated surface onto the main screen
            self.screen.blit(rotated_surface, screen_pos)


    def blit(self, ps, time):
        self.screen.fill(WHITE) 
        self.blit_nodes()
        self.blit_edges()
        if self.highlight:
            self.highlighting()
        # if burning := self.effect_visuals[PriorityEnum.BURNED_NODE.value]:
        #     self.draw_burning(burning)
        self.blit_capital_stars()
        if ps == PSE.START_WAITING:
            self.blit_waiting()
        else:
            self.blit_numbers(time)
        self.draw_buttons()
        if (self.ability_manager.mode in [BRIDGE_CODE, D_BRIDGE_CODE]) and self.ability_manager.clicks:
            self.edge_build(py.mouse.get_pos(), self.ability_manager.mode)
        py.display.update()

    def relocate(self, width, height):
        self.width = width
        self.height = height

    def close_window(self):
        py.display.quit()
        py.quit()
