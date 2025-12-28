import pygame

pygame.init()

#게임 변수 정의
screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash")

clock = pygame.time.Clock()

#색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#플레이어 관련 변수
player_x = 100
player_y = 300
player_size = 50
player_color = BLUE

#장애물 변수
obstacle_x = screen_width
obstacle_width = 40
obstacle_height = 40

obstacle_y = 350 - obstacle_height
obstacle_speed = 8

#중력을 만들기 위해 필요한 변수들
player_v_y = 0 #y축 속도
gravity = 1.0
jump_pwr = -17
is_jumping = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #마우스 클릭시 점프
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_jumping:
                player_v_y = jump_pwr
                is_jumping = True
    screen.fill(WHITE)
    
    #물리법칙
    player_v_y += gravity
    
    player_y += player_v_y
    
    #만약 중력에 의해 라인보다 밑에 가려고 한다면 고정시키기
    if player_y > 300:
        player_y = 300
        player_v_y = 0
        is_jumping = False
        
    #장애물 이동
    obstacle_x -= obstacle_speed
    if obstacle_x <= -obstacle_width:
        obstacle_x = screen_width
        
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    
    if player_rect.colliderect(obstacle_rect):
        print("Game Over!")
        obstacle_x = screen_width
        
    pygame.draw.rect(screen, player_color,(player_x, player_y, player_size, player_size))
    pygame.draw.line(screen, BLACK, (0, 350), (screen_width, 350), 5)
        
    #삼각형 장애물 그리기
    point_top = (obstacle_x + obstacle_width//2, obstacle_y)
    point_bottom_left = (obstacle_x, obstacle_y+obstacle_height)
    point_bottom_right = (obstacle_x + obstacle_width, obstacle_y+obstacle_height)
    
    triangle_points = [point_top, point_bottom_left, point_bottom_right]
    pygame.draw.polygon(screen, RED, triangle_points)
    pygame.display.update()
    clock.tick(120)
pygame.quit()