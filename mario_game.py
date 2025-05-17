import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_POWER = -10
MOVE_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.bottom
                    self.vel_y = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, path_length=100):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.path_start = x
        self.path_length = path_length
        self.direction = 1
    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.x > self.path_start + self.path_length or self.rect.x < self.path_start:
            self.direction *= -1

def create_level():
    platforms = [
        pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
        pygame.Rect(200, HEIGHT - 150, 120, 20),
        pygame.Rect(400, HEIGHT - 250, 120, 20),
    ]
    return platforms

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Mario Clone")
    clock = pygame.time.Clock()

    player = Player(50, HEIGHT - 90)
    enemy = Enemy(500, HEIGHT - 80)
    all_sprites = pygame.sprite.Group(player, enemy)
    platforms = create_level()

    running = True
    game_over = False
    font = pygame.font.SysFont(None, 48)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            player.update(platforms)
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                game_over = True

        screen.fill((135, 206, 235))  # sky blue background
        for p in platforms:
            pygame.draw.rect(screen, (0, 128, 0), p)
        all_sprites.draw(screen)

        if game_over:
            text = font.render("GAME OVER", True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
