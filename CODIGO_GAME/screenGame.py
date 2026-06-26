import random
import pygame
from pygame.locals import K_SPACE, K_j, K_p, K_ESCAPE
from config import WIDTH, HEIGHT, WHITE, YELLOW, ORANGE
from background import BackgroundMoving
from player import Player
from status import Status
from score import Score
from enemySpawner import EnemySpawner
from collisionDetector import CollisionDetector
from universes import UNIVERSES
from boss import Boss
from utils import load_image, draw_text
from soundManager import SoundManager

HUD_HEIGHT = 72

class ScreenGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bg = BackgroundMoving()
        self.player = Player()
        self.status = Status()
        self.score = Score()
        self.spawner = EnemySpawner()
        self.collision = CollisionDetector()
        self.portal_img = load_image("UI/portal.png", (190, 190))
        self.font_big = pygame.font.SysFont('arial', 34, bold=True)
        self.font = pygame.font.SysFont('arial', 22, bold=True)
        self.small = pygame.font.SysFont('arial', 16)
        self.total_score = 0
        self.universe_score = 0
        self.u_index = 0
        self.universe = None
        self.boss = None
        self.portal_timer = 0.0
        self.pause = False
        self.message = ""
        self.message_timer = 0.0
        self.sound = SoundManager.get()
        self.runner_help_timer = 0.0
        # Precarga real de bosses con el tamaño exacto usado en juego.
        # Esto evita microcongelamientos cuando entra el enemigo final.
        for u in UNIVERSES:
            try:
                _name, img, _hp, _pts = u['boss']
                mech = u.get('mechanic')
                size = (210, 175) if mech == 'collect' else (190, 140)
                load_image(img, size)
            except Exception:
                pass
        self.start_universe(0)

    def _music_for_universe(self, idx):
        return ['u1_space', 'u2_uni', 'u3_delivery', 'u4_office'][idx]

    def start_universe(self, idx):
        self.u_index = idx
        self.universe = UNIVERSES[idx]
        self.bg.set_universe(self.universe)
        self.player.reset_for_universe(self.universe)
        self.spawner.reset()
        self.universe_score = 0
        self.boss = None
        if self.universe["mechanic"] != "runner":
            for _ in range(4):
                self.spawner.spawn(self.universe, initial=True)
        else:
            for _ in range(2):
                self.spawner.spawn(self.universe, initial=True)
            self.runner_help_timer = 6.0
        self.portal_timer = 0.0
        self.message = self.universe["title"]
        self.message_timer = 1.4
        self.sound.play_music(self._music_for_universe(idx))

    def spawn_boss_if_needed(self):
        if self.boss is None and self.universe_score >= self.universe["boss_trigger"]:
            name, img, hp, points = self.universe["boss"]
            self.boss = Boss(name, img, hp, points, self.universe["mechanic"])
            self.message = f"JEFE: {name}"
            self.message_timer = 1.2
            self.spawner.enemies.clear()
            self.sound.play_sfx('boss')

    def clear_universe(self):
        self.portal_timer = 2.1
        self.message = self.universe["clear_phrase"]
        self.message_timer = 1.5
        self.sound.play_sfx('portal')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return "quit"
                if event.key == K_p:
                    self.pause = not self.pause
                if event.key in (K_j, K_SPACE):
                    if self.universe["mechanic"] != "runner" or event.key == K_j:
                        self.player.shoot(self.universe["mechanic"])
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mech = self.universe["mechanic"]
        if mech != "runner" and (keys[K_SPACE] or keys[K_j]):
            self.player.shoot(mech)
        if mech == "runner":
            if keys[K_j] or self.boss is not None:
                self.player.shoot(mech)
        self.player.update(dt, keys, mech)
        if mech == "runner" and self.boss is None:
            self.universe_score += int(60 * dt)
        self.player.get_bullet_manager().update(dt)
        self.spawn_boss_if_needed()
        self.spawner.update(dt, self.universe, boss_active=self.boss is not None)
        if self.boss:
            self.boss.update(dt)
            if random.random() < 0.012:
                self.spawner.spawn(self.universe)
        gained = self.collision.bullets_vs_enemies(self.player.get_bullet_manager().get_bullets(), self.spawner.enemies)
        if gained:
            self.total_score += gained
            self.sound.play_sfx('hit')
            if mech != "runner":
                self.universe_score += max(1, gained // 10)
        gained_power = self.collision.player_vs_powerups(self.player, self.spawner.powerups)
        if gained_power:
            self.total_score += gained_power * 25
            self.universe_score += gained_power
        self.collision.player_vs_enemies(self.player, self.spawner.enemies)
        if self.boss:
            gained_boss, defeated = self.collision.bullets_vs_boss(self.player.get_bullet_manager().get_bullets(), self.boss)
            if gained_boss:
                self.total_score += gained_boss
                self.sound.play_sfx('hit')
            if defeated:
                self.boss = None
                self.clear_universe()
        self.message_timer = max(0, self.message_timer - dt)
        self.runner_help_timer = max(0, self.runner_help_timer - dt)

    def _blit_overlay_rect(self, rect, fill=(0,0,0), alpha=145, border=None, radius=12):
        surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(surf, (*fill, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
        if border is not None:
            pygame.draw.rect(surf, border, (0, 0, rect[2], rect[3]), 2, border_radius=radius)
        self.screen.blit(surf, rect[:2])

    def draw_hud_cards(self):
        self._blit_overlay_rect((0, 0, WIDTH, HUD_HEIGHT), fill=(0,0,0), alpha=165)
        self.score.draw(self.screen, self.total_score, self.universe_score, self.universe["target"])
        self.status.draw(self.screen, self.player.get_lives(), self.universe["short"], self.boss, self.player.shield, self.player.turbo)
        # Se retira por completo la frase de objetivo superior que tapaba el fondo.
        if self.universe['mechanic'] == 'runner' and self.runner_help_timer > 0:
            self._blit_overlay_rect((18, HEIGHT - 48, 390, 30), fill=(0,0,0), alpha=135, border=(255,170,30), radius=10)
            draw_text(self.screen, 'SPACE salta | J dispara', self.small, ORANGE, center=(213, HEIGHT - 33), max_width=360)

    def draw(self, dt):
        self.bg.draw(self.screen, dt)
        self.spawner.draw(self.screen)
        if self.boss:
            self.boss.draw(self.screen)
        self.player.get_bullet_manager().draw(self.screen)
        self.player.draw(self.screen)
        self.draw_hud_cards()
        if self.message_timer > 0:
            rect = (120, 225, WIDTH - 240, 64)
            self._blit_overlay_rect(rect, fill=(0, 0, 0), alpha=78, border=None, radius=16)
            draw_text(self.screen, self.message, self.font_big, YELLOW, center=(WIDTH//2, rect[1] + rect[3]//2), max_width=rect[2] - 24)
        if self.portal_timer > 0:
            angle = int(pygame.time.get_ticks() * 0.18)
            portal = pygame.transform.rotate(self.portal_img, angle)
            self.screen.blit(portal, (WIDTH//2 - portal.get_width()//2, HEIGHT//2 - portal.get_height()//2))
        if self.pause:
            self._blit_overlay_rect((0, 0, WIDTH, HEIGHT), fill=(0,0,0), alpha=165)
            draw_text(self.screen, "PAUSA", self.font_big, YELLOW, center=(WIDTH//2, HEIGHT//2 - 20))
            draw_text(self.screen, "P para continuar", self.font, WHITE, center=(WIDTH//2, HEIGHT//2 + 35))

    def loop(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            action = self.handle_events()
            if action == "quit":
                return {"quit": True}
            if not self.pause and self.portal_timer <= 0:
                self.update(dt)
            elif self.portal_timer > 0:
                self.portal_timer -= dt
                if self.portal_timer <= 0:
                    if self.u_index + 1 < len(UNIVERSES):
                        self.start_universe(self.u_index + 1)
                    else:
                        return {"won": True, "score": self.total_score}
            self.draw(dt)
            if not self.player.is_alive():
                return {"won": False, "score": self.total_score, "phrase": self.universe["lose_phrase"], "universe": self.universe["short"]}
            pygame.display.flip()
