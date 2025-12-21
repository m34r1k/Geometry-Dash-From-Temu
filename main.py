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

#플레이어 관련 변수
player_x = 100
player_y = 300
player_size = 50
player_color = BLUE

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
    pygame.draw.rect(screen, player_color,(player_x, player_y, player_size, player_size))
    pygame.draw.line(screen, BLACK, (0, 350), (screen_width, 350), 5)
        
    pygame.display.update()
    clock.tick(60)
pygame.quit()