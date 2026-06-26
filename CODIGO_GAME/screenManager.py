from screenMain import ScreenMain
from screenGame import ScreenGame
from screenResult import ScreenResult

class ScreenManager:
    def __init__(self, screen):
        self.screen = screen

    def playGame(self):
        while True:
            main = ScreenMain(self.screen)
            action = main.loop()
            if action == "quit":
                return
            game = ScreenGame(self.screen)
            result = game.loop()
            if result.get("quit"):
                return
            result_screen = ScreenResult(self.screen)
            next_action = result_screen.loop(result)
            if next_action == "quit":
                return
