import pygame
from config import WIDTH, HEIGHT, YELLOW, WHITE, ORANGE, RED
from utils import load_image, draw_text
from universes import FINAL_PHRASE
from soundManager import SoundManager

class ScreenResult:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bg = load_image("Backgrounds/menu_bg.png", (WIDTH, HEIGHT))
        self.victory_img = load_image("Player/victory.png")
        scale = 255 / self.victory_img.get_height()
        self.victory_img = pygame.transform.smoothscale(self.victory_img, (int(self.victory_img.get_width()*scale), 255))
        self.cry_img = load_image("Player/cry.png")
        scale2 = 235 / self.cry_img.get_height()
        self.cry_img = pygame.transform.smoothscale(self.cry_img, (int(self.cry_img.get_width()*scale2), 235))
        self.title_font = pygame.font.SysFont('arial', 44, bold=True)
        self.font = pygame.font.SysFont('arial', 26, bold=True)
        self.small = pygame.font.SysFont('arial', 20)
        self.tiny = pygame.font.SysFont('arial', 17)
        self.sound = SoundManager.get()

    def draw_panel(self, rect, fill=(0,0,0), border=(255,190,30), radius=18, alpha=220):
        surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(surf, (*fill, alpha), (0,0,rect[2],rect[3]), border_radius=radius)
        pygame.draw.rect(surf, border, (0,0,rect[2],rect[3]), 3, border_radius=radius)
        self.screen.blit(surf, rect[:2])

    def loop(self, result):
        if result.get("won"):
            self.sound.play_music('victory', loops=-1)
        else:
            self.sound.play_music('gameover', loops=-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.sound.play_sfx('portal')
                        return "restart"
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return "quit"

            self.screen.blit(self.bg, (0,0))

            if result.get("won"):
                draw_text(self.screen, "¡GANASTE EL MULTIVERSO!", self.title_font, YELLOW, center=(WIDTH//2, 88))
                self.screen.blit(self.victory_img, (WIDTH//2 - self.victory_img.get_width()//2, 135))

                phrase_box = (100, 418, WIDTH-200, 86)
                self.draw_panel(phrase_box, fill=(10,10,10), alpha=210)
                draw_text(self.screen, FINAL_PHRASE, self.font, WHITE, center=(WIDTH//2, 447), max_width=phrase_box[2]-34)
                draw_text(self.screen, "El pollo aventurero festeja: sobrevivio a todas las vueltas.", self.small, ORANGE, center=(WIDTH//2, 482), max_width=phrase_box[2]-40)
            else:
                draw_text(self.screen, "GAME OVER", self.title_font, RED, center=(WIDTH//2, 88))
                self.screen.blit(self.cry_img, (WIDTH//2 - self.cry_img.get_width()//2, 142))

                phrase_box = (130, 415, WIDTH-260, 92)
                self.draw_panel(phrase_box, fill=(20,0,0), border=(255,110,60), alpha=215)
                phrase = result.get("phrase", "La vida te dio otra vuelta.")
                draw_text(self.screen, "Frase de derrota", self.small, YELLOW, center=(WIDTH//2, 435))
                draw_text(self.screen, phrase, self.font, WHITE, center=(WIDTH//2, 468), max_width=phrase_box[2]-34)
                draw_text(self.screen, f"Caíste en: {result.get('universe','?')}", self.small, ORANGE, center=(WIDTH//2, 495), max_width=phrase_box[2]-34)

            footer = (155, 548, WIDTH-310, 55)
            self.draw_panel(footer, fill=(0,0,0), alpha=205)
            draw_text(self.screen, "R: reiniciar   |   ESC: salir", self.small, WHITE, center=(WIDTH//2, 575))

            pygame.display.flip()
            self.clock.tick(60)
