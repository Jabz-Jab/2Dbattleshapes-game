# entities/minion.py
import pygame
from settings import MINION_SPEED, MINION_HP

class Minion(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(int(pos.x), int(pos.y)))
        self.pos = pygame.Vector2(pos)
        self.radius = max(self.rect.width, self.rect.height) * 0.33
        self.hp = MINION_HP

    def update(self, dt, player_pos):
        v = player_pos - self.pos
        if v.length_squared() > 0:
            d = v.normalize()
            self.pos += d * MINION_SPEED * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def take(self, dmg):
        self.hp -= dmg
        return self.hp <= 0
