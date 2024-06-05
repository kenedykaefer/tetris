# tetris_ai

## Description

`tetris_ai` is a project that combines the classic Tetris game with artificial intelligence. The goal is to develop a functional Tetris game and then implement and train an AI to play the game.

## Technologies Used

- Python
- Pygame for game rendering 
- NumPy for Tetris piece manipulation and game logic
- AI algorithms (to be defined)

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/kenedykaefer/tetris_ai.git 
    ```

2. Navigate to the project directory:
    ```bash
    cd tetris_ai
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the game:
    ```bash
    python tetris.py
    ```
## How to Play in User Mode

Use the following keyboard controls to play the game 

- `Left Arrow` - Move the piece left
- `Right Arrow` - Move the piece right
- `Up Arrow` - Rotate the piece
- `Down Arrow` - Move the piece down faster
- `Space` - Drop the piece instantly
- `n` - Start a new game (when the game is over)

## Project Structure
```
tetris_ai/
├── tetris.py               # Main implementation of the Tetris game
├── tetris_game_logic.py    # Game logic for Tetris
├── tetris_render.py        # Rendering logic for Tetris
├── tetris_user_input.py    # User input handling
├── requirements.txt        # Project dependencies list
├── LICENSE                 # License file
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
