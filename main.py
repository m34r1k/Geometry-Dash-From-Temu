import pygame
import random

pygame.init()

# 게임 변수 정의
screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash")

clock = pygame.time.Clock()

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 플레이어 관련 변수
player_x = 100
player_y = 300
player_size = 50
player_color = BLUE

# 중력 관련 변수
player_v_y = 0
gravity = 1.0
jump_pwr = -17
is_jumping = False

# 바닥(계단) 관련 변수
floor_speed = 6
floor_height = 350
floor_width = 100

# 바닥 블록 생성
floors = []
for i in range(screen_width // floor_width + 5):
    rect = pygame.Rect(i * floor_width, floor_height, floor_width, 500)
    floors.append(rect)

# 장애물 변수
obstacle_width_unit = 40
obstacle_height = 40
obstacle_type = 1
obstacle_rect = pygame.Rect(screen_width, 350 - obstacle_height, obstacle_width_unit, obstacle_height)

def reset_obstacle():
    global obstacle_type
    obstacle_type = random.choice([1, 2])
    obstacle_rect.width = obstacle_width_unit * obstacle_type
   
    candidate_floors = [f for f in floors if f.left > screen_width]
   
    if candidate_floors:
      
        target_floor = random.choice(candidate_floors[:3])  
        
        obstacle_rect.centerx = target_floor.centerx
        
        obstacle_rect.bottom = target_floor.top
    else:
        obstacle_rect.x = screen_width + 200

# 초기 장애물 설정
reset_obstacle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
    if pygame.mouse.get_pressed()[0]: #마우스 꾹 누르면 연속적으로 점프
        if not is_jumping:
            player_v_y = jump_pwr
            is_jumping = True
   
    # 물리법칙
    player_v_y += gravity
    player_y += player_v_y
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    if player_y > screen_height:
        running = False
        print("낭떠러지에서 추락! Game Over!")
   
    # --- 바닥 생성 알고리즘 ---
    last_floor = floors[-1]

    if last_floor.right <= screen_width + floor_width * 2:
        
        new_y = last_floor.y
        rand_val = random.randint(0, 100)

        is_gap = False
        
        if rand_val < 10:
            is_gap = True
        
        elif rand_val < 40:
            new_y -= player_size
        elif rand_val < 70:
            new_y += player_size * random.randint(1, 3)
       
        if new_y < 200:
            new_y = 200
        if new_y > 350:
            new_y = 350
           
        if is_gap == True:
            new_x = last_floor.right + floor_width
        else:
            new_x = last_floor.right
        new_block = pygame.Rect(new_x, new_y, floor_width, 500)
        floors.append(new_block)

    if floors[0].right < 0:
        floors.pop(0)
       
    # 이동 및 충돌 검사
    on_ground = False
   
    for floor in floors:
        floor.x -= floor_speed
       
        if player_rect.colliderect(floor):
            # 점프 중(상승 중)일 때는 바닥 무시
            if player_v_y < 0:
                continue

            # 착지 판정
            if player_rect.bottom <= floor.top + 20 and player_v_y >= 0:
                player_y = floor.top - player_size
                player_v_y = 0
                is_jumping = False
                on_ground = True
            else:
                # 옆면 충돌 판정
                if player_rect.right > floor.left + 10:
                    print("벽에 부딪힘! Game Over!")
                    running = False
                   
    if not on_ground and player_v_y == 0:
        is_jumping = True
       
    # --- 장애물 이동 ---
    obstacle_rect.x -= floor_speed
   
    # 실시간 높이 보정 (장애물이 바닥 위에 떠있지 않게)
    # 현재 장애물 위치의 바닥을 찾아서 그 위에 딱 붙임
    for floor in floors:
        if floor.left <= obstacle_rect.centerx <= floor.right:
            obstacle_rect.bottom = floor.top
            break
           
    if obstacle_rect.right < 0:
        reset_obstacle()
       
    # 장애물 충돌 검사
    collision_box = obstacle_rect.inflate(-15, -15)
    if player_rect.colliderect(collision_box):
        print("가시에 찔림. Game Over!")
        running = False
   
    # 그리기
    screen.fill(WHITE)
   
    for floor in floors:
        pygame.draw.rect(screen, BLACK, floor)
   
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
       
    if obstacle_type == 1:
        p1 = (obstacle_rect.centerx, obstacle_rect.top)
        p2 = (obstacle_rect.left, obstacle_rect.bottom)
        p3 = (obstacle_rect.right, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p1, p2, p3])
    else:
        mid_width = obstacle_width_unit
        p1 = (obstacle_rect.left + mid_width/2, obstacle_rect.top)
        p2 = (obstacle_rect.left, obstacle_rect.bottom)
        p3 = (obstacle_rect.left + mid_width, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p1, p2, p3])
        p4 = (obstacle_rect.left + mid_width + mid_width/2, obstacle_rect.top)
        p5 = (obstacle_rect.left + mid_width, obstacle_rect.bottom)
        p6 = (obstacle_rect.right, obstacle_rect.bottom)
        pygame.draw.polygon(screen, RED, [p4, p5, p6])

    pygame.display.update()
    clock.tick(60)

pygame.quit()
