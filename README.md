# Connect 4 Minimax Game

This is a Connect 4 game implemented in Python. The game can be played in two modes:
1. Two-player mode (human vs. human)
2. One-player mode (human vs. AI using the Minimax algorithm)

## Requirements

- Python 3.x
- `numpy` library
- `streamlit` library

## Installation

1. Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Install the required libraries if you don't have them already. You can install them using `pip`:

    ```bash
    pip install numpy streamlit
    ```

    If you're using Python 3, you may need to use `pip3`:

    ```bash
    pip3 install numpy streamlit
    ```

## Usage

### Running Locally

1. Clone this repository or download the repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory where your files are located.

3. Run the Streamlit app:

    ```bash
    streamlit run streamlit.py
    ```

    This will start a local server and provide you with a URL (usually `http://localhost:8501`) that you can open in your web browser to interact with the app.

### Running on the Web

You can also access the deployed Streamlit app directly on the web without any installation. Visit the following URL:

[Connect 4 Minimax Game on Streamlit](https://apppy-hjdcxnjsqhgwtwuempmvmv.streamlit.app/)

You should select the game mode you want to play first in the left part of the screen.
If you have finished the game or want to start a new one, click the "reset game" button.

## Game Rules

- Players take turns to drop their tokens into one of the columns.
- The first player to connect four of their tokens vertically, horizontally, or diagonally wins.
- If the board fills up without any player connecting four tokens, the game ends in a tie.

## Modes of Play

1. **Two-player mode (human vs. human):** Both players take turns to play the game by clicking on the columns.
2. **One-player mode (human vs. AI):** The player makes their move by clicking on the columns, and the AI will automatically make its move using the Minimax algorithm.

## Repository Structure

- `streamlit_app.py`: The main script to run the Streamlit app.
- `connect4.py`: Contains the game logic for Connect 4.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions!

## License

This project is licensed under the MIT License.
