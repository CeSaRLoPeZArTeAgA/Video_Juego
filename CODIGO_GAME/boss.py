import math
from enemy import Enemy
from config import WIDTH, HEIGHT

class Boss(Enemy):
    def __init__(self, name, image_path, hp, points, mechanic):
        size = (190, 140)
        x, y = WIDTH // 2, 100
        if mechanic == "collect":
            size = (210, 175)
            x, y = WIDTH // 2, 106
        elif mechanic == "runner":
            x, y = WIDTH - 160, HEIGHT - 135
        super().__init__(name, image_path, x, y, 120, 0, hp=hp, points=points, size=size, behavior="boss")
        self.max_hp = hp
        self.mechanic = mechanic
        self.shoot_timer = 1.5

    def update(self, dt):
        self.t += dt
        if self.mechanic == "runner":
            self.rect.y = int(HEIGHT - 170 + 20 * math.sin(self.t * 2.4))
            self.rect.x = int(WIDTH - 210 + 20 * math.sin(self.t * 1.2))
        else:
            self.rect.x += int(self.vx * dt)
            if self.rect.left < 60 or self.rect.right > WIDTH - 60:
                self.vx *= -1
            self.rect.y = int(96 + 22 * math.sin(self.t * 2.0))
        self.hit_flash = max(0, self.hit_flash - dt)
