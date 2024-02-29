import sys

import pygame

from constants import GREY, BLACK, WHITE, LIGHT_GREY

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


def is_point_in_circle(point, circle_center, circle_radius):
    # Calculate the distance between the point and the circle's center
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    distance_squared = dx ** 2 + dy ** 2

    # Check if the distance is less than or equal to the radius squared
    return distance_squared <= circle_radius ** 2


def settings_ui():
    host_settings_info = ["HOST", 0, 0]
    join_settings_info = ["JOIN"]

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    host_button = pygame.Rect(0, 0, screen_width // 2, 100)
    join_button = pygame.Rect(screen_width // 2, 0, screen_width // 2, 100)

    default_button = pygame.Rect(100, screen_height // 2 + 100, 150, 100)
    reload_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 100, 150, 100)
    ports_button = pygame.Rect(screen_width - 250, screen_height // 2 + 100, 150, 100)
    done_button = pygame.Rect(screen_width - 100, screen_height - 100, 100, 50)

    two_players_button_center = (screen_width // 2, 200)
    three_players_button_center = (screen_width // 2 + 150, 200)
    four_players_button_center = (screen_width // 2 + 300, 200)

    host_selected = False
    join_selected = False

    done_selected = False

    ip_input_box_color = LIGHT_GREY
    ip_input_box = pygame.Rect(100, screen_height // 2, screen_width - 200, 40)
    typing_to_input_box = False
    ip_address = ''

    gameplay_selected = None
    num_players_selected = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if host_button.collidepoint(event.pos):
                    if join_selected:
                        join_selected = False
                        gameplay_selected = None
                    host_selected = True
                    ip_address = ''
                elif join_button.collidepoint(event.pos):
                    if host_selected:
                        host_selected = False
                    join_selected = True
                    gameplay_selected = None
                    host_settings_info = ["HOST", 0, 0]
                elif host_selected:
                    if default_button.collidepoint(event.pos):
                        gameplay_selected = "Default"
                        host_settings_info[2] = 1
                    elif reload_button.collidepoint(event.pos):
                        gameplay_selected = "Reload"
                        host_settings_info[2] = 2
                    elif ports_button.collidepoint(event.pos):
                        gameplay_selected = "Ports"
                        host_settings_info[2] = 3

                    if is_point_in_circle(event.pos, two_players_button_center, 10):
                        num_players_selected = 2
                        host_settings_info[1] = 2
                    elif is_point_in_circle(event.pos, three_players_button_center, 10):
                        num_players_selected = 3
                        host_settings_info[1] = 3
                    elif is_point_in_circle(event.pos, four_players_button_center, 10):
                        num_players_selected = 4
                        host_settings_info[1] = 4

                    if done_button.collidepoint(event.pos) and host_settings_info[1] != 0 and host_settings_info[2] != 0:
                        done_selected = True
                elif join_selected:
                    if ip_input_box.collidepoint(event.pos):
                        typing_to_input_box = True
                    else:
                        typing_to_input_box = False

                    if done_button.collidepoint(event.pos) and ip_address != '':
                        done_selected = True

            if event.type == pygame.KEYDOWN:
                if join_selected and typing_to_input_box is True:
                    if event.key == pygame.K_BACKSPACE:
                        ip_address = ip_address[:-1]
                    else:
                        ip_address += event.unicode

        screen.fill(WHITE)

        if host_selected:
            pygame.draw.rect(screen, LIGHT_GREY, host_button)
            pygame.draw.rect(screen, GREY, join_button)

            num_players_label_pos = (200, 200)
            num_players_font_size = 26
            num_players_font = pygame.font.Font(None, num_players_font_size)
            num_players_text = num_players_font.render("Select the number of players:", True, BLACK)
            screen.blit(num_players_text, num_players_text.get_rect(center=num_players_label_pos))

            two_player_button = pygame.draw.circle(screen, GREY, (screen_width // 2, 200), 10)
            three_player_button = pygame.draw.circle(screen, GREY, (screen_width // 2 + 150, 200), 10)
            four_player_button = pygame.draw.circle(screen, GREY, (screen_width // 2 + 300, 200), 10)

            if num_players_selected == 2 and host_settings_info[1] == 2:
                pygame.draw.circle(screen, BLACK, (screen_width // 2, 200), 5)
            elif num_players_selected == 3 and host_settings_info[1] == 3:
                pygame.draw.circle(screen, BLACK, (screen_width // 2 + 150, 200), 5)
            elif num_players_selected == 4 and host_settings_info[1] == 4:
                pygame.draw.circle(screen, BLACK, (screen_width // 2 + 300, 200), 5)

            player_size_font_size = 30  # Larger size for titles
            player_size_font = pygame.font.Font(None, player_size_font_size)

            player_text = player_size_font.render("2", True, BLACK)
            two_player_center = two_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(two_player_center[0], two_player_center[1] - 20)))

            player_text = player_size_font.render("3", True, BLACK)
            three_player_center = three_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(three_player_center[0], three_player_center[1] - 20)))

            player_text = player_size_font.render("4", True, BLACK)
            four_player_center = four_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(four_player_center[0], four_player_center[1] - 20)))

            gameplay_label_pos = (screen_width // 2, screen_height // 2)
            gameplay_label_font_size = 26
            gameplay_label_font = pygame.font.Font(None, gameplay_label_font_size)
            gameplay_label_text = gameplay_label_font.render("Select the type of gameplay:", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=gameplay_label_pos))

            if gameplay_selected == "Default":
                pygame.draw.rect(screen, LIGHT_GREY, default_button)
            else:
                pygame.draw.rect(screen, GREY, default_button)
            gameplay_label_text = gameplay_label_font.render("Default", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=default_button.center))

            if gameplay_selected == "Reload":
                pygame.draw.rect(screen, LIGHT_GREY, reload_button)
            else:
                pygame.draw.rect(screen, GREY, reload_button)
            gameplay_label_text = gameplay_label_font.render("Reload", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=reload_button.center))

            if gameplay_selected == "Ports":
                pygame.draw.rect(screen, LIGHT_GREY, ports_button)
            else:
                pygame.draw.rect(screen, GREY, ports_button)
            gameplay_label_text = gameplay_label_font.render("Ports", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=ports_button.center))

        elif join_selected:
            pygame.draw.rect(screen, GREY, host_button)
            pygame.draw.rect(screen, LIGHT_GREY, join_button)

            ip_font = pygame.font.Font(None, 32)
            ip_text = ip_font.render(ip_address, True, BLACK)
            if typing_to_input_box:
                screen.blit(ip_text, (ip_input_box.x + 5, ip_input_box.y + 5))
            pygame.draw.rect(screen, ip_input_box_color, ip_input_box, 2)

        else:
            pygame.draw.rect(screen, GREY, host_button)
            pygame.draw.rect(screen, GREY, join_button)

        host_font_size = 26
        host_font = pygame.font.Font(None, host_font_size)

        join_font_size = 26
        join_font = pygame.font.Font(None, join_font_size)

        host_text = host_font.render("Host", True, BLACK)
        join_text = join_font.render("Join", True, BLACK)
        screen.blit(host_text, host_text.get_rect(center=host_button.center))
        screen.blit(join_text, join_text.get_rect(center=join_button.center))

        done_font_size = 26
        done_font = pygame.font.Font(None, done_font_size)
        done_text = done_font.render("Done", True, BLACK)

        pygame.draw.rect(screen, GREY, done_button)
        screen.blit(done_text, done_text.get_rect(center=done_button.center))
        pygame.display.flip()
        clock.tick(60)

        if done_selected:
            if host_selected:
                return host_settings_info, None
            elif join_selected:
                return join_settings_info, ip_address
