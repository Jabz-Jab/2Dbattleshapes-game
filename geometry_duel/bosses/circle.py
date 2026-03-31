# bosses/circle.py
import math, random
import pygame
from bosses.base import BossBase
from entities.bullet import Bullet
from entities.minion import Minion
from settings import ENEMY_BULLET_SPEED, ENEMY_BULLET_DMG, MINION_MAX_ON_SCREEN

class CircleBoss(BossBase):
    def __init__(self, img, minion_img):
        super().__init__("CIRCLE BOSS", img, hp=45)  # ✅ shorter boss life
        self.minion_img = minion_img
        self.t = 0.0
        self.shot_cd = 0.45
        self.child_cd = 2.6

    def reset(self):
        super().reset()
        self.t = 0.0
        self.shot_cd = 0.45
        self.child_cd = 2.6

    def update(self, dt, player, enemy_bullets, minions):
        self.t += dt
        self.pos.x = pygame.Vector2().x + (1280 // 2) + math.sin(self.t * 0.9) * 220
        self.pos.y = (720 * 0.22) + math.cos(self.t * 1.1) * 30

        self.shot_cd -= dt
        if self.shot_cd <= 0:
            self.shot_cd = 0.45
            v = player.pos - self.pos
            if v.length_squared() > 0:
                d = v.normalize()
                enemy_bullets.add(Bullet(self.pos, d * ENEMY_BULLET_SPEED, owner="enemy", dmg=ENEMY_BULLET_DMG))

        self.child_cd -= dt
        if self.child_cd <= 0 and len(minions) < MINION_MAX_ON_SCREEN:
            self.child_cd = 2.6
            spawn = self.pos + pygame.Vector2(random.uniform(-80, 80), random.uniform(40, 90))
            minions.add(Minion(spawn, self.minion_img))

        self.image = self.base
        self.sync()
