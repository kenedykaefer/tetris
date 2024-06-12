import tetris_game_logic as tgl
import tetris_render as tr
import pygame
import time
import tetris_user_input as tui

def main():
    pygame.init()
    tetris_game = tgl.TetrisGameLogic()
    tetris_renderer = tr.TetrisRender(tetris_game.get_grid_shape())
    user = tui.TetrisUserInput()

    quit = False

    tetris_game.start_game()
    while not quit:
        while not tetris_game.game_over and not quit:
            tetris_renderer.render(tetris_game.get_state())
            tetris_input = user.get_user_input()

            if tetris_input == 'quit':
                quit = True
            elif tetris_input == 'left':
                tetris_game.move_tetromino_left()
            elif tetris_input == 'right':
                tetris_game.move_tetromino_right()
            elif tetris_input == 'down':
                tetris_game.move_tetromino_down()
            elif tetris_input == 'rotate':
                tetris_game.rotate_tetromino()
            elif tetris_input == 'space':
                tetris_game.move_tetromino_hard_drop()

        tetris_renderer.render(tetris_game.get_state())
        tetris_input = user.get_user_input()
        if tetris_input == 'quit':
            quit = True
        elif tetris_input == 'new_game':
            tetris_game.new_game()
            tetris_game.start_game()

    pygame.quit()        
        
if __name__ == '__main__':
    main()