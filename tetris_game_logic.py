import numpy as np
import random

class TetrisGameLogic:
    # Grid
    NUM_ROWS = 20
    NUM_COLS = 10

    # Tetrominoes
    TETROMINOES = [
        np.array([ # L
            [1, 0],
            [1, 0],
            [1, 1]
        ], np.uint8),
        np.array([ # J
            [0, 2],
            [0, 2],
            [2, 2]
        ], np.uint8),
        np.array([ # O
            [3, 3],
            [3, 3]
        ], np.uint8),
        np.array([ # S
            [0, 4, 4],
            [4, 4, 0]
        ], np.uint8),
        np.array([ # Z
            [5, 5, 0],
            [0, 5, 5]
        ], np.uint8),
        np.array([ # T
            [6, 6, 6],
            [0, 6, 0]
        ], dtype=np.uint8),
        np.array([ # I
            [7],
            [7],
            [7],
            [7]
        ], dtype=np.uint8)
    ]

    def __init__(self):
        self.grid = np.zeros((self.NUM_ROWS, self.NUM_COLS), np.uint8)
        self.next_tetromino = self._get_random_tetromino()
        self.current_tetromino = self._get_random_tetromino()
        self.current_tetromino_row = 0
        self.current_tetromino_col = random.randint(0, self.NUM_COLS - self.current_tetromino.shape[1])
        self.score = 0
        self.game_over = False

    def get_state(self):
        next_tetromino = np.zeros((4, 4))
        next_tetromino[:self.next_tetromino.shape[0], :self.next_tetromino.shape[1]] = self.next_tetromino
        state = {
            'grid': self.grid,
            'current_tetromino': self.current_tetromino,
            'current_tetromino_row': self.current_tetromino_row,
            'current_tetromino_col': self.current_tetromino_col,
            'next_tetromino': self.next_tetromino,
            'score': self.score,
            'game_over': self.game_over
        }
        return state
    
    def get_grid_shape(self):
        return self.grid.shape

    def move_tetromino_down(self):
        if self._check_collision():
            self._add_tetromino_to_grid()
            self._check_full_rows()
            self._spawn_new_tetromino()
            self._check_game_over()
            return False
        else:
            self.current_tetromino_row += 1
            return True
        
    def move_tetromino_left(self):
        for row in range(self.current_tetromino.shape[0]):
            col = 0
            while self.current_tetromino[row][col] == 0:
                col += 1
            if self.current_tetromino_col + col == 0 or self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col - 1] != 0:
                return
        self.current_tetromino_col -= 1

    def move_tetromino_right(self):
        for row in range(self.current_tetromino.shape[0]):
            col = self.current_tetromino.shape[1] - 1
            while self.current_tetromino[row][col] == 0:
                col -= 1
            if self.current_tetromino_col + col == self.NUM_COLS - 1 or self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col + 1] != 0:
                return
        self.current_tetromino_col += 1

    def rotate_tetromino(self):
        rotated_tetromino = np.rot90(self.current_tetromino)
        new_col = self.current_tetromino_col
        while new_col + rotated_tetromino.shape[1] > self.NUM_COLS:
            new_col -= 1

        if self.current_tetromino_row + rotated_tetromino.shape[0] >= self.NUM_ROWS:
            return

        for row in range(rotated_tetromino.shape[0]):
            for col in range(rotated_tetromino.shape[1]):
                if rotated_tetromino[row][col] != 0:
                    if self.grid[self.current_tetromino_row + row][new_col + col] != 0:
                        return
                    
        self.current_tetromino = rotated_tetromino
        self.current_tetromino_col = new_col

    def _check_full_rows(self):
        num_full_rows = 0
        for row in range(self.grid.shape[0]):
            if 0 not in self.grid[row]:
                num_full_rows += 1
                self.grid = np.delete(self.grid, row, axis=0)
                self.grid = np.insert(self.grid, 0, np.zeros(self.NUM_COLS), axis=0)
        self.score += self.NUM_COLS * (num_full_rows ** 2)

    def _add_tetromino_to_grid(self):
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col] = self.current_tetromino[row][col]
        
    def _check_collision(self):
        for row in range(self.current_tetromino.shape[0] - 1, -1, -1):
            if self.current_tetromino_row + row == self.NUM_ROWS - 1:
                return True
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    if self.grid[self.current_tetromino_row + row + 1][self.current_tetromino_col + col] != 0:
                        return True
        return False
    
    def _check_game_over(self):
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    if self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col] != 0:
                        self.game_over = True
            
    def _spawn_new_tetromino(self): # Spawn a new tetromino at the top of the grid
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self._get_random_tetromino()
        self.current_tetromino_row = 0
        self.current_tetromino_col = random.randint(0, self.NUM_COLS - self.current_tetromino.shape[1])

    def _get_random_tetromino(self): # Randomly select a tetromino and rotate it randomly
        tetromino = random.choice(self.TETROMINOES)
        num_rotations = random.randint(0, 3)
        for _ in range(num_rotations):
            tetromino = np.rot90(tetromino)
        return tetromino
    
