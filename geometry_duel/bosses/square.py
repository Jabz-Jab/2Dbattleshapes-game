# bosses/square.py
import math, random
import pygame
from bosses.base import BossBase
from entities.bullet import Bullet
from entities.minion import Minion
from settings import SLAM_DMG, ENEMY_BULLET_DMG, MINION_MAX_ON_SCREEN

class TelegraphCircle:
    def __init__(self, pos, radius, time_left):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.t = time_left

    def update(self, dt): self.t -= dt

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(overlay, (255, 80, 80, 90), (int(self.pos.x), int(self.pos.y)), int(self.radius))
        pygame.draw.circle(overlay, (255, 80, 80, 190), (int(self.pos.x), int(self.pos.y)), int(self.radius), 3)
        screen.blit(overlay, (0, 0))

class SquareBoss(BossBase):
    def __init__(self, img, minion_img):
        super().__init__("SQUARE BOSS", img, hp=60)
        self.minion_img = minion_img
        self.t = 0.0
        self.shot_cd = 1.05

        self.slam_cd = 3.0
        self.slam_warn = None
        self.slam_target = None

        self.child_cd = 1.9

    def reset(self):
        super().reset()
        self.t = 0.0
        self.shot_cd = 1.05
        self.slam_cd = 3.0
        self.slam_warn = None
        self.slam_target = None
        self.child_cd = 1.9

    def update(self, dt, player, enemy_bullets, minions, telegraphs):
        self.t += dt
        self.pos.x = (1280 // 2) + math.sin(self.t * 0.6) * 180
        self.pos.y = (720 * 0.25) + math.cos(self.t * 0.8) * 18

        # 4-way bullets
        self.shot_cd -= dt
        if self.shot_cd <= 0:
            self.shot_cd = 1.05
            dirs = [pygame.Vector2(1,0), pygame.Vector2(-1,0), pygame.Vector2(0,1), pygame.Vector2(0,-1)]
            for d in dirs:
                enemy_bullets.add(Bullet(self.pos, d * 300, owner="enemy", dmg=ENEMY_BULLET_DMG))

        # Slam telegraph
        self.slam_cd -= dt
        if self.slam_warn:
            self.slam_warn.update(dt)
            telegraphs.append(self.slam_warn)
            if self.slam_warn.t <= 0:
                # impact
                if (player.pos - self.slam_target).length_squared() <= (self.slam_warn.radius ** 2):
                    if player.invuln <= 0:
                        player.hp -= SLAM_DMG
                        player.invuln = 0.35

                # small shock bullets
                for i in range(6):
                    a = (i / 6) * (2 * math.pi)
                    d = pygame.Vector2(math.cos(a), math.sin(a))
                    enemy_bullets.add(Bullet(self.slam_target, d * 280, owner="enemy", dmg=1))

                self.slam_warn = None
                self.slam_cd = 3.0
        else:
            if self.slam_cd <= 0:
                self.slam_target = pygame.Vector2(player.pos)
                self.slam_warn = TelegraphCircle(self.slam_target, 110, 0.95)
                telegraphs.append(self.slam_warn)

        # children
        self.child_cd -= dt
        if self.child_cd <= 0 and len(minions) < MINION_MAX_ON_SCREEN:
            self.child_cd = 1.9
            spawn = self.pos + pygame.Vector2(random.uniform(-90, 90), random.uniform(50, 110))
            minions.add(Minion(spawn, self.minion_img))

        self.image = self.base
        self.sync()
