import socket
import pygame
import pyperclip

from constants import GREY, BLACK, WHITE, LIGHT_GREY

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
# colours
DARK_BLUE = pygame.Color(33, 73, 138)
LIGHT_BLUE = pygame.Color(82, 130, 209)
# host options
DEFAULT = 1
RELOAD = 2
PORTS = 3


def is_point_in_circle(point, circle_center, circle_radius):
    # Calculate the distance between the point and the circle's center
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    distance_squared = dx ** 2 + dy ** 2

    # Check if the distance is less than or equal to the radius squared
    return distance_squared <= circle_radius ** 2


def get_local_ip():
    try:
        # Create a socket connection to determine the local IP address
        # The address '8.8.8.8' and port 80 are used here as an example and do not need to be reachable
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None


def settings_ui():
    IP = str(get_local_ip())
    host_settings_info = ["HOST", 0, 0]
    join_settings_info = ["JOIN"]

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    screen_width = screen.get_width()
    print(str(screen_width))
    screen_height = screen.get_height()

    host_button = pygame.Rect(0, 0, screen_width // 2, 100)
    join_button = pygame.Rect(screen_width // 2, 0, screen_width // 2, 100)   
    
    host_ip_font = pygame.font.Font(None, 50)
    host_ip_text = host_ip_font.render("Host IP:    " + IP, True, DARK_BLUE)
    host_ip_rect = host_ip_text.get_rect(center=(screen_width // 2 - 75, 200)) 
    copy_button = pygame.Rect(host_ip_rect.topright[0] + 50, host_ip_rect.top, 100, host_ip_rect.height)

    default_button = pygame.Rect(100, screen_height // 2 + 100, 150, 100)
    reload_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 100, 150, 100)
    ports_button = pygame.Rect(screen_width - 250, screen_height // 2 + 100, 150, 100)
    done_button = pygame.Rect(screen_width - 150, screen_height - 100, 100, 50)

    NUM_PLAYERS_Y = 300
    two_players_button_center = (screen_width // 2, NUM_PLAYERS_Y)
    three_players_button_center = (screen_width // 2 + 150, NUM_PLAYERS_Y)
    four_players_button_center = (screen_width // 2 + 300, NUM_PLAYERS_Y)

    host_selected = False
    join_selected = False

    done_selected = False
    copy_selected = False

    ip_input_box_color = LIGHT_GREY
    ip_input_box = pygame.Rect(100, screen_height // 2, screen_width - 200, 40)
    typing_to_input_box = False
    ip_address = ''

    gameplay_selected = None
    

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
                elif done_button.collidepoint(event.pos):
                    done_selected = True
                elif host_selected:
                    if copy_button.collidepoint(event.pos):
                        pyperclip.copy(IP)
                        copy_selected = True
                        
                    if default_button.collidepoint(event.pos):
                        host_settings_info[2] = DEFAULT
                    elif reload_button.collidepoint(event.pos):
                        host_settings_info[2] = RELOAD
                    elif ports_button.collidepoint(event.pos):
                        host_settings_info[2] = PORTS
                        
                    if is_point_in_circle(event.pos, two_players_button_center, 10):
                        host_settings_info[1] = 2
                    elif is_point_in_circle(event.pos, three_players_button_center, 10):
                        host_settings_info[1] = 3
                    elif is_point_in_circle(event.pos, four_players_button_center, 10):
                        host_settings_info[1] = 4       

            if event.type == pygame.KEYDOWN:
                if join_selected:
                    if event.key == pygame.K_BACKSPACE:
                        ip_address = ip_address[:-1]
                    else:
                        ip_address += event.unicode
                if join_selected and event.key == pygame.K_v:  # Paste event
                    if pygame.key.get_mods() and pygame.KMOD_CTRL or pygame.key.get_mods() and pygame.KMOD_META:
                        ip_address = pyperclip.paste()

        # Draw elements on screen
        
        screen.fill(WHITE)
        
        # Opening page
        pygame.draw.rect(screen, LIGHT_GREY, host_button)
        pygame.draw.rect(screen, GREY, join_button)
        choose_one_font = pygame.font.Font(None, 48)
        choose_one_text = choose_one_font.render("Please choose an option above", True, BLACK)
        choose_one_rect = choose_one_text.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(choose_one_text, choose_one_rect)


        if host_selected:
            HOST_MED_FONT = pygame.font.Font(None, 30)
            
            pygame.draw.rect(screen, WHITE, choose_one_rect)
            
            # Display host name 
            screen.blit(host_ip_text, host_ip_rect)
            if copy_selected:
                copy_ip_text = HOST_MED_FONT.render("Copied", True, BLACK)
                pygame.draw.rect(screen, LIGHT_BLUE, copy_button)
                screen.blit(copy_ip_text, copy_ip_text.get_rect(center=copy_button.center))
            else:
                copy_ip_text = HOST_MED_FONT.render("Copy IP", True, BLACK)
                pygame.draw.rect(screen, DARK_BLUE, copy_button)
                screen.blit(copy_ip_text, copy_ip_text.get_rect(center=copy_button.center))
            
            NUM_PLAYERS_Y = 300
            num_players_label_pos = (200, NUM_PLAYERS_Y)
            num_players_text = HOST_MED_FONT.render("Select the number of players:", True, BLACK)
            screen.blit(num_players_text, num_players_text.get_rect(center=num_players_label_pos))

            two_player_button = pygame.draw.circle(screen, GREY, two_players_button_center, 10)
            three_player_button = pygame.draw.circle(screen, GREY, three_players_button_center, 10)
            four_player_button = pygame.draw.circle(screen, GREY, four_players_button_center, 10)

            if host_settings_info[1] == 2:
                pygame.draw.circle(screen, BLACK, two_players_button_center, 5)
            elif host_settings_info[1] == 3:
                pygame.draw.circle(screen, BLACK, three_players_button_center, 5)
            elif host_settings_info[1] == 4:
                pygame.draw.circle(screen, BLACK, four_players_button_center, 5)


            player_text = HOST_MED_FONT.render("2", True, BLACK)
            two_player_center = two_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(two_player_center[0], two_player_center[1] - 20)))

            player_text = HOST_MED_FONT.render("3", True, BLACK)
            three_player_center = three_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(three_player_center[0], three_player_center[1] - 20)))

            player_text = HOST_MED_FONT.render("4", True, BLACK)
            four_player_center = four_player_button.center
            screen.blit(player_text, player_text.get_rect(center=(four_player_center[0], four_player_center[1] - 20)))

            gameplay_label_pos = (screen_width // 2, screen_height // 2)
            gameplay_label_text = HOST_MED_FONT.render("Select the type of gameplay:", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=gameplay_label_pos))

            if host_settings_info[2] == DEFAULT:
                pygame.draw.rect(screen, LIGHT_GREY, default_button)
            else:
                pygame.draw.rect(screen, GREY, default_button)
            gameplay_label_text = HOST_MED_FONT.render("Default", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=default_button.center))

            if host_settings_info[2] == RELOAD:
                pygame.draw.rect(screen, LIGHT_GREY, reload_button)
            else:
                pygame.draw.rect(screen, GREY, reload_button)
            gameplay_label_text = HOST_MED_FONT.render("Reload", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=reload_button.center))

            if host_settings_info[2] == PORTS:
                pygame.draw.rect(screen, LIGHT_GREY, ports_button)
            else:
                pygame.draw.rect(screen, GREY, ports_button)
            gameplay_label_text = HOST_MED_FONT.render("Ports", True, BLACK)
            screen.blit(gameplay_label_text, gameplay_label_text.get_rect(center=ports_button.center))

        elif join_selected:
            pygame.draw.rect(screen, WHITE, choose_one_rect)
            ip_prompt_font = pygame.font.Font(None, 40)
            ip_prompt_text = ip_prompt_font.render("Type or paste host IP to join game", True, BLACK)
            screen.blit(ip_prompt_text, ip_prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100)))
            
            ip_font = pygame.font.Font(None, 32)
            ip_text = ip_font.render(ip_address, True, BLACK)
            screen.blit(ip_text, (ip_input_box.x + 5, ip_input_box.y + 5))
            pygame.draw.rect(screen, ip_input_box_color, ip_input_box, 2)

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
            
        # if (host_selected and host_settings_info[1] != 0 and host_settings_info[2] != 0) \
        #     or (join_selected and len(ip_address) > 0): 
        if (host_selected and host_settings_info[2] != 0) \
            or (join_selected and len(ip_address) > 0): 
            
            pygame.draw.rect(screen, GREY, done_button)
            screen.blit(done_text, done_text.get_rect(center=done_button.center))
        
        mouse_pos = pygame.mouse.get_pos()
        if done_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_GREY, done_button)
            screen.blit(done_text, done_text.get_rect(center=done_button.center))
        
        pygame.display.flip()
        clock.tick(60)

        if done_selected:
            screen.fill(WHITE)
            waiting_font = pygame.font.Font(None, 50)
            waiting_text = waiting_font.render("Waiting for players to join...", True, pygame.Color(127, 93, 153))
            screen.blit(waiting_text, waiting_text.get_rect(center=(screen_width // 2, screen_height // 3)))
            
            pygame.display.flip()
            clock.tick(60)

            if host_selected:
                if host_settings_info[1] == 0:
                    host_settings_info[1] = 1
                return host_settings_info, IP
            elif join_selected:
                return join_settings_info, ip_address
            
        