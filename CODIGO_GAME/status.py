import pygame
from config import WIDTH, RED, WHITE, YELLOW

class Status:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 18, bold=True)
        self.small = pygame.font.SysFont('arial', 15, bold=True)

    def draw(self, screen, lives, universe_name, boss=None, shield=0, turbo=0):
        life_text = self.font.render('Vidas: ' + str(lives), True, RED)
        screen.blit(life_text, (WIDTH - 120, 8))
        uni = self.font.render(universe_name, True, YELLOW)
        screen.blit(uni, (WIDTH//2 - uni.get_width()//2, 8))

        if shield > 0:
            s = self.small.render(f'Shield: {shield:0.1f}s', True, WHITE)
            screen.blit(s, (WIDTH - 195, 30))
        elif turbo > 0:
            t = self.small.render(f'Turbo: {turbo:0.1f}s', True, WHITE)
            screen.blit(t, (WIDTH - 185, 30))

        if boss:
            pygame.draw.rect(screen, (60,20,20), (250, 34, 460, 16), border_radius=6)
            max_hp = max(boss.max_hp, 1)
            w = int(456 * boss.hp / max_hp)
            pygame.draw.rect(screen, (255,80,40), (252, 36, w, 12), border_radius=6)
            label = self.small.render(boss.name, True, WHITE)
            screen.blit(label, (WIDTH//2 - label.get_width()//2, 52))
