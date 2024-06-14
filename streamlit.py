import streamlit as st
import numpy as np

# Connect4 Game Logic

class Connect4Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)

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
        center_array = [int(i) for i in list(self.board[:, self.cols // 2])]
        center_count = center_array.count(2)
        score += center_count * 3
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.cols - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window)
        for c in range(self.cols):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window)
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
                else:
                    return None, 0
            else:
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
        else:
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
                    if c <= self.cols - 4:
                        if self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == player:
                            return True
                    if r <= self.rows - 4:
                        if self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == player:
                            return True
                    if r <= self.rows - 4 and c <= self.cols - 4:
                        if self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == player:
                            return True
                    if r <= self.rows - 4 and c >= 3:
                        if self.board[r+1][c-1] == self.board[r+2][c-2] == self.board[r+3][c-3] == player:
                            return True
        return False

# Streamlit UI

def main():
    st.title("Connect 4 Game")
    game_mode = st.sidebar.selectbox("Select Game Mode", ["Player vs Player", "Player vs AI"])
    
    if "board" not in st.session_state:
        st.session_state.board = Connect4Board()
    if "current_player" not in st.session_state:
        st.session_state.current_player = 1
    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    def render_board():
        for r_idx, row in enumerate(reversed(st.session_state.board.board)):
            cols = st.columns(st.session_state.board.cols)
            for c_idx, cell in enumerate(row):
                key = f"{r_idx}-{c_idx}"
                if cell == 0:
                    cols[c_idx].button(" ", key=key, on_click=make_move, args=(c_idx,))
                elif cell == 1:
                    cols[c_idx].button("🔴", key=key)
                else:
                    cols[c_idx].button("🔵", key=key)

    def make_move(col):
        if st.session_state.game_over:
            st.warning("Game over. Please restart to play again.")
            return
        if st.session_state.board.is_valid_move(col):
            st.session_state.board.drop_token(col, st.session_state.current_player)
            if st.session_state.board.check_winner(st.session_state.current_player):
                st.session_state.game_over = True
                st.success(f"Player {st.session_state.current_player} wins!")
            elif st.session_state.board.is_terminal_node():
                st.session_state.game_over = True
                st.info("It's a tie!")
            else:
                st.session_state.current_player = 3 - st.session_state.current_player
                if game_mode == "Player vs AI" and st.session_state.current_player == 2:
                    col, _ = st.session_state.board.minimax(4, True)
                    st.session_state.board.drop_token(col, 2)
                    if st.session_state.board.check_winner(2):
                        st.session_state.game_over = True
                        st.success("AI wins!")
                    elif st.session_state.board.is_terminal_node():
                        st.session_state.game_over = True
                        st.info("It's a tie!")
                    else:
                        st.session_state.current_player = 1

    if st.button("Restart Game"):
        st.session_state.board = Connect4Board()
        st.session_state.current_player = 1
        st.session_state.game_over = False

    render_board()

if __name__ == "__main__":
    main()