import random
from enemy import Enemy
from powerUp import PowerUp
from config import WIDTH, HEIGHT

class EnemySpawner:
    def __init__(self):
        self.enemies = []
        self.powerups = []
        self.spawn_timer = 0.0
        self.power_timer = 0.0

    def reset(self):
        self.enemies.clear()
        self.powerups.clear()
        self.spawn_timer = 0.0
        self.power_timer = 0.0

    def get_enemies(self):
        return self.enemies

    def spawn(self, universe, initial=False):
        name, img, hp, points = random.choice(universe["enemies"])
        mech = universe["mechanic"]
        if mech == "runner":
            x = WIDTH + (100 if initial else 60)
            # runner,  hueco siempre abajo; otros pueden venir algo altos.
            if "Hueco" in name:
                y = HEIGHT - 52
                size = (120, 50)
            elif "Moto" in name:
                y = HEIGHT - 92
                size = (110, 76)
            elif "Cliente" in name:
                y = random.choice([HEIGHT-96, HEIGHT-148])
                size = (86, 86)
            else:
                y = random.choice([HEIGHT-88, HEIGHT-138])
                size = (82, 70)
            vx = random.randint(-320, -230)
            vy = 0
            behavior = "runner"
        elif mech == "office":
            side = random.choice(["top","left","right"])
            if side == "top":
                x, y = random.randint(60, WIDTH-60), 90
                vx, vy = random.randint(-80,80), random.randint(90,160)
            elif side == "left":
                x, y = -40, random.randint(140, HEIGHT-80)
                vx, vy = random.randint(120,220), random.randint(-60,60)
            else:
                x, y = WIDTH+40, random.randint(140, HEIGHT-80)
                vx, vy = random.randint(-220,-120), random.randint(-60,60)
            size = (72,62)
            behavior = "fall"
        else:
            x = random.randint(80, WIDTH-80)
            y = random.randint(125, 210) if initial else -35
            vx = random.randint(-70, 70)
            vy = random.randint(120, 205)
            size = (76,76)
            behavior = "wave" if random.random() < 0.40 else "fall"
        enemy = Enemy(name, img, x, y, vx, vy, hp=hp, points=points, size=size, behavior=behavior)
        self.enemies.append(enemy)

    def spawn_powerup(self, universe):
        mech = universe["mechanic"]
        if "collectible" in universe and random.random() < 0.78:
            name, img, value, kind = universe["collectible"]
            p = PowerUp(name, img, "score", random.randint(70, WIDTH-70), -40, vy=120)
        elif "powerups" in universe:
            name, img, kind = random.choice(universe["powerups"])
            if mech == "runner":
                p = PowerUp(name, img, kind, WIDTH + 60, random.choice([HEIGHT-150, HEIGHT-205]), vx=-230, vy=0)
            else:
                p = PowerUp(name, img, kind, random.randint(70, WIDTH-70), -40, vy=105)
        else:
            return
        self.powerups.append(p)

    def update(self, dt, universe, boss_active=False):
        rate = universe.get("enemy_rate", 1.0)
        self.spawn_timer -= dt
        self.power_timer -= dt
        if self.spawn_timer <= 0 and not boss_active:
            self.spawn(universe)
            self.spawn_timer = max(0.50, rate + random.uniform(-0.15, 0.35))
        if self.power_timer <= 0:
            self.spawn_powerup(universe)
            self.power_timer = random.uniform(2.6, 4.6) if universe["mechanic"] == 'runner' else random.uniform(3.2, 5.7)
        for e in list(self.enemies):
            e.update(dt)
            if not e.alive():
                if e in self.enemies:
                    self.enemies.remove(e)
        for p in list(self.powerups):
            p.update(dt)
            if not p.alive():
                if p in self.powerups:
                    self.powerups.remove(p)

    def draw(self, screen):
        for p in self.powerups:
            p.draw(screen)
        for e in self.enemies:
            e.draw(screen)
