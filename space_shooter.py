import pygame
import random
import sys

WIDTH, HEIGHT = 600, 800
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = -8
ENEMY_SPEED = 2
ENEMY_DROP = 40

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 10))

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self) -> "Bullet":
        return Bullet(self.rect.centerx, self.rect.top)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = ENEMY_SPEED

    def update(self) -> None:
        self.rect.x += self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += ENEMY_DROP


def create_enemies(group: pygame.sprite.Group, rows: int = 3, cols: int = 6) -> None:
    for r in range(rows):
        for c in range(cols):
            x = 60 + c * 80
            y = 60 + r * 60
            group.add(Enemy(x, y))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    create_enemies(enemies)

    font = pygame.font.SysFont(None, 36)
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.add(player.shoot())

        player_group.update()
        bullets.update()
        enemies.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        score += len(hits)

        if pygame.sprite.spritecollideany(player, enemies):
            running = False
        else:
            for e in enemies:
                if e.rect.bottom >= HEIGHT:
                    running = False
                    break

        if not enemies:
            create_enemies(enemies)

        screen.fill((0, 0, 0))
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)

        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    game_over_font = pygame.font.SysFont(None, 64)
    text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
