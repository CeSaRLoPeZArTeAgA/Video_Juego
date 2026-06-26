import pygame
from config import WIDTH, HEIGHT, YELLOW, WHITE, ORANGE
from utils import load_image, draw_text
from universes import UNIVERSES
from soundManager import SoundManager

class ScreenMain:
    def __init__(self, screen):
        self.screen = screen
        self.bg = load_image("Backgrounds/menu_bg.png", (WIDTH, HEIGHT))
        self.logo = load_image("UI/logo.png", (700, 220))
        self.font = pygame.font.SysFont('arial', 22, bold=True)
        self.small = pygame.font.SysFont('arial', 17)
        self.title_font = pygame.font.SysFont('arial', 31, bold=True)
        self.big_font = pygame.font.SysFont('arial', 28, bold=True)
        self.clock = pygame.time.Clock()
        self.sound = SoundManager.get()
        self.sound.play_music('menu')

    def draw_panel(self, rect, fill=(0,0,0), border=(255,190,30), radius=18, alpha=215):
        surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(surf, (*fill, alpha), (0,0,rect[2],rect[3]), border_radius=radius)
        pygame.draw.rect(surf, border, (0,0,rect[2],rect[3]), 3, border_radius=radius)
        self.screen.blit(surf, rect[:2])

    def loop(self):
        blink = 0
        while True:
            dt = self.clock.tick(60) / 1000
            blink += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.sound.play_sfx('portal')
                        return "start"
                    if event.key == pygame.K_ESCAPE:
                        return "quit"

            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.logo, (WIDTH//2 - self.logo.get_width()//2, 24))
            draw_text(self.screen, "Ruta de universos", self.title_font, ORANGE, center=(WIDTH//2, 245), shadow=True)

            route_rect = (100, 270, WIDTH-200, 175)
            self.draw_panel(route_rect, fill=(8,8,18), alpha=150)
            y = route_rect[1] + 24
            for u in UNIVERSES:
                line = f"{u['id']}. {u['short']} - {u['goal']}"
                draw_text(self.screen, line, self.small, WHITE, center=(WIDTH//2, y), shadow=True, max_width=route_rect[2]-40)
                y += 34

            footer = (90, 500, WIDTH-180, 105)
            self.draw_panel(footer, fill=(0,0,0), alpha=225)
            if int(blink*2) % 2 == 0:
                draw_text(self.screen, "Pulsa ENTER para empezar la vuelta", self.big_font, (255,245,235), center=(WIDTH//2, 538), shadow=True)
            draw_text(self.screen, "Mover: Flechas o WASD   |   Accion: SPACE / J   |   Pausa: P   |   Salir: ESC", self.small, WHITE, center=(WIDTH//2, 582), shadow=True, max_width=footer[2]-28)

            pygame.display.flip()
