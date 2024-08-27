import pygame
pygame.init()

game_active = False
screen_color = "#E1D7B7"
clock = pygame.time.Clock() 
bg_x = 0

#obstacles
obstacles_event = pygame.USEREVENT + 1
obstacles_spawn = pygame.time.set_timer(obstacles_event, 2000)
cactus_group = []

score = 0
start_time = 0