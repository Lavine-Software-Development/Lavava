import pygame
from constants import BLACK, GREEN, LIGHT_GREEN, WHITE, MEDIUM_GREEN, DARK_GRAY
import math
# import mode as mode

# Constants
WINDOW_WIDTH = 1067  # Adjust as needed
WINDOW_HEIGHT = 800  # Adjust as needed
BOX_SIZE = 200  # Size of each ability box
COLUMNS = 4
ROWS = 3
PADDING = 50  # Padding between boxes
BOX_PADDING = 18  # Padding around each box


class ChooseUI:

    def __init__(self, boxes):
        self.boxes = boxes
        self.box_rects = []
        self.selected_boxes = set()
        # self.gs = gs
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.number_font_size = 42  # Example size, adjust as needed for your UI
        self.number_font = pygame.font.Font(None, self.number_font_size)

        self.name_font_size = 36  # Example size, adjust as needed for your UI
        self.name_font = pygame.font.Font(None, self.name_font_size)

        self.count_font_size = 48  # Slightly bigger for box.count
        self.count_font = pygame.font.Font(None, self.count_font_size)

        self.reset_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 60, 100, 50)
    
    def choose_abilities(self):
    
        # Create boxes
        # from modeConstants import DEFAULT_SPAWN, ABILITY_COUNT
        
        # if DEFAULT_SPAWN[mode.MODE]:
        #     self.boxes.pop(SPAWN_CODE)

        # Calculate positions for boxes and store them as Pygame Rects for easy collision detection
        horizontal_spacing = (WINDOW_WIDTH - (BOX_SIZE * COLUMNS)) / (COLUMNS + 1)
        vertical_spacing = (WINDOW_HEIGHT - (BOX_SIZE * ROWS)) / (ROWS + 3)
        for index, (code, box) in enumerate(self.boxes.items()):
            column = index % COLUMNS
            row = index // COLUMNS
            x = horizontal_spacing + (BOX_SIZE + horizontal_spacing) * column
            y = vertical_spacing + (BOX_SIZE + vertical_spacing) * row

            rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
            self.box_rects.append((code, rect))

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for code, rect in self.box_rects:
                        if rect.collidepoint(event.pos):
                            self.click_box(code, event.button)
                            break
                        if self.reset_button_rect.collidepoint(event.pos):
                            self.reset_boxes()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill(WHITE)
            self.draw_boxes(mouse_pos)
            self.draw_message()
            pygame.display.flip()
            self.clock.tick(60)

        # if DEFAULT_SPAWN[mode.MODE]:
        #     return [SPAWN_CODE] + list(self.selected_boxes)
        # return list(self.selected_boxes)

    def click_box(self, code, click):

        # from modeConstants import ABILITY_COUNT

        if code in self.selected_boxes:
            self.selected_boxes.remove(code)
        # elif len(self.selected_boxes) < ABILITY_COUNT[mode.MODE]:
        elif len(self.selected_boxes) < 4:
            self.selected_boxes.add(code)

    def _generate_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)


    def _generate_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)


    def draw_boxes(self, mouse_pos):
        for code, rect in self.box_rects:
            box = self.boxes[code]
            # Check if the current box is under the mouse cursor
            is_hovered = rect.collidepoint(mouse_pos)
            is_selected = code in self.selected_boxes

            # Draw the outer box with padding if hovered or selected
            if is_selected or is_hovered:
                outer_color = GREEN if is_selected else LIGHT_GREEN
                pygame.draw.rect(
                    self.screen, outer_color, rect.inflate(BOX_PADDING, BOX_PADDING)
                )

            # Draw the inner box
            pygame.draw.rect(self.screen, self._generate_darker_color(box.visual.color), rect)

            # Drawing the shape inside the box
            self.draw_shape(
                box.visual.shape, rect.x, rect.y, self._generate_lighter_color(box.visual.color)
            )

            # Set up the fonts

            # Render the ability name and blit it at the bottom center of the box
            text = self.name_font.render(box.visual.name, True, WHITE)
            text_rect = text.get_rect(
                center=(rect.x + rect.width / 2, rect.y + rect.height - self.name_font_size + 15)
            )
            self.screen.blit(text, text_rect)

            self.draw_numbers(rect, box)

        pygame.draw.rect(self.screen, DARK_GRAY, self.reset_button_rect)  # Draw the button
        reset_text = self.name_font.render('Reset', True, WHITE)
        reset_text_rect = reset_text.get_rect(center=self.reset_button_rect.center)
        if self.reset_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.screen, BLACK, self.reset_button_rect.inflate(BOX_PADDING, BOX_PADDING)
            )
        self.screen.blit(reset_text, reset_text_rect)
    
    def draw_numbers(self, rect, box):
        cost_text = self.number_font.render(str(box.visual.cost), True, WHITE)

        cost_text_rect = cost_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        self.screen.blit(cost_text, cost_text_rect)

    def draw_star(self, position, size, color):
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

        pygame.draw.polygon(self.screen, color, star_points)

    def draw_x(self, position, size, color):
        x = position[0]
        y = position[1]

        width = size[0]
        length = size[1]

        x_end_pos = x + 2 * (width // 4)
        y_end_pos = y + 2 * (length // 4)

        pygame.draw.line(self.screen, color, (x, y), (x_end_pos, y_end_pos), 20)
        pygame.draw.line(self.screen, color, (x, y_end_pos), (x_end_pos, y), 20)


    def draw_cross(self, position, size, color):
        pygame.draw.line(self.screen, color, (position[0], position[1] + size[1] // 2),
                        (position[0] + size[0], position[1] + size[1] // 2), 20)
        pygame.draw.line(self.screen, color, (position[0] + size[0] // 2, position[1]),
                        (position[0] + size[0] // 2, position[1] + size[1]), 20)

    def draw_shape(self, shape, x, y, light_color):
        # This function will handle drawing the shape within a given box
        center = (x + BOX_SIZE // 2, y + BOX_SIZE // 2)
        if shape == "circle":
            pygame.draw.circle(self.screen, light_color, center, BOX_SIZE // 3.5)
        elif shape == "square":
            rect = (x + BOX_SIZE // 4, y + BOX_SIZE // 4, BOX_SIZE // 2, BOX_SIZE // 2)
            pygame.draw.rect(self.screen, light_color, rect)
        elif shape == "triangle":
            points = [
                (center[0], y + BOX_SIZE // 4),
                (x + BOX_SIZE // 4, y + 3 * BOX_SIZE // 4),
                (x + 3 * BOX_SIZE // 4, y + 3 * BOX_SIZE // 4),
            ]
            pygame.draw.polygon(self.screen, light_color, points)
        elif shape == "star":
            star_size = BOX_SIZE * 0.8  # Adjust the size as needed
            self.draw_star(center, star_size, light_color)
        elif shape == "x":
            self.draw_x((x + (BOX_SIZE // 4), y + (BOX_SIZE // 4)), (BOX_SIZE, BOX_SIZE), light_color)
        elif shape == "cross":
            self.draw_cross((x + BOX_SIZE // 4, y + BOX_SIZE // 4), (BOX_SIZE // 2, BOX_SIZE // 2), light_color)


    def draw_message(self):
        font_size = 90  # Example size, adjust as needed for your UI
        font = pygame.font.Font(None, font_size)
        message = ""
        color = MEDIUM_GREEN

        if self.complete_check() :
            message = "Press Enter"
            color = GREEN
        else:
            message = self.message

        # Render the message and center it at the bottom of the screen
        text = font.render(message, True, color)
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )  # 50 pixels from the bottom

        # Blit the message onto the screen
        self.screen.blit(text, text_rect)

    def reset_boxes(self):
        self.selected_boxes.clear() 

    @property
    def message(self):
        return f"Pick {4 - len(self.selected_boxes)}"
    
    def complete_check(self):
        return len(self.selected_boxes) == 4


class ChooseReloadUI(ChooseUI):

    def __init__(self, boxes, credits):
        self.start_credits = credits
        self.credits = credits
        super().__init__(boxes)
        for key, box in boxes.items():
            if box.remaining > 0:
                self.credits -= box.credits * box.remaining
                self.selected_boxes.add(key)

    def draw_numbers(self, rect, box):
        count_text = self.count_font.render(str(box.remaining), True, BLACK)
        count_text_rect = count_text.get_rect(center=(rect.centerx, rect.centery))
        self.screen.blit(count_text, count_text_rect)
        credit_text = self.number_font.render(str(box.credits), True, WHITE)

        cost_text_rect = credit_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        self.screen.blit(credit_text, cost_text_rect)

    def click_box(self, code, click):

        if click == 1 and self.credits >= self.boxes[code].credits:
            if code not in self.selected_boxes:
                if len(self.selected_boxes) < 4:
                    self.selected_boxes.add(code)
                else:
                    return
            self.boxes[code].remaining += 1
            self.credits -= self.boxes[code].credits
        elif click == 3 and code in self.selected_boxes:
            self.boxes[code].remaining -= 1
            self.credits += self.boxes[code].credits
            if self.boxes[code].remaining == 0:
                self.selected_boxes.remove(code)

    def reset_boxes(self):
        # Reset all counts to 0 and remove all from selected_boxes
        for key, box in self.boxes.items():
            box.remaining = 0  # Reset count
        self.credits = self.start_credits
        super().reset_boxes()

    @property
    def message(self):
        return f"{self.credits} Credits"
    
    def complete_check(self):
        return self.credits == 0