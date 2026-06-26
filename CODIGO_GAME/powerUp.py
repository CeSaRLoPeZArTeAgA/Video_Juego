import pygame
from utils import load_image

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, name, image_path, kind, x, y, vx=0, vy=120):
        super().__init__()
        self.name = name
        self.kind = kind
        self.image = load_image(image_path, (58,58))
        self.rect = self.image.get_rect(center=(x,y))
        self.vx = vx
        self.vy = vy
        self.dead = False

    def kill(self):
        """Marca el power-up como eliminado aunque esté guardado en una lista."""
        self.dead = True
        super().kill()

    def alive(self):
        return not self.dead

    def update(self, dt):
        if self.dead:
            return
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        if self.rect.top > 700 or self.rect.right < -80 or self.rect.left > 1040:
            self.kill()

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.image, self.rect)
