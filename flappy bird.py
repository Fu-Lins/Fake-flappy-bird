import pygame
import random

pygame.init()

# Ekran boyutları ve hız ayarları
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 36)

# Renkler
WHITE = (255, 255, 255)

# Resimler
bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

# Kuşun özellikleri
bird_rect = bird_images[0].get_rect(topleft=(100, HEIGHT // 2))
bird_speed = 0
bird_acceleration = 1
bird_flap = -12
flap_count = 0

# Boru özellikleri
pipe_width = 50
pipe_height = 300
pipe_x = WIDTH
pipe_gap = 200
pipe_speed = 5

# Oyun durumu
score = 0
game_over = False

def draw_bird():
    global flap_count
    SCREEN.blit(bird_images[flap_count // 5], bird_rect)
    flap_count += 1
    if flap_count >= 15:
        flap_count = 0

def draw_pipe(pipe_x, pipe_height):
    SCREEN.blit(top_pipe_image, (pipe_x, pipe_height - top_pipe_image.get_height()))
    SCREEN.blit(bottom_pipe_image, (pipe_x, pipe_height + pipe_gap))


def check_collision(pipe_x, pipe_height):
    if bird_rect.x + bird_rect.width > pipe_x and bird_rect.x < pipe_x + pipe_width:
        if bird_rect.y < pipe_height or bird_rect.y + bird_rect.height > pipe_height + pipe_gap:
            return True
    return False

def game_over_screen():
    game_over_text = FONT.render("Game Over", True, WHITE)
    restart_text = FONT.render("Press 'R' to Restart", True, WHITE)
    SCREEN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    SCREEN.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_speed = bird_flap

    bird_speed += bird_acceleration
    bird_rect.y += bird_speed

    SCREEN.blit(skyline_image, (0, 0))

    draw_bird()
    draw_pipe(pipe_x, pipe_height)

    if check_collision(pipe_x, pipe_height) or bird_rect.y < 0 or bird_rect.y + bird_rect.height > HEIGHT:
        game_over_screen()
        bird_rect.y = HEIGHT // 2
        pipe_x = WIDTH
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
        score = 0
        bird_speed = 0
        bird_acceleration = 1
    pipe_x -= pipe_speed

    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
        score += 1

    score_text = FONT.render("Score: " + str(score), True, WHITE)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()   
