import pygame
import random

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

#중력을 만들기 위해 필요한 변수들
player_v_y = 0 #y축 속도
gravity = 1.0
jump_pwr = -17
is_jumping = False

#바닥(계단) 관련 변수
floor_speed = 6
floor_height = 350
floor_width = 100

#바닥 블록 생성
floors = []
for i in range(screen_width//floor_width+2):
    #길이를 아주 길게 하여 밑으로 뚫리지 않게 함
    rect = pygame.Rect(i*floor_width, floor_height, floor_width, 500)
    floors.append(rect)

#장애물 변수
obstacle_width_unit = 40
obstacle_height = 40

obstacle_type = 1
obstacle_rect = pygame.Rect(screen_width, 0, obstacle_width_unit, obstacle_height)

def reset_obstacle(): #장애물을 화면 끝으로 보내고 한개일지 두개일지 정하는 함수
    global obstacle_type
    obstacle_type = random.choice([1, 2])
    obstacle_rect.width = obstacle_width_unit * obstacle_type
    obstacle_rect.x = screen_width + random.randint(0, 200)

reset_obstacle()

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
    
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    #바닥 생성 알고리즘
    #가장 마지막 블록 마지막 끝을 찾기
    #마지막 블록이 끝나면 그 뒤에 새로운 블럭을 이어붙인다.
    last_floor = floors[-1]
    if last_floor.right <= screen_width + floor_width:
        new_y = last_floor.y
        rand_val = random.randint(0, 10)
        if rand_val < 2:
            new_y -= player_size
        elif rand_val < 4:
            new_y += player_size
        #블록이 너무 높아져도, 너무 낮아져도 안된다.
        if new_y < 200:
            new_y = 200
        if new_y < 400:
            new_y = 400
        new_block = pygame.Rect(last_floor.right, new_y, floor_width, 500)
        floors.append(new_block)
    if floors[0].right < 0:
        floors.pop(0)
        
    #만약 중력에 의해 라인보다 밑에 가려고 한다면 고정시키기
    if player_y > 300:
        player_y = 300
        player_v_y = 0
        is_jumping = False
        
    #장애물 이동
    obstacle_x -= obstacle_speed
    if obstacle_x <= -obstacle_width:
        obstacle_x = screen_width
        
    obstacle2_x -= obstacle_speed
    if obstacle2_x <= -obstacle_width:
        obstacle2_x = screen_width
        
    #각 오브젝트 rect
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    obstacle2_rect = pygame.Rect(obstacle2_x, obstacle_y, obstacle_width, obstacle_height)
    
    if player_rect.colliderect(obstacle_rect):
        print("Game Over!")
        obstacle_x = screen_width
    if player_rect.colliderect(obstacle2_rect):
        print("Game Over!")
        obstacle2_x = screen_width
    
    #플레이어 그리기
    pygame.draw.rect(screen, player_color,(player_x, player_y, player_size, player_size))
    #바닥 그리기
    pygame.draw.line(screen, BLACK, (0, 350), (screen_width, 350), 5)
        
    #삼각형 장애물 그리기
    point_top = (obstacle_x + obstacle_width//2, obstacle_y)
    point_bottom_left = (obstacle_x, obstacle_y+obstacle_height)
    point_bottom_right = (obstacle_x + obstacle_width, obstacle_y+obstacle_height)
    
    point_top2 = (obstacle2_x + obstacle_width//2, obstacle_y)
    point_bottom_left2 = (obstacle2_x, obstacle_y+obstacle_height)
    point_bottom_right2 = (obstacle2_x + obstacle_width, obstacle_y+obstacle_height)
    
    triangle_points = [point_top, point_bottom_left, point_bottom_right]
    triangle_points2 = [point_top2, point_bottom_left2, point_bottom_right2]
    
    pygame.draw.polygon(screen, RED, triangle_points)
    pygame.draw.polygon(screen, RED, triangle_points2)
    pygame.display.update()
    clock.tick(60)
pygame.quit()