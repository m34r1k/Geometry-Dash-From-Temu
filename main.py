import pygame
import random

pygame.init()

#===============================================================================
GAME_MODE = "CUSTOM"

custom_level = [
    ("step_up", 2.0),
    ("floor_reset", 4.0),
    ("obstacle_2", 4.0,)
]

# 게임 변수 정의
screen_width = 800
screen_height = 400
font = pygame.font.SysFont(None, 80)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash")

clock = pygame.time.Clock()

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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
obstacles = []
obstacle_width_unit = 40
obstacle_height = 40
# obstacle_type = 1
# obstacle_rect = pygame.Rect(screen_width, 350 - obstacle_height, obstacle_width_unit, obstacle_height)
start_ticks = pygame.time.get_ticks()

next_command_idx = 0
game_clear = False
last_obstacle_time = 0

running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_ticks) // 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
    if pygame.mouse.get_pressed()[0]: #마우스 꾹 누르면 연속적으로 점프
        if not is_jumping:
            player_v_y = jump_pwr
            is_jumping = True
    if GAME_MODE == "CUSTOM" and not game_clear:
        if next_command_idx >= len(custom_level):
            last_cmd_time = custom_level[-1][1]
            if elapsed_time > last_cmd_time + 4.0:
                game_clear = True
    if game_clear:
        player_x += 5
            
    # 물리법칙
    player_v_y += gravity
    player_y += player_v_y
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    if not game_clear and player_y > screen_height:
        running = False
        print("낭떠러지에서 추락! Game Over!")
   
    # --- 바닥 생성 알고리즘 ---
    if not game_clear:
        last_floor = floors[-1]
        if last_floor.right <= screen_width + floor_width * 2:
            
            new_y = last_floor.y
            new_x = last_floor.right

            is_gap = False
            spawn_obs_type = 0
            if GAME_MODE == "CUSTOM":
                if next_command_idx < len(custom_level):
                    cmd_name, cmd_time = custom_level[next_command_idx]
                    if elapsed_time >= cmd_time:
                        if cmd_name == "step_up": new_y -= player_size
                        elif cmd_name == "step_down": new_y += player_size
                        elif cmd_name == "floor_reset": new_y = 350
                        elif cmd_name == "cliff": is_gap = True
                        elif cmd_name == "obstacle_1": spawn_obs_type = 1
                        elif cmd_name == "obstacle_2": spawn_obs_type = 2
                        next_command_idx += 1
            
            # if rand_val < 10:
            #     is_gap = True
            
            # elif rand_val < 40:
            #     new_y -= player_size
            # elif rand_val < 70:
            #     new_y += player_size * random.randint(1, 3)
        
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

            if spawn_obs_type > 0 and not is_gap:
                obs_width = obstacle_width_unit * spawn_obs_type
                new_obs_rect = pygame.Rect(0, 0, obs_width, obstacle_height)
                new_obs_rect.centerx = new_block.centerx
                new_obs_rect.bottom = new_block.top
                obstacles.append({'rect': new_obs_rect, 'type': spawn_obs_type})
                
        if floors[0].right < 0:
            floors.pop(0)
            
        for floor in floors:
            floor.x -= floor_speed
            
        active_obstacles = []
        for obs in obstacles:
            rect = obs['rect']
            rect.x -= floor_speed
            for floor in floors:
                if floor.left <= rect.centerx <= floor.right:
                    rect.bottom = floor.top
                    break
                
            if rect.right > 0:
                active_obstacles.append(obs)
        obstacles = active_obstacles
       
    # 이동 및 충돌 검사
    on_ground = False
   
    for floor in floors:      
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
                if player_rect.right > floor.left + 10 and not game_clear:
                    print("벽에 부딪힘! Game Over!")
                    running = False
                   
    if not on_ground and player_v_y == 0:
        is_jumping = True
    if not game_clear:
        for obs in obstacles:
            collision_box = obs['rect'].inflate(-15, -15)
            if player_rect.colliderect(collision_box):
                print("가시에 찔림. Game Over!")
                running = False
    # 그리기
    screen.fill(WHITE)
   
    for floor in floors:
        pygame.draw.rect(screen, BLACK, floor)
   
    for obs in obstacles:
        rect = obs['rect']
        o_type = obs['type']
        if o_type == 1:
            p1 = (rect.centerx, rect.top)
            p2 = (rect.left, rect.bottom)
            p3 = (rect.right, rect.bottom)
            pygame.draw.polygon(screen, RED, [p1, p2, p3])
        else:
            mid_width = obstacle_width_unit
            p1 = (rect.left + mid_width/2, rect.top)
            p2 = (rect.left, rect.bottom)
            p3 = (rect.left + mid_width, rect.bottom)
            pygame.draw.polygon(screen, RED, [p1, p2, p3])
            p4 = (rect.left + mid_width + mid_width/2, rect.top)
            p5 = (rect.left + mid_width, rect.bottom)
            p6 = (rect.right, rect.bottom)
            pygame.draw.polygon(screen, RED, [p4, p5, p6])
            
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
    
    if game_clear:
        win_text = font.render("GAME CLEAR!", True, GREEN)
        win_text_rect = win_text.get_rect(center = (screen_width / 2, screen_height/2))
        screen.blit(win_text, win_text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
