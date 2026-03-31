# game.py
import pygame
from settings import WIDTH, HEIGHT, FPS, MINION_CONTACT_DMG
from assets import load_all
from ui import draw_text, draw_player_panel, draw_boss_panel_top_right
from utils import dist2

from entities.player import Player
from bosses import CircleBoss, SquareBoss, TriangleBoss

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Battle Shapes")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.bg, player_img, boss_c, boss_s, boss_t, minion_img = load_all()
        self.player = Player(player_img)

        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.minions = pygame.sprite.Group()

        self.bosses = [
            CircleBoss(boss_c, minion_img),
            SquareBoss(boss_s, minion_img),
            TriangleBoss(boss_t, minion_img),
        ]
        self.boss_index = 0
        self.boss = self.bosses[self.boss_index]

        self.state = "menu"
        self.score = 0

    def start(self):
        self.state = "fight"
        self.score = 0

        self.player.hp = self.player.max_hp
        self.player.pos = pygame.Vector2(WIDTH // 2, int(HEIGHT * 0.75))
        self.player.invuln = 0
        self.player.last_dash = -999
        self.player.last_shot = -999
        self.player.dash_left = 0

        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.minions.empty()

        for b in self.bosses:
            b.reset()

        self.boss_index = 0
        self.boss = self.bosses[self.boss_index]

    def next_boss(self):
        self.boss_index += 1
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.minions.empty()

        if self.boss_index >= len(self.bosses):
            return False

        self.boss = self.bosses[self.boss_index]
        self.boss.reset()
        return True

    def handle_events(self, now):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "fight":
                        self.state = "pause"
                    elif self.state == "pause":
                        self.state = "fight"

                if self.state == "menu" and event.key == pygame.K_RETURN:
                    self.start()

                if self.state in ("gameover", "win") and event.key == pygame.K_RETURN:
                    self.state = "menu"

                if self.state == "fight":
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and self.player.can_dash(now):
                        self.player.do_dash(now)

            if self.state == "fight":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.player.can_shoot(now):
                        b = self.player.shoot(now, mouse_pos)
                        if b:
                            self.player_bullets.add(b)

        # hold-to-shoot
        if self.state == "fight" and keys[pygame.K_SPACE] and self.player.can_shoot(now):
            b = self.player.shoot(now, mouse_pos)
            if b:
                self.player_bullets.add(b)

        return True

    def update(self, dt, now):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        telegraphs = []

        if self.state == "fight":
            self.player.update(dt, keys, mouse_pos)

            self.player_bullets.update(dt)
            self.enemy_bullets.update(dt)

            for m in list(self.minions):
                m.update(dt, self.player.pos)

            # boss update
            if self.boss.__class__.__name__ == "CircleBoss":
                self.boss.update(dt, self.player, self.enemy_bullets, self.minions)
            elif self.boss.__class__.__name__ == "SquareBoss":
                self.boss.update(dt, self.player, self.enemy_bullets, self.minions, telegraphs)
            else:
                self.boss.update(dt, self.player, self.enemy_bullets, self.minions)

            # player bullets -> boss/minions
            for b in list(self.player_bullets):
                if dist2(b.pos, self.boss.pos) <= (self.boss.radius + b.radius) ** 2:
                    self.boss.damage(b.dmg)
                    b.kill()
                    self.score += 2
                    continue

                for m in list(self.minions):
                    if dist2(b.pos, m.pos) <= (m.radius + b.radius) ** 2:
                        if m.take(b.dmg):
                            m.kill()
                            self.score += 5
                        b.kill()
                        break

            # enemy bullets -> player
            for b in list(self.enemy_bullets):
                if dist2(b.pos, self.player.pos) <= (self.player.radius + b.radius) ** 2:
                    if self.player.invuln <= 0:
                        self.player.hp -= b.dmg
                        self.player.invuln = 0.35
                    b.kill()

            # minion touch
            for m in list(self.minions):
                if dist2(m.pos, self.player.pos) <= (m.radius + self.player.radius) ** 2:
                    if self.player.invuln <= 0:
                        self.player.hp -= MINION_CONTACT_DMG
                        self.player.invuln = 0.35

            if self.player.hp <= 0:
                self.state = "gameover"

            if self.boss.dead:
                self.score += 100
                if not self.next_boss():
                    self.state = "win"

        return telegraphs

    def draw(self, telegraphs):
        self.screen.blit(self.bg, (0, 0))

        if self.state in ("fight", "pause", "gameover", "win"):
            for tg in telegraphs:
                tg.draw(self.screen)

            self.player_bullets.draw(self.screen)
            self.enemy_bullets.draw(self.screen)
            self.minions.draw(self.screen)

            self.boss.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)

            draw_player_panel(self.screen, self.player.hp, self.player.max_hp, self.score)
            draw_boss_panel_top_right(self.screen, self.boss)

        if self.state == "menu":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "COMP GRAPHICS PROJECT", 92, WIDTH//2, 170, center=True)
            draw_text(self.screen, "Battle Shapes BSIT 4-B", 36, WIDTH//2, 240, (220,220,220), center=True)
            draw_text(self.screen, "Amparado, Marbane, Montero, Talaman", 36, WIDTH//2, 300, (220,220,220), center=True)
            draw_text(self.screen, "Press ENTER to start", 40, WIDTH//2, 420, center=True)

        if self.state == "pause":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "PAUSED", 90, WIDTH//2, HEIGHT//2 - 40, center=True)
            draw_text(self.screen, "Press ESC to resume", 34, WIDTH//2, HEIGHT//2 + 25, (230,230,230), center=True)

        if self.state == "gameover":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "GAME OVER", 96, WIDTH//2, HEIGHT//2 - 70, center=True)
            draw_text(self.screen, f"Score: {self.score}", 44, WIDTH//2, HEIGHT//2 - 10, center=True)
            draw_text(self.screen, "Press ENTER for menu", 34, WIDTH//2, HEIGHT//2 + 70, center=True)

        if self.state == "win":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "YOU WIN!", 96, WIDTH//2, HEIGHT//2 - 70, center=True)
            draw_text(self.screen, f"Final Score: {self.score}", 44, WIDTH//2, HEIGHT//2 - 10, center=True)
            draw_text(self.screen, "Press ENTER for menu", 34, WIDTH//2, HEIGHT//2 + 70, center=True)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.033)
            now = pygame.time.get_ticks() / 1000.0

            running = self.handle_events(now)
            telegraphs = self.update(dt, now)
            self.draw(telegraphs)

        pygame.quit()
