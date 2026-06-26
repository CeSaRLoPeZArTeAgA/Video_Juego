import pygame
from config import YELLOW, WHITE

class Score:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.big = pygame.font.SysFont('arial', 32, bold=True)

    def draw(self, screen, total_score, universe_score, target):
        text = self.font.render(f"Puntaje total: {total_score}", True, YELLOW)
        screen.blit(text, (18, 14))
        text2 = self.font.render(f"Progreso universo: {universe_score}/{target}", True, WHITE)
        screen.blit(text2, (18, 42))
