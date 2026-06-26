import random
import pygame
from utils import load_image
from config import WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, image_path, x, y, vx, vy, hp=1, points=10, size=(72,72), behavior="fall"):
        super().__init__()
        self.name = name
        self.base_image = load_image(image_path, size)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.hp = hp
        self.points = points
        self.behavior = behavior
        self.t = random.random() * 10
        self.hit_flash = 0.0
        self.dead = False

    def kill(self):
        """Marca el enemigo como eliminado aunque esté guardado en una lista normal.

        Importante: en este proyecto los enemigos NO están dentro de un
        pygame.sprite.Group, sino dentro de una lista de EnemySpawner. Por eso
        pygame.sprite.Sprite.alive() siempre devolvía False y los enemigos se
        borraban inmediatamente después de aparecer. Esta bandera corrige eso.
        """
        self.dead = True
        super().kill()

    def alive(self):
        return not self.dead

    def update(self, dt):
        if self.dead:
            return
        self.t += dt
        if self.behavior == "wave":
            wave = 90 * pygame.math.Vector2(1, 0).rotate(self.t * 80).x
            self.rect.x += int((self.vx + wave) * dt)
            self.rect.y += int(self.vy * dt)
        elif self.behavior == "runner":
            self.rect.x += int(self.vx * dt)
        elif self.behavior == "edge":
            self.rect.x += int(self.vx * dt)
            self.rect.y += int(self.vy * dt)
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.vx *= -1
            if self.rect.top < 110 or self.rect.bottom > HEIGHT:
                self.vy *= -1
        elif self.behavior == "boss":
            # Boss se actualiza en boss.py.
            pass
        else:
            self.rect.x += int(self.vx * dt)
            self.rect.y += int(self.vy * dt)
        self.hit_flash = max(0, self.hit_flash - dt)
        if self.rect.top > HEIGHT + 90 or self.rect.right < -140 or self.rect.left > WIDTH + 140:
            self.kill()

    def damage(self, amount=1):
        if self.dead:
            return False
        self.hp -= amount
        self.hit_flash = 0.10
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def draw(self, screen):
        if self.dead:
            return
        screen.blit(self.image, self.rect)
        if self.hit_flash > 0:
            pygame.draw.rect(screen, (255,255,255), self.rect, 3, border_radius=8)
