import pygame
from config import WIDTH, RED, WHITE, YELLOW

class Status:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 24, bold=True)

    def draw(self, screen, lives, universe_name, boss=None, shield=0, turbo=0):
        life_text = self.font.render('Vidas: ' + str(lives), True, RED)
        screen.blit(life_text, (WIDTH - 135, 14))
        uni = self.font.render(universe_name, True, YELLOW)
        screen.blit(uni, (WIDTH//2 - uni.get_width()//2, 14))
        y = 46
        if shield > 0:
            s = self.font.render(f'Mayonesa Shield: {shield:0.1f}s', True, WHITE)
            screen.blit(s, (WIDTH - 275, y)); y += 26
        if turbo > 0:
            t = self.font.render(f'Aji Turbo: {turbo:0.1f}s', True, WHITE)
            screen.blit(t, (WIDTH - 275, y))
        if boss:
            pygame.draw.rect(screen, (60,20,20), (260, 55, 440, 22), border_radius=8)
            max_hp = max(boss.max_hp, 1)
            w = int(436 * boss.hp / max_hp)
            pygame.draw.rect(screen, (255,80,40), (262, 57, w, 18), border_radius=8)
            label = self.font.render(boss.name, True, WHITE)
            screen.blit(label, (WIDTH//2 - label.get_width()//2, 82))
