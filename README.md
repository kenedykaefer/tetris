# tetris

## Description

`tetris` is a project that combines the classic Tetris game with artificial intelligence. The goal is to develop a functional Tetris game and implement various AI approaches to play the game. This includes both traditional and reinforcement learning techniques, with a focus on experimenting and iterating on different AI models.

## Technologies Used

- Python
- Pygame for game rendering 
- NumPy for Tetris piece manipulation and game logic
- AI algorithms:
  - Q-learning (with current implementation needing improvement)
  - Custom AI logic (e.g., `TetrisAITosco` for a simpler approach)

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/kenedykaefer/tetris.git 
    ```

2. Navigate to the project directory:
    ```bash
    cd tetris_ai
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play in User Mode

Run the game:

```bash
python tetris.py
```

Use the following keyboard controls to play the game:

- `Left Arrow` - Move the piece left
- `Right Arrow` - Move the piece right
- `Up Arrow` - Rotate the piece
- `Down Arrow` - Move the piece down faster
- `Space` - Drop the piece instantly
- `n` - Start a new game (when the game is over)

## Running the AI

### TetrisAITosco

`TetrisAITosco` is a simpler AI that calculates the best move using basic heuristics. It’s not the most sophisticated AI, but it works reliably for what it is.

To run `TetrisAITosco`:

```bash
python tetris_ai_t.py
```

### TetrisQLearning

The `TetrisQLearning` class implements a Q-learning AI that attempts to learn optimal moves through training. However, this implementation is still a work in progress and requires further refinement. The current model has started to show some signs of learning but is not yet fully optimized.

To run the Q-learning AI:

```bash
python tetris_ai_qlearning.py
```

## Project Structure
```
tetris_ai/
├── tetris.py               # Main implementation of the Tetris game
├── tetris_game_logic.py    # Game logic for Tetris
├── tetris_render.py        # Rendering logic for Tetris
├── tetris_user_input.py    # User input handling
├── tetris_ai_t.py          # Custom AI implementation (e.g., TetrisAITosco)
├── tetris_ai_qlearning.py  # Q-learning AI implementation
├── requirements.txt        # Project dependencies list
├── LICENSE                 # License file
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
