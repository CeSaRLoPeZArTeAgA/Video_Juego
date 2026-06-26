import pygame
from config import ASSET_DIR

_IMAGE_CACHE = {}


def asset_path(relative_path):
    return ASSET_DIR / relative_path


def _is_light_neutral(pixel):
    r, g, b, a = pixel
    if a == 0:
        return True
    return r >= 218 and g >= 218 and b >= 218 and (max(r, g, b) - min(r, g, b) <= 24)


def _remove_light_edge_background(surface):
    """Quita fondos blancos/grises tipo checkerboard pegados al borde.

    No modifica los archivos PNG originales: solo limpia la Surface cargada en memoria.
    Sirve para sprites exportados con falso fondo transparente, como algunas imágenes
    nuevas del usuario.
    """
    try:
        w, h = surface.get_size()
        if w == 0 or h == 0:
            return surface
        alpha = pygame.surfarray.pixels_alpha(surface)
        # Si ya tiene transparencia real, no se toca.
        if alpha.min() < 255:
            del alpha
            return surface
        del alpha

        # Si los bordes no parecen fondo claro, no se toca.
        samples = []
        step_x = max(1, w // 24)
        step_y = max(1, h // 24)
        for x in range(0, w, step_x):
            samples.append(surface.get_at((x, 0)))
            samples.append(surface.get_at((x, h - 1)))
        for y in range(0, h, step_y):
            samples.append(surface.get_at((0, y)))
            samples.append(surface.get_at((w - 1, y)))
        if sum(_is_light_neutral(px) for px in samples) < max(8, int(0.55 * len(samples))):
            return surface

        cleaned = surface.copy().convert_alpha()
        visited = set()
        stack = []
        for x in range(w):
            stack.append((x, 0))
            stack.append((x, h - 1))
        for y in range(h):
            stack.append((0, y))
            stack.append((w - 1, y))

        while stack:
            x, y = stack.pop()
            if (x, y) in visited or x < 0 or y < 0 or x >= w or y >= h:
                continue
            visited.add((x, y))
            if not _is_light_neutral(cleaned.get_at((x, y))):
                continue
            cleaned.set_at((x, y), (0, 0, 0, 0))
            stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
        return cleaned
    except Exception:
        return surface


def _scale_sprite_to_box(img, size):
    """Escala conservando proporción y centra en una caja transparente."""
    box_w, box_h = size
    if img.get_width() <= 0 or img.get_height() <= 0:
        return img
    scale = min(box_w / img.get_width(), box_h / img.get_height())
    new_w = max(1, int(img.get_width() * scale))
    new_h = max(1, int(img.get_height() * scale))
    scaled = pygame.transform.smoothscale(img, (new_w, new_h))
    canvas = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    canvas.blit(scaled, ((box_w - new_w) // 2, (box_h - new_h) // 2))
    return canvas


def load_image(relative_path, size=None, fallback_size=(64, 64), fallback_color=(255, 0, 255)):
    key = (str(relative_path), size)
    if key in _IMAGE_CACHE:
        return _IMAGE_CACHE[key]
    path = asset_path(relative_path)
    try:
        img = pygame.image.load(str(path)).convert_alpha()
        # Limpia en memoria fondos blancos/checkerboard falsos en sprites.
        if not str(relative_path).replace('\\', '/').startswith('Backgrounds/'):
            img = _remove_light_edge_background(img)
    except Exception:
        img = pygame.Surface(fallback_size, pygame.SRCALPHA)
        pygame.draw.rect(img, fallback_color, img.get_rect(), border_radius=8)
        pygame.draw.rect(img, (20, 20, 20), img.get_rect(), 2, border_radius=8)
    if size is not None:
        rel = str(relative_path).replace('\\', '/')
        if rel.startswith('Backgrounds/'):
            img = pygame.transform.smoothscale(img, size)
        else:
            img = _scale_sprite_to_box(img, size)
    _IMAGE_CACHE[key] = img
    return img


def draw_text(surface, text, font, color, center=None, topleft=None, shadow=True, max_width=None):
    lines = []
    if max_width:
        words = str(text).split()
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    else:
        lines = str(text).split("\n")
    rendered = [font.render(line, True, color) for line in lines]
    width = max((img.get_width() for img in rendered), default=0)
    height = sum(img.get_height() + 4 for img in rendered) - 4
    if center:
        x = center[0] - width // 2
        y = center[1] - height // 2
    elif topleft:
        x, y = topleft
    else:
        x, y = 0, 0
    for line, img in zip(lines, rendered):
        rx = x + (width - img.get_width()) // 2
        if shadow:
            sh = font.render(line, True, (0, 0, 0))
            surface.blit(sh, (rx + 2, y + 2))
        surface.blit(img, (rx, y))
        y += img.get_height() + 4


def clamp(v, lo, hi):
    return max(lo, min(hi, v))
