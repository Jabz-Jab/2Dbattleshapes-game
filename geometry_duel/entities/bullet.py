# entities/bullet.py
import pygame
from settings import BULLET_LIFE, WIDTH, HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel, owner="player", dmg=1):
        super().__init__()
        self.owner = owner
        self.dmg = dmg
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.life = BULLET_LIFE

        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        if owner == "player":
            pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 4)
            pygame.draw.circle(self.image, (120, 220, 255), (5, 5), 2)
        else:
            pygame.draw.circle(self.image, (255, 230, 120), (5, 5), 4)
            pygame.draw.circle(self.image, (255, 120, 80), (5, 5), 2)

        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.radius = 4

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()
            return

        self.pos += self.vel * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if (
            self.rect.right < -40 or self.rect.left > WIDTH + 40 or
            self.rect.bottom < -40 or self.rect.top > HEIGHT + 40
        ):
            self.kill()
