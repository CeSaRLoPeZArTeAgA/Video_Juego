import pygame
from config import WIDTH, HEIGHT, TITLE
from screenManager import ScreenManager
from soundManager import SoundManager


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    SoundManager.get()  # inicializa audio si esta disponible
    manager = ScreenManager(screen)
    manager.playGame()
    pygame.quit()

if __name__ == "__main__":
    main()
