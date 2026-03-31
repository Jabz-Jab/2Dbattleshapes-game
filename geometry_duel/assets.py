# assets.py
import os
import pygame

from settings import WIDTH, HEIGHT
from utils import scale_cover 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_img(filename, size=None, fallback=None):
 
    path = os.path.join(ASSETS_DIR, filename)

    try:
        img = pygame.image.load(path)

        ext = os.path.splitext(filename)[1].lower()
        if ext in (".jpg", ".jpeg"):
            img = img.convert()
        else:
            img = img.convert_alpha()

        if size:
            img = pygame.transform.smoothscale(img, size)

        return img

    except Exception:
        # fallback surface
        w, h = size if size else (72, 72)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        if fallback:
            fallback(surf, w, h)
        else:
            pygame.draw.rect(surf, (200, 200, 200), (0, 0, w, h), border_radius=12)

        return surf

def fb_player(s, w, h):
    pygame.draw.circle(s, (90, 200, 255), (w // 2, h // 2), min(w, h) // 2 - 4)
    pygame.draw.circle(s, (255, 255, 255), (w // 2, h // 2), min(w, h) // 2 - 14, 3)

def fb_circle_boss(s, w, h):
    pygame.draw.circle(s, (255, 90, 90), (w // 2, h // 2), min(w, h) // 2 - 6)
    pygame.draw.circle(s, (0, 0, 0), (w // 2, h // 2), min(w, h) // 2 - 6, 3)

def fb_square_boss(s, w, h):
    pygame.draw.rect(s, (180, 120, 255), (6, 6, w - 12, h - 12), border_radius=14)
    pygame.draw.rect(s, (0, 0, 0), (6, 6, w - 12, h - 12), 3, border_radius=14)

def fb_triangle_boss(s, w, h):
    pygame.draw.polygon(s, (255, 220, 90), [(w // 2, 6), (w - 6, h - 6), (6, h - 6)])
    pygame.draw.polygon(s, (0, 0, 0), [(w // 2, 6), (w - 6, h - 6), (6, h - 6)], 3)

def fb_minion(s, w, h):
    pygame.draw.circle(s, (255, 170, 80), (w // 2, h // 2), min(w, h) // 2 - 6)
    pygame.draw.circle(s, (0, 0, 0), (w // 2, h // 2), min(w, h) // 2 - 6, 3)


def load_all():
    # Load background raw first (no forced size), then cover-scale it
    bg_raw = load_img("ba.jpg", size=None, fallback=lambda s, w, h: s.fill((18, 22, 35)))
    bg = scale_cover(bg_raw, WIDTH, HEIGHT) 

    player = load_img("player.png", (90, 90), fallback=fb_player)
    boss_c = load_img("boss_circle.png", (140, 140), fallback=fb_circle_boss)
    boss_s = load_img("boss_square.png", (150, 150), fallback=fb_square_boss)
    boss_t = load_img("boss_triangle.png", (160, 160), fallback=fb_triangle_boss)
    minion = load_img("minion.png", (54, 54), fallback=fb_minion)

    return bg, player, boss_c, boss_s, boss_t, minion
