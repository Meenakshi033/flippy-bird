import pygame, sys, random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐦 Flappy Bird - Level Edition")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 180, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 230, 0)
ORANGE = (255, 165, 0)
RED = (220, 30, 30)
BROWN = (139, 69, 19)
GRAY = (60, 60, 60)

# Game variables
gravity = 0.4
bird_movement = 0
bird_x, bird_y = 100, HEIGHT // 2
bird_radius = 14
pipe_gap = 180
pipe_speed = 4
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

game_active = False
menu_active = True
score = 0
level = 1
font = pygame.font.SysFont("Comic Sans MS", 28, True)

# Animation variables
level_up_timer = 0
LEVELUP_DURATION = 60  # frames to display “LEVEL UP!”

def create_pipe():
    height = random.randint(150, 400)
    bottom = pygame.Rect(WIDTH, height, 60, HEIGHT - height)
    top = pygame.Rect(WIDTH, 0, 60, height - pipe_gap)
    return bottom, top

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= pipe_speed
    return [p for p in pipes if p.right > 0]

def draw_pipes(pipes):
    for p in pipes:
        pygame.draw.rect(screen, GREEN, p, border_radius=5)
        pygame.draw.rect(screen, BROWN, (p.x, p.bottom if p.y == 0 else p.y - 10, 60, 10))  # pipe edge

def check_collision():
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    for p in pipes:
        if bird_rect.colliderect(p):
            return False
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT - 40:
        return False
    return True

def display_text(text, y, color=WHITE, size=28):
    f = pygame.font.SysFont("Comic Sans MS", size, True)
    s = f.render(text, True, color)
    screen.blit(s, (WIDTH // 2 - s.get_width() // 2, y))

def draw_button(text, rect, color, hover_color, mouse_pos):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=15)
    else:
        pygame.draw.rect(screen, color, rect, border_radius=15)
    display_text(text, rect.y + 10, WHITE, 24)

def draw_bird(x, y):
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), bird_radius)
    pygame.draw.polygon(screen, ORANGE, [(x + 12, y - 3), (x + 22, y), (x + 12, y + 3)])  # Beak
    pygame.draw.circle(screen, WHITE, (int(x - 5), int(y - 5)), 4)  # Eye
    pygame.draw.circle(screen, (0, 0, 0), (int(x - 5), int(y - 5)), 2)

def reset_game():
    global pipes, bird_x, bird_y, bird_movement, score, level, pipe_speed, passed_pipes, level_up_timer
    pipes.clear()
    bird_x, bird_y = 100, HEIGHT // 2
    bird_movement = 0
    score = 0
    level = 1
    pipe_speed = 4
    passed_pipes = []
    level_up_timer = 0

# Game loop
passed_pipes = []

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 30, 160, 50)
                exit_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
                if start_button.collidepoint(mouse_pos):
                    menu_active = False
                    game_active = True
                    reset_game()
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8
            if event.key == pygame.K_SPACE and not game_active and not menu_active:
                game_active = True
                reset_game()

        if event.type == SPAWNPIPE and game_active:
            bottom, top = create_pipe()
            pipes.extend([bottom, top])
            passed_pipes.append(False)  # track each bottom pipe once

    screen.fill(BLUE)

    if menu_active:
        display_text("🐤 Flappy Bird", 150, WHITE, 38)
        start_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 30, 160, 50)
        exit_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
        draw_button("Start", start_button, ORANGE, RED, mouse_pos)
        draw_button("Exit", exit_button, GRAY, RED, mouse_pos)

    elif game_active:
        # Bird
        bird_movement += gravity
        bird_y += bird_movement
        draw_bird(bird_x, bird_y)

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Ground
        pygame.draw.rect(screen, RED, (0, HEIGHT - 40, WIDTH, 40))

        # Collision
        game_active = check_collision()

        # Level System (score hidden)
        bottom_pipes = [pipes[i] for i in range(0, len(pipes), 2)]
        for i, bp in enumerate(bottom_pipes):
            if bp.right < bird_x and not passed_pipes[i]:
                score += 1
                passed_pipes[i] = True

                if score % 10 == 0:
                    level += 1
                    pipe_speed = 4 + level
                    pipe_gap = max(120, 180 - level * 5)
                    level_up_timer = LEVELUP_DURATION

        # Only show Level
        display_text(f"Level: {level}", 20)

        if level_up_timer > 0:
            display_text("LEVEL UP!", HEIGHT // 2 - 60, YELLOW, 36)
            level_up_timer -= 1

    else:
        display_text("GAME OVER 💥", HEIGHT // 2 - 60, RED, 36)
        display_text(f"Level Reached: {int(level)}", HEIGHT // 2 - 10)
        display_text("Press SPACE to Restart", HEIGHT // 2 + 40, WHITE, 22)
        display_text("Press ESC for Menu", HEIGHT // 2 + 70, WHITE, 22)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            menu_active = True

    pygame.display.update()
    clock.tick(60)




