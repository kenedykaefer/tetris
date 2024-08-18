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
            [0, 0, 1],
            [1, 1, 1]
        ], np.uint8),
        np.array([ # J
            [2, 0, 0],
            [2, 2, 2],
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
            [7, 7, 7, 7]
        ], dtype=np.uint8)
    ]

    def __init__(self):
        self.new_game()        
        
    def new_game(self):
        self.score = 0
        self.game_over = False
        self.grid = np.zeros((self._NUM_ROWS, self._NUM_COLS), np.uint8)
        self.current_tetromino_type = 0
        self.next_tetromino = self._get_random_tetromino()
        self.current_tetromino = self._get_random_tetromino()
        self.current_tetromino_row = 0
        self.current_tetromino_col = random.randint(0, self._NUM_COLS - self.current_tetromino.shape[1])
        self._old_time = time.time()

        for num in self.current_tetromino[0]:
            if num == 0:
                continue
            self.current_tetromino_type = num
            break

        self._running = False
        
        self._reward = 0
        self._rw_full_rows = 0
        
    def get_state(self):
        self._update()
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
    
    def get_init_state_ai(self):
        grid_with_current_tetromino = np.copy(self.grid)
        non_zero_indices = np.argwhere(self.current_tetromino != 0)
        for i, j in non_zero_indices:
            grid_with_current_tetromino[self.current_tetromino_row + i, self.current_tetromino_col + j] = self.current_tetromino[i, j]

        return (grid_with_current_tetromino > 0).astype(np.uint8)

    def get_state_ai(self):     
        self._update()
        
        grid_with_current_tetromino = np.copy(self.grid)
        non_zero_indices = np.argwhere(self.current_tetromino != 0)
        for i, j in non_zero_indices:
            grid_with_current_tetromino[self.current_tetromino_row + i, self.current_tetromino_col + j] = self.current_tetromino[i, j]

        return (grid_with_current_tetromino > 0).astype(np.uint8)

    def get_reward(self):
        if self.game_over:
            return self.score
        
        rw = self._reward
        self._reward = 0

        return rw
    
    def calculate_reward(self):
        rw = 0

        # Encaixe perfeito
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    c_row = self.current_tetromino_row + row
                    c_col = self.current_tetromino_col + col

                    if (0 < c_col < (self._NUM_COLS - 1)):
                        if self.grid[c_row][c_col - 1] != 0:
                            if col == 0 or self.current_tetromino[row][col - 1] == 0:
                                rw += c_row # Lateral Esquerda
                        if self.grid[c_row][c_col + 1] != 0:
                            if col == (self.current_tetromino.shape[1] - 1) or self.current_tetromino[row][col + 1] == 0:
                                rw += c_row # Lateral Direita
                    elif c_col == 0:
                        rw += c_row
                    elif c_col == (self._NUM_COLS - 1):
                        rw += c_row

                    if (0 < c_row < (self._NUM_ROWS - 1)):
                        if self.grid[c_row + 1][c_col] != 0:
                            if row == (self.current_tetromino.shape[0] - 1) or self.current_tetromino[row + 1][col] == 0:
                                rw += c_row # Embaixo
                    elif c_row == (self._NUM_ROWS - 1):
                        rw += c_row
                

        # Buracos
        for col in range(self.current_tetromino.shape[1]):
            row = 0
            while self.current_tetromino[row][col] == 0:
                row += 1
            while (row < self.current_tetromino.shape[0]) and self.current_tetromino[row][col] != 0:
                row +=1
            
            c_row = self.current_tetromino_row + row
            c_col = self.current_tetromino_col + col
            r = 0
            i = 0
            while c_row < self._NUM_ROWS and self.grid[c_row][c_col] == 0:
                i += 1
                r += c_row * 10 * i
                c_row += 1
            rw -= r

        # Topo plano
        min_grid = 0
        for col in range(self.grid.shape[1]):
            row = 0
            while row < self._NUM_ROWS and self.grid[row][col] == 0:
                row += 1
            if row > min_grid:
                min_grid = row
        diff = min_grid - (self.current_tetromino_row + self.current_tetromino.shape[0])

        if diff > 2:
            rw -= self._NUM_COLS * diff * 10

        # Profundidade
        rw += (self.current_tetromino_row + self.current_tetromino.shape[1]) * 10

        # if self._rw_full_rows == 0:
        #     for row in range(self._current_tetromino.shape[0]):
        #         c_row = self._current_tetromino_row + row
        #         rw += np.count_nonzero(self._grid[c_row]) * c_row
        # else: 
        rw += (self._rw_full_rows ** 2) * 1000
        self._rw_full_rows = 0

        self._reward += rw
    
    def get_grid_shape(self):
        return self.grid.shape
        
    def move_tetromino_left(self):
        if self.game_over:
            return False
        self._update()
        for row in range(self.current_tetromino.shape[0]):
            col = 0
            while self.current_tetromino[row][col] == 0:
                col += 1
            if self.current_tetromino_col + col == 0 or self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col - 1] != 0:
                return False
        self.current_tetromino_col -= 1
        return True

    def move_tetromino_right(self):
        if self.game_over:
            return False
        self._update()
        for row in range(self.current_tetromino.shape[0]):
            col = self.current_tetromino.shape[1] - 1
            while self.current_tetromino[row][col] == 0:
                col -= 1
            if self.current_tetromino_col + col == self._NUM_COLS - 1 or self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col + 1] != 0:
                return False
        self.current_tetromino_col += 1
        return True

    def move_tetromino_down(self):
        if self.game_over:
            return False
        self._update()
        r = self._move_down()
        self._old_time = time.time()
        return r
        
    def move_tetromino_hard_drop(self):
        if self.game_over:
            return False
        self._update()
        while self._move_down():
            pass
        self._old_time = time.time()
        return True

    def rotate_tetromino(self):
        if self.game_over:
            return False
        self._update()
        rotated_tetromino = np.rot90(self.current_tetromino)
        new_col = self.current_tetromino_col
        while new_col + rotated_tetromino.shape[1] > self._NUM_COLS:
            new_col -= 1

        if self.current_tetromino_row + rotated_tetromino.shape[0] > self._NUM_ROWS:
            return False

        for row in range(rotated_tetromino.shape[0]):
            for col in range(rotated_tetromino.shape[1]):
                if rotated_tetromino[row][col] != 0:
                    if self.grid[self.current_tetromino_row + row][new_col + col] != 0:
                        return False
                    
        self.current_tetromino = rotated_tetromino
        self.current_tetromino_col = new_col

        return True

    def _update(self):
        if self.game_over:
            return
        if self._running:
            time_elapsed = time.time() - self._old_time
            if time_elapsed >= 1:
                while time_elapsed >= 1:
                    time_elapsed -= 1
                    self._move_down()
                self._old_time = time.time()
        else:
            self._old_time = time.time()
            self._running = True

    def _move_down(self):
        if self._check_collision():
            if self.game_over:
                return False
            self._add_tetromino_to_grid()
            self._check_full_rows()
            self.calculate_reward()
            self._spawn_new_tetromino()
            return False
        else:
            self.current_tetromino_row += 1
            return True

    def _check_full_rows(self):
        num_full_rows = 0
        for row in range(self.grid.shape[0]):
            if 0 not in self.grid[row]:
                num_full_rows += 1
                self.grid = np.delete(self.grid, row, axis=0)
                self.grid = np.insert(self.grid, 0, np.zeros(self._NUM_COLS), axis=0)
        self.score += self._NUM_COLS * (num_full_rows ** 2)
        self._rw_full_rows += num_full_rows

    def _add_tetromino_to_grid(self):
        for row in range(self.current_tetromino.shape[0]):
            for col in range(self.current_tetromino.shape[1]):
                if self.current_tetromino[row][col] != 0:
                    self.grid[self.current_tetromino_row + row][self.current_tetromino_col + col] = self.current_tetromino[row][col]
        
    def _check_collision(self):
        if self._check_game_over():
            return True
        for row in range(self.current_tetromino.shape[0] - 1, -1, -1):
            if self.current_tetromino_row + row == self._NUM_ROWS - 1:
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
                        self.running = False
                        return True
        return False
            
    def _spawn_new_tetromino(self): # Spawn a new tetromino at the top of the grid
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self._get_random_tetromino()
        self.current_tetromino_row = 0
        self.current_tetromino_col = random.randint(0, self._NUM_COLS - self.current_tetromino.shape[1])

        for num in self.current_tetromino[0]:
            if num == 0:
                continue
            self.current_tetromino_type = num
            break

    def _get_random_tetromino(self): # Randomly select a tetromino and rotate it randomly
        tetromino = random.choice(self._TETROMINOES)
        num_rotations = random.randint(0, 3)
        for _ in range(num_rotations):
            tetromino = np.rot90(tetromino)
        return tetromino


