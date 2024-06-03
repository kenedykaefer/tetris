import pygame
import time

class TetrisUserInput:
    def __init__(self):
        pygame.init()
        self.last_input_time = time.time()
        self.input_delay = 0.15

    def get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'space'
                if event.key == pygame.K_UP:
                    return 'rotate'
                if event.key == pygame.K_LEFT:
                    self.last_input_time = time.time()
                    return 'left'
                if event.key == pygame.K_RIGHT:
                    self.last_input_time = time.time()
                    return 'right'
                if event.key == pygame.K_DOWN:
                    self.last_input_time = time.time()
                    return 'down'
                if event.key == pygame.K_n:
                    return 'new_game'
        
        if time.time() - self.last_input_time < self.input_delay:
            return None
        
        self.last_input_time = time.time()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return 'left'
        if keys[pygame.K_RIGHT]:
            return 'right'
        if keys[pygame.K_DOWN]:
            return 'down'
        return None
