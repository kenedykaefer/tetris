import pygame

class TetrisRender:
    # Colors
    _COLOR_DARK = (20, 20, 20)
    _COLOR_WHITE = (255, 255, 255)

    _TREMINOES_COLORS = [
        (0, 0, 0), # Empty
        (0, 255, 0), # Green
        (0, 0, 255), # Blue
        (255, 255, 0), # Yellow
        (255, 0, 0), # Red
        (255, 165, 0), # Orange
        (128, 0, 128), # Purple
        (0, 255, 255) # Cyan
    ]
    
    #Screen
    _SCREEN_FPS = 60
    _IMFORMATION_PANEL_WIDTH = 200

    # Grid
    _GRID_SIZE = 30

    def __init__(self, grid_shape):
        self._SCREEN_WIDTH = grid_shape[1] * self._GRID_SIZE + self._IMFORMATION_PANEL_WIDTH
        self._SCREEN_HEIGHT = grid_shape[0] * self._GRID_SIZE
        self._NUM_GRID_COLS = grid_shape[1]

        pygame.display.set_caption('Tetris')
        self._screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))  
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, 36)

    def render(self, tetris_game_state):
        self._screen.fill(self._COLOR_DARK)
        self._draw_grid(tetris_game_state['grid'])
        self._draw_tetromino(tetris_game_state['grid'], tetris_game_state['current_tetromino'], tetris_game_state['current_tetromino_row'], tetris_game_state['current_tetromino_col'])
        self._draw_next_tetromino(tetris_game_state['next_tetromino'])
        self._draw_score(tetris_game_state['score'])
        self._draw_game_over(tetris_game_state['game_over'])
        pygame.display.flip()
        self._clock.tick(self._SCREEN_FPS)

    def _draw_grid(self, grid):
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                pygame.draw.rect(self._screen, self._TREMINOES_COLORS[int(grid[row, col])], (col * self._GRID_SIZE + .5, row * self._GRID_SIZE + .5, self._GRID_SIZE - 1, self._GRID_SIZE - 1), 0)

    def _draw_tetromino(self, grid, tetromino, tetromino_row, tetromino_col):
        for row in range(tetromino.shape[0]):
            for col in range(tetromino.shape[1]):
                if tetromino[row, col] != 0:
                    color = self._TREMINOES_COLORS[int(tetromino[row, col])] if grid[row + tetromino_row, col + tetromino_col] == 0 else (255, 255, 255)
                    pygame.draw.rect(self._screen, color, ((col + tetromino_col) * self._GRID_SIZE + .5, (row + tetromino_row) * self._GRID_SIZE + .5, self._GRID_SIZE - 1, self._GRID_SIZE - 1), 0)

    def _draw_next_tetromino(self, next_tetromino):
        row = self._SCREEN_HEIGHT // 10 * 3
        col = self._NUM_GRID_COLS * self._GRID_SIZE + self._IMFORMATION_PANEL_WIDTH / 2
        text = self._font.render('Next Tetromino', True, self._COLOR_WHITE)
        self._screen.blit(text, text.get_rect(center=(col, row)))
        row += self._GRID_SIZE
        next_tetromino_center = (next_tetromino.shape[1] * self._GRID_SIZE) / 2
        for r in range(next_tetromino.shape[0]):
            for c in range(next_tetromino.shape[1]):
                if next_tetromino[r, c] != 0:
                    pygame.draw.rect(self._screen, self._TREMINOES_COLORS[int(next_tetromino[r, c])], (c * self._GRID_SIZE + col - next_tetromino_center, r * self._GRID_SIZE + row, self._GRID_SIZE - 1, self._GRID_SIZE - 1), 0)

    def _draw_score(self, score):
        row = self._SCREEN_HEIGHT // 10
        col = self._NUM_GRID_COLS * self._GRID_SIZE + self._IMFORMATION_PANEL_WIDTH / 2
        text = self._font.render('Score', True, self._COLOR_WHITE)
        self._screen.blit(text, text.get_rect(center=(col, row)))
        row += self._GRID_SIZE
        text = self._font.render(str(score), True, self._COLOR_WHITE)
        self._screen.blit(text, text.get_rect(center=(col, row)))

    def _draw_game_over(self, game_over):
        if game_over:
            row = (self._SCREEN_HEIGHT // 3) * 2
            col = self._NUM_GRID_COLS * self._GRID_SIZE + self._GRID_SIZE
            text = self._font.render('Game Over', True, self._COLOR_WHITE)
            self._screen.blit(text, (col, row))
