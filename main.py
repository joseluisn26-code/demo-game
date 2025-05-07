import pygame
import sys
import random

# Initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)

# Font
font = pygame.font.SysFont("Arial", 30)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo Game")
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def update(self):
        self.handle_input()

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 200)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Function to show menu
def show_menu():
    while True:
        screen.fill((0, 0, 0))
        title = font.render("Welcome to Demo Game", True, (255, 255, 255))
        subtitle = font.render("Press ENTER to play or ESC to Exit", True, (200, 200, 200))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Function to show Game Over and then return to the menu
def show_game_over(score):
    screen.fill((0, 0, 0))
    text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    show_menu()

# Function to start the game
def start_game():
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.right, player.rect.centery)
                    bullet_group.add(bullet)
            elif event.type == pygame.USEREVENT + 1:
                enemy = Enemy()
                enemy_group.add(enemy)

        player_group.update()
        bullet_group.update()
        enemy_group.update()

        # Collisions
        collisions = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
        score += len(collisions)

        if pygame.sprite.spritecollideany(player, enemy_group):
            return score

        screen.fill(BACKGROUND_COLOR)
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

# Main Loop
while True:
    show_menu()
    score = start_game()
    show_game_over(score)
    pygame.event.clear()