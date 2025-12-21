import pygame

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

player_x = 100
player_y = 300
player_size = 50
player_color = BLUE

player_v_y = 0 #y축 속도
gravity = 1.0
jump_pwr = -17
is_jumping = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_jumping:
                player_v_y = jump_pwr
                is_jumping = True
    screen.fill(WHITE)
    
    #물리법칙
    player_v_y += gravity
    
    player_y += player_v_y
    
    if player_y > 300:
        player_y = 300
        player_v_y = 0
        is_jumping = False
    pygame.draw.rect(screen, player_color,(player_x, player_y, player_size, player_size))
    pygame.draw.line(screen, BLACK, (0, 350), (screen_width, 350), 5)
        
    pygame.display.update()
    clock.tick(60)
pygame.quit()