import sys

import pygame

from constants import GREY, BLACK, WHITE, LIGHT_GREY


# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

def settings_ui():

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    host_button = pygame.Rect(0, 0, screen_width // 2, 100)
    join_button = pygame.Rect(screen_width // 2, 0, screen_width // 2, 100)

    host_selected = False
    join_selected = False

    current_screen = 'Menu'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if host_button.collidepoint(event.pos):
                    if join_selected:
                        join_selected = False
                    host_selected = True
                elif join_button.collidepoint(event.pos):
                    if host_selected:
                        host_selected = False
                    join_selected = True


                # if current_screen == "Menu" and host_button.collidepoint(event.pos):
                #     current_screen = "Host"
                # elif current_screen == "Menu" and join_button.collidepoint(event.pos):
                #     current_screen = "Join"
                # elif current_screen == "Host" or current_screen == "Join":
                #     if back_button.collidepoint(event.pos):
                #         current_screen = "Menu"

        screen.fill(WHITE)

        if (host_selected):
            pygame.draw.rect(screen, LIGHT_GREY, host_button)
            pygame.draw.rect(screen, GREY, join_button)

            num_players_label_pos = (screen_width // 2 - 100, 200)
            num_players_font_size = 26
            num_players_font = pygame.font.Font(None, num_players_font_size)
            num_players_text = num_players_font.render("Select the number of players:", True, BLACK)
            screen.blit(num_players_text, num_players_text.get_rect(center=num_players_label_pos))

            number_of_players_button = pygame.draw.circle(screen, GREY, ())
        elif (join_selected):
            pygame.draw.rect(screen, GREY, host_button)
            pygame.draw.rect(screen, LIGHT_GREY, join_button)
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

        # if current_screen == "Menu":
        #     game_option_label_pos = (host_button.x - 150, host_button.y + 20)
        #     game_option_font_size = 30  # Larger size for titles
        #     game_option_font = pygame.font.Font(None, game_option_font_size)
        #
        #     pygame.draw.rect(screen, GREY, host_button)
        #     pygame.draw.rect(screen, GREY, join_button)
        #
        #     host_text = host_font.render("Host", True, BLACK)
        #     join_text = join_font.render("Join", True, BLACK)
        #     screen.blit(host_text, host_text.get_rect(center=host_button.center))
        #     screen.blit(join_text, join_text.get_rect(center=join_button.center))
        #
        #     game_option_text = game_option_font.render("Choose one option:", True, BLACK)
        #     screen.blit(game_option_text, game_option_text.get_rect(center=game_option_label_pos))
        # else:
        #     back_button = pygame.Rect(screen_width - 250, screen_height - 100, 150, 40)
        #
        #     back_font_size = 26
        #     back_font = pygame.font.Font(None, back_font_size)
        #     # Draw "Back" button for "Host" or "Join" screens
        #     pygame.draw.rect(screen, GREY, back_button)
        #     back_text = back_font.render("Back", True, BLACK)
        #     screen.blit(back_text, back_text.get_rect(center=back_button.center))
        #
        #     if current_screen == "Host":
        #         player_font_size = 26
        #         player_font = pygame.font.Font(None, player_font_size)
        #
        #         two_player_button = pygame.Rect(500, 100, 40, 40)
        #         three_player_button = pygame.Rect(600, 100, 40, 40)
        #         four_player_button = pygame.Rect(700, 100, 40, 40)
        #
        #         player_size_label_pos = (two_player_button.x - 200, two_player_button.y + 20)
        #         player_size_font_size = 30  # Larger size for titles
        #         player_size_font = pygame.font.Font(None, player_size_font_size)
        #
        #         pygame.draw.rect(screen, GREY, two_player_button)
        #         pygame.draw.rect(screen, GREY, three_player_button)
        #         pygame.draw.rect(screen, GREY, four_player_button)
        #
        #         player_text = player_font.render("1", True, BLACK)
        #         screen.blit(player_text, player_text.get_rect(center=two_player_button.center))
        #
        #         player_text = player_font.render("2", True, BLACK)
        #         screen.blit(player_text, player_text.get_rect(center=three_player_button.center))
        #
        #         player_text = player_font.render("3", True, BLACK)
        #         screen.blit(player_text, player_text.get_rect(center=four_player_button.center))
        #
        #         player_size_text = player_size_font.render("Choose the number of players:", True, BLACK)
        #         screen.blit(player_size_text, player_size_text.get_rect(center=player_size_label_pos))



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
