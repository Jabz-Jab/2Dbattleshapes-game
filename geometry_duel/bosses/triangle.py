# bosses/triangle.py
import math, random
import pygame
from bosses.base import BossBase
from entities.bullet import Bullet
from entities.minion import Minion
from settings import MINION_MAX_ON_SCREEN

class TriangleBoss(BossBase):
    def __init__(self, img, minion_img):
        super().__init__("TRIANGLE BOSS", img, hp=70)
        self.minion_img = minion_img
        self.t = 0.0
        self.shot_cd = 0.65
        self.child_cd = 2.3

    def reset(self):
        super().reset()
        self.t = 0.0
        self.shot_cd = 0.65
        self.child_cd = 2.3

    def update(self, dt, player, enemy_bullets, minions):
        self.t += dt
        self.pos.x = (1280 // 2) + math.sin(self.t * 0.8) * 260
        self.pos.y = (720 * 0.22) + math.cos(self.t * 1.1) * 22

        # simple 3-bullet spread
        self.shot_cd -= dt
        if self.shot_cd <= 0:
            self.shot_cd = 0.65
            v = player.pos - self.pos
            if v.length_squared() > 0:
                base = math.atan2(v.y, v.x)
                for deg in (-12, 0, 12):
                    a = base + math.radians(deg)
                    d = pygame.Vector2(math.cos(a), math.sin(a))
                    enemy_bullets.add(Bullet(self.pos, d * 360, owner="enemy", dmg=1))

        # children
        self.child_cd -= dt
        if self.child_cd <= 0 and len(minions) < MINION_MAX_ON_SCREEN:
            self.child_cd = 2.3
            spawn = self.pos + pygame.Vector2(random.uniform(-90, 90), random.uniform(50, 110))
            minions.add(Minion(spawn, self.minion_img))

        # face player
        v = player.pos - self.pos
        if v.length_squared() > 0:
            ang = math.degrees(math.atan2(-v.y, v.x))
            self.image = pygame.transform.rotozoom(self.base, ang, 1.0)
        else:
            self.image = self.base

        self.sync()