def get_future_reward(tetris_game: TetrisGameLogic) -> float:
    if tetris_game.game_over:
        return tetris_game.score
    
    tg = TetrisGameLogic()
    tg.grid = np.copy(tetris_game.grid)
    tg.current_tetromino = np.copy(tetris_game.current_tetromino)
    tg.current_tetromino_row = tetris_game.current_tetromino_row
    tg.current_tetromino_col = tetris_game.current_tetromino_col


    while not tg._check_collision():
        tg.current_tetromino_row += 1

    if tg.game_over:
        return -float('inf')
        
    tg._add_tetromino_to_grid()
    tg._check_full_rows()
    tg.calculate_reward()

    reward = tg.get_reward()

    next_tetromino = np.copy(tetris_game.next_tetromino)
  
    max_num_rotations = 1
    for t in next_tetromino[0]:
        if t == 0:
            continue
        if t in [1, 2, 6]:
            max_num_rotations = 3
        elif t == 3:
            max_num_rotations = 0
        break

    possible_rotations = [next_tetromino]
    for _ in range(max_num_rotations):
        next_tetromino = np.rot90(next_tetromino)
        possible_rotations.append(next_tetromino)

    max_reward = -float('inf')

    for tetromino in possible_rotations:
        tg.current_tetromino = tetromino
        for col in range(tg._NUM_COLS - tetromino.shape[1] + 1):
            tg.current_tetromino_col = col
            tg.current_tetromino_row = 0

            while not tg._check_collision():
                tg.current_tetromino_row += 1

            if not tg.game_over:
                tg._add_tetromino_to_grid()
                tg._check_full_rows()
                tg.calculate_reward()
                max_reward = max(max_reward, tg.get_reward())

                for row in range(tetromino.shape[0]):
                    for col in range(tetromino.shape[1]):
                        if tetromino[row][col] != 0:
                            tg.grid[tg.current_tetromino_row + row][tg.current_tetromino_col + col] = 0

    if max_reward != -float('inf'):
        reward += max_reward

    return reward