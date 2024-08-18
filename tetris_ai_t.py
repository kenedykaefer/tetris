import tetris_game_logic as tgl
import tetris_render as tgr
import numpy as np
import sys
import time
import copy
import threading
import pygame

class TetrisAITosco:
    def __init__(self) -> None:
        self.tg = tgl.TetrisGameLogic()
        self.best_col = 0
        self.best_rotation = 0
        self.move_calculated = False
        self.lock = threading.Lock()
        
        # Render
        self.state = np.array(self.tg.get_grid_shape(), dtype=np.uint8)
        self.score = 0

        self.tr = tgr.TetrisRender(self.tg.grid.shape)

    def best_move(self):
            tg = copy.deepcopy(self.tg)

            current_tetromino = tg.current_tetromino

            max_num_rotations = 1
            for t in current_tetromino[0]:
                if t == 0:
                    continue
                if t in [1, 2, 6]:
                    max_num_rotations = 3
                elif t == 3:
                    max_num_rotations = 0
                break

            possible_rotations = [current_tetromino]
            for _ in range(max_num_rotations):
                current_tetromino = np.rot90(current_tetromino)
                possible_rotations.append(current_tetromino)

            best_reward = -float('inf')
            best_rotation = 0
            best_col = 0

            for rotation, tetromino in enumerate(possible_rotations):
                tg.current_tetromino = tetromino
                for col in range(tg.grid.shape[1] - tetromino.shape[1] + 1):
                    tg.current_tetromino_col = col

                    reward = tgl.get_future_reward(tg)
                    if reward > best_reward:
                        best_reward = reward
                        best_rotation = rotation
                        best_col = col

            with self.lock:            
                self.move_calculated = True
                self.best_rotation = best_rotation
                self.best_col = best_col

    def play(self):
        self.tg.new_game()

        while not self.tg.game_over:
            self.move_calculated = False
            best_move_thread = threading.Thread(target=self.best_move)
            best_move_thread.start()

            while not self.move_calculated:
                self.render()

            best_move_thread.join()

            for _ in range(self.best_rotation):
                self.tg.rotate_tetromino()
                self.render()

            executed = True
            while self.tg.current_tetromino_col != self.best_col and executed:
                if self.tg.current_tetromino_col > self.best_col:
                    executed = self.tg.move_tetromino_left()
                else:
                    executed = self.tg.move_tetromino_right()
                self.render()

            self.tg.move_tetromino_down()
            self.render()     
            while self.tg.current_tetromino_row != 0: 
                self.tg.move_tetromino_down()
                self.render()

    def render(self, str = ''):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.tr.render(self.tg.get_state())
        self.score = self.tg.score
        # self.state = self.tg.get_state_ai()
        # self.tetris_render_cli(str)
        # time.sleep(0.01)

    def tetris_render_cli(self, str='\n'):
        result = []
        result.append("\033[H\033[J")  # Clear the screen
        
        for row in self.state:
            result.extend('██' if col else '⬛' for col in row)
            result.append("\n")

        result.append(f'Score: {self.score}\n')
        result.append(str + '\n')

        sys.stdout.write(''.join(result))
        sys.stdout.flush()

if __name__ == '__main__':        
    pygame.init()

    ai = TetrisAITosco()
    ai.play()
    
    pygame.quit()     
