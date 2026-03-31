# ui.py
import pygame
from settings import WIDTH, WHITE

def draw_text(screen, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.center = (x, y) if center else rect.move(x, y).topleft
    if not center:
        rect.topleft = (x, y)
    screen.blit(img, rect)
    return rect

def draw_player_panel(screen, hp, max_hp, score):
    pygame.draw.rect(screen, (0, 0, 0), (12, 12, 320, 76), border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), (12, 12, 320, 76), 2, border_radius=12)

    bar_x, bar_y = 26, 26
    bar_w, bar_h = 190, 14
    pygame.draw.rect(screen, (45, 45, 45), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
    fill = int(bar_w * (max(0, hp) / max_hp))
    pygame.draw.rect(screen, (90, 255, 140), (bar_x, bar_y, fill, bar_h), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=8)

    draw_text(screen, f"HP: {int(max(0, hp))}/{max_hp}", 22, 230, 21)
    draw_text(screen, f"Score: {score}", 22, 26, 48, (240, 240, 240))

def draw_boss_panel_top_right(screen, boss):
    panel_w, panel_h = 420, 76
    x = WIDTH - panel_w - 12
    y = 12

    pygame.draw.rect(screen, (0, 0, 0), (x, y, panel_w, panel_h), border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, panel_w, panel_h), 2, border_radius=12)

    draw_text(screen, boss.name, 26, x + 14, y + 10)

    bbx, bby = x + 14, y + 42
    bbw, bbh = panel_w - 28, 12
    pygame.draw.rect(screen, (45, 45, 45), (bbx, bby, bbw, bbh), border_radius=8)
    fill = int(bbw * (boss.hp / boss.max_hp))
    pygame.draw.rect(screen, (255, 120, 120), (bbx, bby, fill, bbh), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), (bbx, bby, bbw, bbh), 2, border_radius=8)
