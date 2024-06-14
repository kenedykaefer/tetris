import pygame
import time
from enum import Enum

class TetrisUserInput:
    class UserInput(Enum):
        QUIT = 0
        LEFT = 1
        RIGHT = 2
        DOWN = 3
        ROTATE = 4
        HARD_DROP = 5
        NEW_GAME = 6

    def __init__(self):
        self.input_delay = 0.15
        self._last_input_time = time.time()

    def get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.UserInput.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.UserInput.HARD_DROP
                if event.key == pygame.K_UP:
                    return self.UserInput.ROTATE
                if event.key == pygame.K_LEFT:
                    self._last_input_time = time.time()
                    return self.UserInput.LEFT
                if event.key == pygame.K_RIGHT:
                    self._last_input_time = time.time()
                    return self.UserInput.RIGHT
                if event.key == pygame.K_DOWN:
                    self._last_input_time = time.time()
                    return self.UserInput.DOWN
                if event.key == pygame.K_n:
                    return self.UserInput.NEW_GAME
        
        if time.time() - self._last_input_time < self.input_delay:
            return None
        
        self._last_input_time = time.time()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return self.UserInput.LEFT
        if keys[pygame.K_RIGHT]:
            return self.UserInput.RIGHT
        if keys[pygame.K_DOWN]:
            return self.UserInput.DOWN
        return None
