# Connect 4 Minimax Game

This is a Connect 4 game implemented in Python. The game can be played in two modes:
1. Two-player mode (human vs. human)
2. One-player mode (human vs. AI using the Minimax algorithm)

## Requirements

- Python 3.x
- `numpy` library

## Installation

1. Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Install the `numpy` library if you don't have it already. You can install it using `pip`:

    ```bash
    pip install numpy
    ```

    If you're using Python 3, you may need to use `pip3`:

    ```bash
    pip3 install numpy
    ```

## Usage

1. Clone this repository or download the `Minimax.py` file to your local machine.

2. Open a terminal or command prompt and navigate to the directory where `Minimax.py` is located.

3. Run the script:

    ```bash
    python Minimax.py
    ```

    If you're using Python 3, you may need to use:

    ```bash
    python3 Minimax.py
    ```

4. Choose the game mode:
    - Enter `1` for two-player mode (human vs. human).
    - Enter `2` for one-player mode (human vs. AI).

5. Follow the prompts to enter the column number (0-6) where you want to drop your token.

## Game Rules

- Players take turns to drop their tokens into one of the columns.
- The first player to connect four of their tokens vertically, horizontally, or diagonally wins.
- If the board fills up without any player connecting four tokens, the game ends in a tie.
