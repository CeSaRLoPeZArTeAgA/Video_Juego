import pygame
from bullet import Bullet

class BulletManager:
    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0.0

    def reset(self):
        self.bullets.empty()
        self.cooldown = 0.0

    def update(self, dt):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.bullets.update(dt)

    def spawn_bullet(self, x, y, direction="up"):
        if self.cooldown > 0:
            return False
        if direction == "right":
            bullet = Bullet(x + 48, y, vx=680, vy=0, kind="aji")
            self.cooldown = 0.24
        else:
            bullet = Bullet(x, y - 40, vx=0, vy=-650, kind="aji_laser")
            self.cooldown = 0.20
        self.bullets.add(bullet)
        return True

    def draw(self, screen):
        for b in self.bullets:
            b.draw(screen)

    def get_bullets(self):
        return self.bullets

    def increase_type(self):
        # Compatibilidad con el proyecto base Galaga.
        pass
