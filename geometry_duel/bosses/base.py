# bosses/base.py
import pygame
from settings import WIDTH, HEIGHT
from utils import clamp

class BossBase:
    def __init__(self, name, img, hp):
        self.name = name
        self.base = img
        self.image = img

        self.max_hp = hp
        self.hp = hp
        self.dead = False

        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT * 0.23)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.radius = max(self.rect.width, self.rect.height) * 0.42

    def reset(self):
        self.hp = self.max_hp
        self.dead = False
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT * 0.23)
        self.image = self.base
        self.sync()

    def damage(self, d):
        self.hp -= d
        if self.hp <= 0:
            self.hp = 0
            self.dead = True

    def sync(self):
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        hx, hy = self.rect.width // 2, self.rect.height // 2
        self.pos.x = clamp(self.pos.x, hx, WIDTH - hx)
        self.pos.y = clamp(self.pos.y, hy, HEIGHT - hy)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.radius = max(self.rect.width, self.rect.height) * 0.42

    def draw(self, screen):
        screen.blit(self.image, self.rect)
