import random
import pygame
from config import WIDTH, HEIGHT
from utils import load_image

class BackgroundMoving:
    def __init__(self):
        self.image = None
        self.particles = []
        self.universe_id = None

    def set_universe(self, universe):
        self.universe_id = universe["id"]
        self.image = load_image(universe["background"], (WIDTH, HEIGHT))
        self.particles.clear()
        for _ in range(70):
            self.particles.append([
                random.randrange(0, WIDTH), random.randrange(0, HEIGHT),
                random.uniform(0.3, 2.2), random.choice([(255,220,90), (255,120,50), (160,220,255)])
            ])

    def draw(self, screen, dt):
        if self.image:
            screen.blit(self.image, (0, 12))
        for p in self.particles:
            p[1] += p[2] * (0.5 + 0.25 * self.universe_id) * dt * 60
            if p[1] > HEIGHT:
                p[0] = random.randrange(0, WIDTH)
                p[1] = -5
            pygame.draw.circle(screen, p[3], (int(p[0]), int(p[1])), 2)
