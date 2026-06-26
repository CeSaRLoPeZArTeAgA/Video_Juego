import pygame
from utils import load_image
from config import WIDTH, HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx=0, vy=-620, kind="aji_laser"):
        super().__init__()
        self.image = load_image("Bullets/aji_laser.png" if kind == "aji_laser" else "Bullets/aji.png", (42, 42))
        if vy < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.damage = 1

    def update(self, dt):
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        if self.rect.bottom < -20 or self.rect.top > HEIGHT + 20 or self.rect.right < -20 or self.rect.left > WIDTH + 20:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
