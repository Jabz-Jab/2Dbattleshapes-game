# entities/player.py
import math
import pygame
from settings import (
    PLAYER_SPEED, DASH_SPEED, DASH_TIME, DASH_COOLDOWN,
    PLAYER_MAX_HP, PLAYER_BULLET_SPEED, PLAYER_BULLET_COOLDOWN,
    WIDTH, HEIGHT
)
from utils import clamp
from entities.bullet import Bullet

SPRITE_ANGLE_OFFSET = -90

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.base = img
        self.image = img
        self.rect = self.image.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.75)))
        self.pos = pygame.Vector2(self.rect.center)
        self.radius = max(self.rect.width, self.rect.height) * 0.35

        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp

        self.last_shot = -999.0
        self.last_dash = -999.0
        self.dash_left = 0.0
        self.invuln = 0.0

    def can_shoot(self, now): return (now - self.last_shot) >= PLAYER_BULLET_COOLDOWN
    def can_dash(self, now):  return (now - self.last_dash) >= DASH_COOLDOWN

    def do_dash(self, now):
        self.last_dash = now
        self.dash_left = DASH_TIME
        self.invuln = max(self.invuln, DASH_TIME + 0.08)

    def update(self, dt, keys, mouse_pos):
        if self.invuln > 0:
            self.invuln -= dt

        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]: move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move.x += 1
        if move.length_squared() > 0:
            move = move.normalize()

        speed = DASH_SPEED if self.dash_left > 0 else PLAYER_SPEED
        if self.dash_left > 0:
            self.dash_left -= dt

        self.pos += move * speed * dt

        aim = pygame.Vector2(mouse_pos) - self.pos
        if aim.length_squared() > 0:
            ang = math.degrees(math.atan2(-aim.y, aim.x)) + SPRITE_ANGLE_OFFSET
            self.image = pygame.transform.rotozoom(self.base, ang, 1.0)
        else:
            self.image = self.base

        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.radius = max(self.rect.width, self.rect.height) * 0.35

        pad_x, pad_y = self.rect.width // 2, self.rect.height // 2
        self.pos.x = clamp(self.pos.x, pad_x, WIDTH - pad_x)
        self.pos.y = clamp(self.pos.y, pad_y, HEIGHT - pad_y)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def shoot(self, now, mouse_pos):
        aim = pygame.Vector2(mouse_pos) - self.pos
        if aim.length_squared() == 0:
            return None
        d = aim.normalize()
        self.last_shot = now

        spawn = self.pos + d * (self.radius + 12)
        return Bullet(spawn, d * PLAYER_BULLET_SPEED, owner="player", dmg=1)
