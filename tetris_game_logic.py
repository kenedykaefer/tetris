import numpy as np
import random
import time

class TetrisGameLogic:
    # Grid
    _NUM_ROWS = 20
    _NUM_COLS = 10

    # Tetrominoes
    _TETROMINOES = [
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
        self.new_game()        
        
    def new_game(self):
        self.score = 0
        self.game_over = False
        self._grid = np.zeros((self._NUM_ROWS, self._NUM_COLS), np.uint8)
        self._next_tetromino = self._get_random_tetromino()
        self._current_tetromino = self._get_random_tetromino()
        self._current_tetromino_row = 0
        self._current_tetromino_col = random.randint(0, self._NUM_COLS - self._current_tetromino.shape[1])
        self._old_time = time.time()
        
    def get_state(self):
        self._update()
        next_tetromino = np.zeros((4, 4))
        next_tetromino[:self._next_tetromino.shape[0], :self._next_tetromino.shape[1]] = self._next_tetromino
        state = {
            'grid': self._grid,
            'current_tetromino': self._current_tetromino,
            'current_tetromino_row': self._current_tetromino_row,
            'current_tetromino_col': self._current_tetromino_col,
            'next_tetromino': self._next_tetromino,
            'score': self.score,
            'game_over': self.game_over
        }
        return state
    
    def get_grid_shape(self):
        return self._grid.shape
        
    def move_tetromino_left(self):
        if self.game_over:
            return
        self._update()
        for row in range(self._current_tetromino.shape[0]):
            col = 0
            while self._current_tetromino[row][col] == 0:
                col += 1
            if self._current_tetromino_col + col == 0 or self._grid[self._current_tetromino_row + row][self._current_tetromino_col + col - 1] != 0:
                return
        self._current_tetromino_col -= 1

    def move_tetromino_right(self):
        if self.game_over:
            return
        self._update()
        for row in range(self._current_tetromino.shape[0]):
            col = self._current_tetromino.shape[1] - 1
            while self._current_tetromino[row][col] == 0:
                col -= 1
            if self._current_tetromino_col + col == self._NUM_COLS - 1 or self._grid[self._current_tetromino_row + row][self._current_tetromino_col + col + 1] != 0:
                return
        self._current_tetromino_col += 1

    def move_tetromino_down(self):
        if self.game_over:
            return
        self._update()
        self._move_down()
        self._old_time = time.time()
        
    def move_tetromino_hard_drop(self):
        if self.game_over:
            return
        self._update()
        while self._move_down():
            pass
        self._old_time = time.time()

    def rotate_tetromino(self):
        if self.game_over:
            return
        self._update()
        rotated_tetromino = np.rot90(self._current_tetromino)
        new_col = self._current_tetromino_col
        while new_col + rotated_tetromino.shape[1] > self._NUM_COLS:
            new_col -= 1

        if self._current_tetromino_row + rotated_tetromino.shape[0] > self._NUM_ROWS:
            return

        for row in range(rotated_tetromino.shape[0]):
            for col in range(rotated_tetromino.shape[1]):
                if rotated_tetromino[row][col] != 0:
                    if self._grid[self._current_tetromino_row + row][new_col + col] != 0:
                        return
                    
        self._current_tetromino = rotated_tetromino
        self._current_tetromino_col = new_col

    def _update(self):
        if self.game_over:
            return
        time_elapsed = time.time() - self._old_time
        if time_elapsed >= 1:
            while time_elapsed >= 1:
                time_elapsed -= 1
                self._move_down()
            self._old_time = time.time()

    def _move_down(self):
        if self._check_collision():
            self._add_tetromino_to_grid()
            self._check_full_rows()
            self._spawn_new_tetromino()
            self._check_game_over()
            return False
        else:
            self._current_tetromino_row += 1
            return True

    def _check_full_rows(self):
        num_full_rows = 0
        for row in range(self._grid.shape[0]):
            if 0 not in self._grid[row]:
                num_full_rows += 1
                self._grid = np.delete(self._grid, row, axis=0)
                self._grid = np.insert(self._grid, 0, np.zeros(self._NUM_COLS), axis=0)
        self.score += self._NUM_COLS * (num_full_rows ** 2)

    def _add_tetromino_to_grid(self):
        for row in range(self._current_tetromino.shape[0]):
            for col in range(self._current_tetromino.shape[1]):
                if self._current_tetromino[row][col] != 0:
                    self._grid[self._current_tetromino_row + row][self._current_tetromino_col + col] = self._current_tetromino[row][col]
        
    def _check_collision(self):
        for row in range(self._current_tetromino.shape[0] - 1, -1, -1):
            if self._current_tetromino_row + row == self._NUM_ROWS - 1:
                return True
            for col in range(self._current_tetromino.shape[1]):
                if self._current_tetromino[row][col] != 0:
                    if self._grid[self._current_tetromino_row + row + 1][self._current_tetromino_col + col] != 0:
                        return True
        return False
    
    def _check_game_over(self):
        for row in range(self._current_tetromino.shape[0]):
            for col in range(self._current_tetromino.shape[1]):
                if self._current_tetromino[row][col] != 0:
                    if self._grid[self._current_tetromino_row + row][self._current_tetromino_col + col] != 0:
                        self.game_over = True
                        self.running = False
                        return
            
    def _spawn_new_tetromino(self): # Spawn a new tetromino at the top of the grid
        self._current_tetromino = self._next_tetromino
        self._next_tetromino = self._get_random_tetromino()
        self._current_tetromino_row = 0
        self._current_tetromino_col = random.randint(0, self._NUM_COLS - self._current_tetromino.shape[1])

    def _get_random_tetromino(self): # Randomly select a tetromino and rotate it randomly
        tetromino = random.choice(self._TETROMINOES)
        num_rotations = random.randint(0, 3)
        for _ in range(num_rotations):
            tetromino = np.rot90(tetromino)
        return tetromino
