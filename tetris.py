import pygame
import random
import numpy as np


class GameConstants:
    # Colors
    COLOR_DARK = (20, 20, 20)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_WHITE = (255, 255, 255)

    # Screen
    SCREEN_SCALE = 1
    SCREEN_WIDTH = SCREEN_SCALE * 400
    SCREEN_HEIGHT = SCREEN_SCALE * 600
    SCREEN_FPS = 60

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()

    def run(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    
            self.screen.fill(GameConstants.COLOR_DARK)
            self.clock.tick(GameConstants.SCREEN_FPS)
            pygame.display.update()

def main():
    game = TetrisGame()
    game.run()

if __name__ == '__main__':
    main()