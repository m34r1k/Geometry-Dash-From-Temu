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
        
    #모든 바닥 블록 왼쪽으로 이동 및 충돌 검사
    on_ground = False
    
    for floor in floors:
        floor.x -= floor_speed
        #플레이어랑 바닥 블록이 겹쳤는지 확인
        if player_rect.colliderect(floor):
            #충돌 판단 (바닥이 닿았나 옆에 닿았나)
            #플레이어 발바닥이 블록 윗면 근처이고 아래로 떨어지는 중일때 -> 착지 성공
            if player_rect.bottom <= floor.top + 15 and player_v_y >= 0:
                player_y = floor.top-player_size
                player_v_y = 0
                is_jumping = False
                on_ground = True
            else:
                #옆에 부딫혔을 때 게임 오버
                print("Game Over!")
                running = False
                
    #땅에 닿지 않았다면 점프 상태로 변경 (계단에서 떨어질 때)
    if not on_ground and player_v_y == 0:
        is_jumping = True
        
    #장애물 이동 및 충돌
    obstacle_rect.y = 350-obstacle_height
    obstacle_rect.x -= floor_speed
    
    if obstacle_rect.right < 0:
        reset_obstacle()
        
    #장애물 충돌 검사
    collision_box = obstacle_rect.inflate(-10 ,-10)
    if player_rect.colliderect(collision_box):
        print("가시에 찔림. Game Over!")
        running = False
    
    #화면 그리기
    screen.fill(WHITE)
    
    #바닥 그리기
    for floor in floors:
        pygame.draw.rect(screen, BLACK, floor)
    
    #플레이어 그리기
    pygame.draw.rect(screen, player_color,(player_x, player_y, player_size, player_size))
        
    #삼각형 장애물 그리기
    if obstacle_type == 1:
        # 삼각형 1개
        p1 = (obstacle_rect.centerx, obstacle_rect.top)
        p2 = (obstacle_rect.left, obstacle_rect.bottom)
        p3 = (obstacle_rect.right, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p1, p2, p3])
    else:
        # 삼각형 2개 (반반 나누어서 그림)
        mid_width = obstacle_width_unit
        # 첫 번째 가시
        p1 = (obstacle_rect.left + mid_width/2, obstacle_rect.top)
        p2 = (obstacle_rect.left, obstacle_rect.bottom)
        p3 = (obstacle_rect.left + mid_width, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p1, p2, p3])
        # 두 번째 가시
        p4 = (obstacle_rect.left + mid_width + mid_width/2, obstacle_rect.top)
        p5 = (obstacle_rect.left + mid_width, obstacle_rect.bottom)
        p6 = (obstacle_rect.right, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p4, p5, p6])

    pygame.display.update()
    clock.tick(60)
pygame.quit()