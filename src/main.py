"""
made by squirrel acorns

4/11/2025 9:56 PM

I don't own flappybird or some shit so yea
"""
import pygame
import sys
import random
import os
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 400, 600
FPS = 60
PIPE_GAP = 150
PIPE_WIDTH = 60
GROUND_SPEED = -3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
def load_resource(name, folder="assets"):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, folder, name)
    try:
        if ".png" in name:
            img = pygame.image.load(filepath).convert_alpha()
            return img
        elif ".mp3" in name:
            return pygame.mixer.Sound(filepath)
        else:
            return None
    except Exception as e:
        print(f"Error loading resource {name}: {e}")
        return None
def load_image(name, scale=None):
    img = load_resource(name)
    if img and scale:
        return pygame.transform.scale(img, scale)
    return img
def load_sound(name):
    return load_resource(name)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stupid Flappy Bird rygewuheijo")
pygame.display.set_icon(load_image("icon.png"))
clock = pygame.time.Clock()
number_sprites = [load_image(f"{i}.png") for i in range(10)]
background = load_image("background-night.png", (WIDTH, HEIGHT))
ground_img = load_image("base.png")
ground_height = ground_img.get_height()
ground_y = HEIGHT - ground_height
ground_group = pygame.sprite.Group()
pipe_img = load_image("pipe-green.png")
bird_frames = [
    load_image("bird1.png", (50, 35)),
    load_image("bird2.png", (50, 35)),
    load_image("bird3.png", (50, 35)),
]
game_over_img = load_image("gameover.png")
start_img = load_image("message.png", (WIDTH, HEIGHT))
flap_sound = load_sound("flap.mp3")
hit_sound = load_sound("hit.mp3")
point_sound = load_sound("point.mp3")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 60)
restart_font = pygame.font.Font(None, 28)
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = bird_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.vel = 0
        self.gravity = 0.5
        self.flap_power = -10
        self.anim_counter = 0
    def update(self):
        self.vel += self.gravity
        self.rect.y += self.vel
        self.anim_counter += 1
        if self.anim_counter % 5 == 0:
            self.index = (self.index + 1) % len(self.frames)
        rotated = pygame.transform.rotate(self.frames[self.index], -self.vel * 2)
        self.image = rotated
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.top < 0:
            self.rect.top = 0
    def flap(self):
        self.vel = self.flap_power
        if flap_sound:
            flap_sound.play()
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        super().__init__()
        self.flipped = flipped
        height = y if flipped else HEIGHT - y - PIPE_GAP - ground_height
        self.image = pygame.transform.scale(pipe_img, (PIPE_WIDTH, height))
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y + PIPE_GAP))
        self.speed = GROUND_SPEED
        self.passed = False
    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, group):
        super().__init__()
        self.image = ground_img
        self.rect = self.image.get_rect(topleft=(x, ground_y))
        self.speed = GROUND_SPEED
        self.group = group
    def update(self):
        self.rect.x += self.speed
        if self.rect.right <= 0:
            self.rect.left = max(g.rect.right for g in self.group if g != self)
def show_score(score):
    score_str = str(score)
    x_offset = 0
    for digit in score_str:
        image = number_sprites[int(digit)]
        rect = image.get_rect(topleft=(10 + x_offset, 10))
        screen.blit(image, rect)
        x_offset += image.get_width() + 5
def show_game_over(score):
    game_over_rect = game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(game_over_img, game_over_rect)
    score_str = str(score)
    total_width = 0
    score_surfaces = [number_sprites[int(digit)] for digit in score_str]
    for surf in score_surfaces:
        total_width += surf.get_width() + 5
    start_x = WIDTH // 2 - total_width // 2
    score_y = game_over_rect.bottom + 30
    for surf in score_surfaces:
        screen.blit(surf, (start_x, score_y))
        start_x += surf.get_width() + 5
    restart_text = restart_font.render("press anything to restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, score_y + 50))
    screen.blit(restart_text, restart_rect)
def show_start_screen():
    bird = Bird()
    bird.vel = 0
    ground_group = pygame.sprite.Group()
    g1 = Ground(0, ground_group)
    g2 = Ground(g1.rect.width, ground_group)
    g3 = Ground(g2.rect.right, ground_group)
    ground_group.add(g1, g2, g3)
    small_start_img = pygame.transform.scale(start_img, (200, 300))
    rect = small_start_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        bird.anim_counter += 1
        if bird.anim_counter % 5 == 0:
            bird.index = (bird.index + 1) % len(bird.frames)
        bird.image = bird.frames[bird.index]
        bird.rect = bird.image.get_rect(center=(WIDTH // 2, HEIGHT // 2.5))
        ground_group.update()
        screen.blit(background, (0, 0))
        screen.blit(bird.image, bird.rect)
        for ground in ground_group:
            screen.blit(ground.image, ground.rect.topleft)
        screen.blit(small_start_img, rect)
        pygame.display.flip()
        clock.tick(FPS)
def create_pipe_pair():
    y = random.randint(100, HEIGHT - PIPE_GAP - ground_height - 100)
    return Pipe(WIDTH, y, True), Pipe(WIDTH, y, False)
def game():
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    bird = Bird()
    all_sprites.add(bird)
    g1 = Ground(0, ground_group)
    g2 = Ground(g1.rect.width, ground_group)
    g3 = Ground(g2.rect.right, ground_group)
    ground_group.add(g1, g2, g3)
    all_sprites.add(g1, g2, g3)
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1400)
    score = 0
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    bird.flap()
            elif game_over:
                return
            if event.type == SPAWNPIPE and not game_over:
                top, bottom = create_pipe_pair()
                all_sprites.add(top, bottom)
                pipes.add(top, bottom)
        if not game_over:
            all_sprites.update()
            if pygame.sprite.spritecollideany(bird, pipes) or bird.rect.bottom >= ground_y:
                game_over = True
                if hit_sound:
                    hit_sound.play()
            for pipe in pipes:
                if not pipe.passed and not pipe.flipped and pipe.rect.right < bird.rect.left:
                    pipe.passed = True
                    score += 1
                    if point_sound:
                        point_sound.play()
            if bird.rect.bottom > ground_y:
                bird.rect.bottom = ground_y
        screen.blit(background, (0, 0))
        pipes.draw(screen)
        screen.blit(bird.image, bird.rect)
        for ground in ground_group:
            screen.blit(ground.image, ground.rect.topleft)
        show_score(score)
        if game_over:
            show_game_over(score)
        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    while True:
        show_start_screen()
        game()
