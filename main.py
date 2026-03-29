import pygame
import random

pygame.init()
pygame.mixer.init()

#===============================================================================
GAME_MODE = "CUSTOM"

custom_level = [
    # step_up
    # step_down
    # floor_reset
    # cliff
    # obstacle_1
    # obstacle_2
    ("step_up", 2.0),
    ("step_up", 3.0),
    ("floor_reset", 5.0),
    ("obstacle_1", 6.0),
    ("obstacle_2", 7.0),
    ("obstacle_2", 8.0),
    ("step_up", 9.0),
    ("step_up", 10.0),
    ("floor_reset", 11.0),
    ("cliff", 12.0),
    ("cliff", 13.0),
    ("cliff", 14.0),
    ("obstacle_2", 16.0),
    ("step_up", 18.0),
    ("step_up", 19.0),
    ("step_up", 20.0),
    ("cliff", 21.0),
    ("floor_reset", 22.0),
    ("obstacle_2", 23.0),
    ("obstacle_1", 24.0),
    ("obstacle_1", 26.0),
    ("obstacle_1", 28.0),
]

# 게임 변수 정의
screen_width = 800
screen_height = 400
font = pygame.font.SysFont(None, 80)
font_medium = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 30)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash")

pygame.mixer.music.load("Tobu - Higher - Tobu.mp3")

best_progress = 0

total_level_duration = custom_level[-1][1] + 4.0

clock = pygame.time.Clock()

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (100, 100, 100)
GRAY = (200, 200, 200)

# 플레이어 관련 변수
player_size = 50
player_color = BLUE

# 중력 관련 변수
gravity = 1.0
jump_pwr = -17

# 바닥(계단) 관련 변수
floor_speed = 6
floor_height = 350
floor_width = 100

# 장애물 변수
obstacle_width_unit = 40
obstacle_height = 40
# obstacle_type = 1
# obstacle_rect = pygame.Rect(screen_width, 350 - obstacle_height, obstacle_width_unit, obstacle_height)

restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)

def reset_game():
    global player_x, player_y, player_v_y, is_jumping
    global floors, obstacles, start_ticks
    global next_command_idx, game_clear, game_over, last_obstacle_time, current_progress_percent
    player_x = 100
    player_y = 300
    player_v_y = 0
    is_jumping = False
    # 바닥 블록 생성
    floors = []
    for i in range(screen_width // floor_width + 5):
        rect = pygame.Rect(i * floor_width, floor_height, floor_width, 500)
        floors.append(rect)
    obstacles = []
    start_ticks = pygame.time.get_ticks()
    next_command_idx = 0
    game_clear = False
    game_over = False
    last_obstacle_time = 0
    pygame.mixer.music.play(-1)
    current_progress_percent = 0
    
reset_game()

running = True
while running:
    if not game_over and not game_clear:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_ticks) / 1000
        
        progress_ratio = min(1.0, elapsed_time / total_level_duration)
        current_progress_percent = int(progress_ratio * 100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if restart_button_rect.collidepoint(event.pos):
                    reset_game()
           
    if pygame.mouse.get_pressed()[0]: #마우스 꾹 누르면 연속적으로 점프
        if not is_jumping:
            player_v_y = jump_pwr
            is_jumping = True
    if GAME_MODE == "CUSTOM" and not game_clear:
        if next_command_idx >= len(custom_level):
            last_cmd_time = custom_level[-1][1]
            if elapsed_time > last_cmd_time + 4.0:
                game_clear = True
    if not game_over:
        if game_clear:
            player_x += 5
            
        # 물리법칙
        player_v_y += gravity
        player_y += player_v_y
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
        if not game_clear and player_y > screen_height:
            game_over = True
            pygame.mixer.music.stop()
   
    # --- 바닥 생성 알고리즘 ---
    if not game_clear and not game_over:
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
    if not game_over:
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
                        game_over = True
                        pygame.mixer.music.stop()
                    
        if not on_ground and player_v_y == 0:
            is_jumping = True
        if not game_clear:
            for obs in obstacles:
                collision_box = obs['rect'].inflate(-15, -15)
                if player_rect.colliderect(collision_box):
                    game_over = True
                    pygame.mixer.music.stop()
                    
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
    
    bar_width = 400
    bar_height = 20
    bar_x = (screen_width - bar_width) // 2
    bar_y = 20
    
    pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), 3)
    fill_width = int(bar_width * progress_ratio)
    
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
    
    percent_text = font_small.render(f"{current_progress_percent}%", True, BLACK)
    screen.blit(percent_text, (bar_x+bar_width+10,bar_y))
    
    if game_clear:
        best_progress = max(current_progress_percent, best_progress)
        
        win_text = font.render("GAME CLEAR!", True, GREEN)
        win_text_rect = win_text.get_rect(center = (screen_width / 2, screen_height/2))
        screen.blit(win_text, win_text_rect)
        
    if game_over:
        best_progress = max(current_progress_percent, best_progress)
        
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        fail_text = font.render("GAME OVER!", True, RED)
        fail_text_rect = fail_text.get_rect(center = (screen_width / 2, screen_height/2))
        screen.blit(fail_text, fail_text_rect)
        
        pygame.draw.rect(screen, BLUE, restart_button_rect, border_radius=10)
        button_text = font_medium.render("RESTART", True, WHITE)
        button_text_rect = button_text.get_rect(center = restart_button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        progress_text = font_medium.render(f"Your Progress: {current_progress_percent}% | Best Progress: {best_progress}%", True, BLACK)
        progress_text_rect = progress_text.get_rect(center = (screen_width // 2, screen_height // 2 - 80))
        screen.blit(progress_text, progress_text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()