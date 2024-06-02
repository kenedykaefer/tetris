import pygame
import random
import numpy as np

class TetrisGame:
    # Colors
    COLOR_DARK = (20, 20, 20)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_WHITE = (255, 255, 255)

    # Screen
    SCREEN_SCALE = 1
    SCREEN_WIDTH = SCREEN_SCALE * 600
    SCREEN_HEIGHT = SCREEN_SCALE * 600
    SCREEN_FPS = 60

    # Grid
    NUM_ROWS = 20
    NUM_COLS = 10
    GRID_SIZE = 30 

    # Tetrominoes
    TETROMINOES = {
        1 : np.array([ # L
            [1, 0],
            [1, 0],
            [1, 1]
        ]),

        2 : np.array([ # J
            [0, 2],
            [0, 2],
            [2, 2]
        ]),

        3 : np.array([ # S
            [0, 3, 3],
            [3, 3, 0]
        ]),

        4 : np.array([ # Z
            [4, 4, 0],
            [0, 4, 4]
        ]),

        5 : np.array([ # I
            [5],
            [5],
            [5],
            [5]
        ]),

        6 : np.array([ # O
            [6, 6],
            [6, 6]
        ]),

        7 : np.array([ # T
            [7, 7, 7],
            [0, 7, 0]
        ])
      }
    
    TETROMINOES_COLORS = {
        0 : (0, 0, 0),
        1 : (0, 255, 0),
        2 : (0, 0, 255),
        3 : (255, 0, 0),
        4 : (255, 255, 0),
        5 : (0, 255, 255),
        6 : (255, 165, 0),
        7 : (128, 0, 128)
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = np.zeros((self.NUM_ROWS, self.NUM_COLS))

        self.next_tetromino = self.TETROMINOES[random.randint(1, 7)]
        num_rotations = random.randint(0, 3)
        for _ in range(num_rotations):
            self.next_tetromino = np.rot90(self.next_tetromino)
        self.current_tetromino = self.TETROMINOES[random.randint(1, 7)]
        self.x_current_tetromino = random.randint(0, self.NUM_COLS - self.current_tetromino.shape[1])
        self.y_current_tetromino = 0
        self.update_tetromines = False

        self.score = 0
        
        self.game_alive = True

    def run(self):

        MOVE_DOWN = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE_DOWN, 500)

        down_end = False

        while self.game_alive:
            self.screen.fill(self.COLOR_DARK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_alive = False
                # if event.type == MOVE_DOWN:
                #     self.update_y_current_tetromino()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.can_move_left():
                            self.x_current_tetromino -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.can_move_right():
                            self.x_current_tetromino += 1
                    if event.key == pygame.K_UP:
                        self.rotate_tetromino()
                    if event.key == pygame.K_DOWN:
                        self.update_y_current_tetromino()
                    if event.key == pygame.K_SPACE:
                        down_end = True

            if down_end:
                down_end = self.update_y_current_tetromino()

            self.draw_grid_with_tetromino()
            self.draw_next_tetromino_preview()
            self.draw_current_tetromino()

            self.check_full_row()
                  
            self.clock.tick(self.SCREEN_FPS)
            pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # write game over
            # self.screen.fill(self.COLOR_DARK)
            font = pygame.font.Font(None, 36)
            text = font.render('Game Over', True, self.COLOR_WHITE)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def can_move_right(self):
        for row in range(self.current_tetromino.shape[0]):
            col = self.current_tetromino.shape[1] - 1
            while self.current_tetromino[row][col] == 0:
                col -= 1
            if self.x_current_tetromino + col == self.NUM_COLS - 1 or self.grid[self.y_current_tetromino + row][self.x_current_tetromino + col + 1] != 0:
                return False
        return True
    
    def can_move_left(self):
        for row in range(self.current_tetromino.shape[0]):
            col = 0
            while self.current_tetromino[row][col] == 0:
                col += 1
            if self.x_current_tetromino + col == 0 or self.grid[self.y_current_tetromino + row][self.x_current_tetromino + col - 1] != 0:
                return False
        return True
            

    def check_full_row(self):
        for row in range(self.grid.shape[0]):
            if 0 not in self.grid[row]:
                self.grid = np.delete(self.grid, row, 0)
                self.grid = np.insert(self.grid, 0, np.zeros(self.grid.shape[1]), 0)
                self.score += 10

    def update_y_current_tetromino(self):
        if self.check_collision():
            self.add_tetromino_to_grid_and_update_current_tetromino()
            return False
        else:
            self.y_current_tetromino += 1
            return True

    def add_tetromino_to_grid_and_update_current_tetromino(self):
        self.add_tetromino_to_grid()
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self.TETROMINOES[random.randint(1, 7)]
        num_rotations = random.randint(0, 3)
        for _ in range(num_rotations):
            self.next_tetromino = np.rot90(self.next_tetromino)
        self.x_current_tetromino = random.randint(0, self.NUM_COLS - self.current_tetromino.shape[1])
        self.y_current_tetromino = 0
        self.check_game_over()

    def check_game_over(self):
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    if self.grid[row][self.x_current_tetromino + col] != 0:
                        self.game_alive = False

    def rotate_tetromino(self):
        new_x = self.x_current_tetromino
        rotated_tetromino = np.rot90(self.current_tetromino)
        while new_x + rotated_tetromino.shape[1] > self.NUM_COLS:
            new_x -= 1

        for row in range(rotated_tetromino.shape[0]):
            for col in range(rotated_tetromino.shape[1]):
                if rotated_tetromino[row][col] != 0:
                    if self.y_current_tetromino + row >= self.NUM_ROWS or self.grid[self.y_current_tetromino + row][new_x + col] != 0:
                        return
                    
        self.current_tetromino = rotated_tetromino
        self.x_current_tetromino = new_x                            
        

    def add_tetromino_to_grid(self):
        if self.y_current_tetromino < 0:
            self.game_alive = False
            return
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    self.grid[self.y_current_tetromino + row][self.x_current_tetromino + col] = self.current_tetromino[row][col]

    def draw_grid_with_tetromino(self):
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                pygame.draw.rect(self.screen, self.TETROMINOES_COLORS[int(self.grid[row][col])], (col * self.GRID_SIZE, row * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 0)
                
    def draw_next_tetromino_preview(self):
        x = self.SCREEN_WIDTH - (self.GRID_SIZE * self.NUM_COLS) // 2
        y = self.GRID_SIZE * self.NUM_ROWS // 3

        font = pygame.font.Font(None, 36)
        text = font.render('Next Tetromino', True, self.COLOR_WHITE)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

        x = self.SCREEN_WIDTH - (self.GRID_SIZE * self.NUM_COLS) // 2 - self.GRID_SIZE * self.next_tetromino.shape[1] // 2
        y += self.GRID_SIZE

        for row in range(self.next_tetromino.shape[0]):
            for col in range(self.next_tetromino.shape[1]):
                if self.next_tetromino[row][col] != 0:
                    pygame.draw.rect(self.screen, self.TETROMINOES_COLORS[int(self.next_tetromino[row][col])], (x + col * self.GRID_SIZE, y + row * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 0)

    def draw_current_tetromino(self):
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    if self.grid[self.y_current_tetromino + row][self.x_current_tetromino + col] != 0:
                        color = self.COLOR_WHITE
                    else:
                        color = self.TETROMINOES_COLORS[int(self.current_tetromino[row][col])]
                    pygame.draw.rect(self.screen, color , (self.x_current_tetromino * self.GRID_SIZE + col * self.GRID_SIZE, self.y_current_tetromino * self.GRID_SIZE + row * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 0)

    def check_collision(self):
        for row in range(self.current_tetromino.shape[0] - 1, -1, -1):
            if self.y_current_tetromino + row == self.NUM_ROWS - 1:
                return True
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    if self.grid[self.y_current_tetromino + row + 1][self.x_current_tetromino + col] != 0:
                        return True
        return False
    
def main():
    game = TetrisGame()
    game.run()

if __name__ == '__main__':
    main()