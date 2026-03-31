# utils.py
import pygame

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def dist2(a: pygame.Vector2, b: pygame.Vector2) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy

def scale_cover(img: pygame.Surface, target_w: int, target_h: int) -> pygame.Surface:
  
    if img is None:
        return pygame.Surface((target_w, target_h))

    iw, ih = img.get_size()
    if iw <= 0 or ih <= 0:
        return pygame.transform.smoothscale(img, (target_w, target_h))

    scale = max(target_w / iw, target_h / ih)
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))

    scaled = pygame.transform.smoothscale(img, (nw, nh))

    x = max(0, (nw - target_w) // 2)
    y = max(0, (nh - target_h) // 2)

    # subsurface then copy so the returned surface is independent
    return scaled.subsurface((x, y, target_w, target_h)).copy()

def scale_stretch(img: pygame.Surface, target_w: int, target_h: int) -> pygame.Surface:
  
    if img is None:
        return pygame.Surface((target_w, target_h))
    return pygame.transform.smoothscale(img, (target_w, target_h))
