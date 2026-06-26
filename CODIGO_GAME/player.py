import pygame
from pygame.locals import K_RIGHT, K_LEFT, K_UP, K_DOWN, K_a, K_d, K_w, K_s, K_SPACE
from config import WIDTH, HEIGHT
from utils import load_image, clamp
from bulletManager import BulletManager
from soundManager import SoundManager

class Player(pygame.sprite.Sprite):
    STATES = {
        "excited": "Player/excited.png",
        "angry": "Player/angry.png",
        "shock": "Player/shock.png",
        "laugh": "Player/laugh.png",
        "dizzy": "Player/dizzy.png",
        "cry": "Player/cry.png",
        "cool": "Player/cool.png",
        "victory": "Player/victory.png",
    }

    def __init__(self):
        super().__init__()
        self.images = {name: load_image(path) for name, path in self.STATES.items()}
        self.state = "excited"
        self.image = self._scaled_image(self.state)
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.copy()
        self.bullet_manager = BulletManager()
        self.lives = 5
        self.speed = 310
        self.x = WIDTH // 2
        self.y = HEIGHT - 120
        self.vy = 0
        self.on_ground = True
        self.jump_count = 0
        self.max_jumps = 2
        self.invuln = 0.0
        self.shield = 0.0
        self.turbo = 0.0
        self.ground_y = HEIGHT - 92
        self._jump_pressed = False
        self.sound = SoundManager.get()

    def _scaled_image(self, state):
        img = self.images.get(state, self.images["excited"])
        target_h = 116
        scale = target_h / img.get_height()
        return pygame.transform.smoothscale(img, (max(28, int(img.get_width()*scale)), target_h))

    def reset_for_universe(self, universe):
        self.state = universe.get("player_state", "excited")
        self.image = self._scaled_image(self.state)
        self.rect = self.image.get_rect()
        mech = universe["mechanic"]
        if mech == "runner":
            self.x = 150
            self.ground_y = HEIGHT - 80
            self.rect.midbottom = (self.x, self.ground_y)
            self.y = self.rect.y
            self.vy = 0
            self.on_ground = True
            self.jump_count = 0
            self.max_jumps = 2
            self._jump_pressed = False
        else:
            self.rect.center = (WIDTH // 2, HEIGHT - 110)
            self.x = self.rect.x
            self.y = self.rect.y
        self.bullet_manager.reset()
        self.invuln = 1.0
        self.shield = max(self.shield, 0.0)

    def update(self, dt, keys, mechanic):
        self.invuln = max(0, self.invuln - dt)
        self.shield = max(0, self.shield - dt)
        self.turbo = max(0, self.turbo - dt)
        speed = self.speed * (1.55 if self.turbo > 0 else 1.0)
        if mechanic == "runner":
            jump_now = bool(keys[K_SPACE] or keys[K_w] or keys[K_UP])
            if jump_now and not self._jump_pressed and self.jump_count < self.max_jumps:
                self.vy = -760 if self.jump_count == 0 else -690
                self.on_ground = False
                self.jump_count += 1
                self.sound.play_sfx('jump')
            self._jump_pressed = jump_now
            if keys[K_LEFT] or keys[K_a]:
                self.rect.x -= int(speed * 0.55 * dt)
            if keys[K_RIGHT] or keys[K_d]:
                self.rect.x += int(speed * 0.55 * dt)
            self.vy += 1800 * dt
            self.rect.y += int(self.vy * dt)
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.vy = 0
                self.on_ground = True
                self.jump_count = 0
            self.rect.x = clamp(self.rect.x, 40, WIDTH - self.rect.width - 60)
        else:
            dx = (keys[K_RIGHT] or keys[K_d]) - (keys[K_LEFT] or keys[K_a])
            dy = (keys[K_DOWN] or keys[K_s]) - (keys[K_UP] or keys[K_w])
            if dx and dy:
                dx *= 0.707
                dy *= 0.707
            self.rect.x += int(dx * speed * dt)
            self.rect.y += int(dy * speed * dt)
            self.rect.x = clamp(self.rect.x, 20, WIDTH - self.rect.width - 20)
            self.rect.y = clamp(self.rect.y, 120, HEIGHT - self.rect.height - 20)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.35, -self.rect.height * 0.20)
        self.bullet_manager.update(dt)

    def shoot(self, mechanic):
        if mechanic == "runner":
            shot = self.bullet_manager.spawn_bullet(self.rect.centerx, self.rect.centery, direction="right")
        else:
            shot = self.bullet_manager.spawn_bullet(self.rect.centerx, self.rect.top, direction="up")
        if shot:
            self.sound.play_sfx('shoot')
        return shot

    def hit(self):
        if self.invuln > 0:
            return False
        if self.shield > 0:
            self.shield = 0
            self.invuln = 0.8
            self.sound.play_sfx('hit')
            return False
        self.lives -= 1
        self.invuln = 1.4
        self.state = "dizzy" if self.lives > 1 else "cry"
        self.image = self._scaled_image(self.state)
        self.sound.play_sfx('hit')
        return True

    def heal(self):
        self.lives = min(6, self.lives + 1)

    def apply_power(self, kind):
        if kind == "shield":
            self.shield = 6.0
        elif kind == "turbo":
            self.turbo = 5.0
        elif kind == "heal":
            self.heal()
        self.sound.play_sfx('powerup')

    def is_alive(self):
        return self.lives > 0

    def get_lives(self):
        return self.lives

    def get_bullet_manager(self):
        return self.bullet_manager

    def draw(self, screen):
        if self.invuln > 0 and int(self.invuln * 12) % 2 == 0:
            return
        screen.blit(self.image, self.rect)
        if self.shield > 0:
            pygame.draw.ellipse(screen, (255, 255, 200), self.rect.inflate(25, 18), 3)
            pygame.draw.ellipse(screen, (255, 230, 80), self.rect.inflate(35, 28), 1)
