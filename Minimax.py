import numpy as np

class Connect4Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)

    def print_board(self, valid_move=True):
        if not valid_move:
            print("Invalid move!")
        for r in reversed(range(self.rows)):
            print(self.board[r])
        print("...................")  # Add separator line

    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[self.rows - 1][col] == 0

    def drop_token(self, col, player):
        if not self.is_valid_move(col):
            return False
        for r in range(self.rows):
            if self.board[r][col] == 0:
                self.board[r][col] = player
                break
        return True

    def undo_move(self, col):
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] != 0:
                self.board[r][col] = 0
                break

    def evaluate_position(self):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(self.board[:, self.cols // 2])]
        center_count = center_array.count(2)
        score += center_count * 3

        # Score horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.cols - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window)

        # Score vertical
        for c in range(self.cols):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window)

        # Score positively sloped diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        # Score negatively sloped diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        score = 0
        opp_piece = 1
        piece = 2
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def minimax(self, depth, maximizing_player, alpha=-np.inf, beta=np.inf):
        valid_moves = [col for col in range(self.cols) if self.is_valid_move(col)]
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner(2):
                    return None, 100000000
                elif self.check_winner(1):
                    return None, -100000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.evaluate_position()

        if maximizing_player:
            value = -np.inf
            column = np.random.choice(valid_moves)
            for col in valid_moves:
                self.drop_token(col, 2)
                new_score = self.minimax(depth - 1, False, alpha, beta)[1]
                self.undo_move(col)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # Minimizing player
            value = np.inf
            column = np.random.choice(valid_moves)
            for col in valid_moves:
                self.drop_token(col, 1)
                new_score = self.minimax(depth - 1, True, alpha, beta)[1]
                self.undo_move(col)
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def is_terminal_node(self):
        return self.check_winner(1) or self.check_winner(2) or len([col for col in range(self.cols) if self.is_valid_move(col)]) == 0

    def check_winner(self, player):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == player:
                    # Check horizontal
                    if c <= self.cols - 4:
                        if self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == player:
                            return True
                    # Check vertical
                    if r <= self.rows - 4:
                        if self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == player:
                            return True
                    # Check diagonal (down-right)
                    if r <= self.rows - 4 and c <= self.cols - 4:
                        if self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == player:
                            return True
                    # Check diagonal (down-left)
                    if r <= self.rows - 4 and c >= 3:
                        if self.board[r+1][c-1] == self.board[r+2][c-2] == self.board[r+3][c-3] == player:
                            return True
        return False

# Function to choose the game mode
def choose_game_mode():
    while True:
        mode = input("Choose game mode:\n1. Two-player game\n2. Play against AI\nEnter choice (1/2): ")
        if mode in ['1', '2']:
            return int(mode)
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Game loop
def play_connect4():
    mode = choose_game_mode()
    board = Connect4Board()
    board.print_board()
    current_player = 1
    while not board.is_terminal_node():
        if mode == 1 or (mode == 2 and current_player == 1):
            try:
                col = int(input(f"Player {current_player}, enter column number (0-6): "))
            except ValueError:
                print("Invalid input! Please enter an integer between 0 and 6.")
                continue
        else:
            col, _ = board.minimax(4, True)
            print(f"AI chooses column {col}")
        if board.is_valid_move(col):
            board.drop_token(col, current_player)
            board.print_board()
            if board.check_winner(current_player):
                print(f"Player {current_player} wins!")
                return
            current_player = 3 - current_player  # Switch player (1 -> 2, 2 -> 1)
        else:
            print("Invalid move! Please try again.")

    print("It's a tie!")

# Start the game
if __name__ == "__main__":
    play_connect4()
