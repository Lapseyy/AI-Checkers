# AI.py

from copy import deepcopy
from game import Game

class MinimaxAI:
    def __init__(self, color, max_depth=6):
        self.color = color
        self.max_depth = max_depth

    def choose_move(self, game):
        # 1 Work on a clone of the board so we never touch the real one
        board_copy = deepcopy(game.board)
        # 2 Run minimax on the **copy**
        def minimax(state, depth, alphas, beta, maximizing):
            if depth == 0 or not state.get_all_pieces(self.color):
                return self.evaluate(state), None

            best_move = None
            if maximizing:
                max_eval = -float('inf')
                # for move in state.get_all_moves(self.color):
                #     # move is (piece_clone, (to_row, to_col), captured_list)
                #     # find *that* piece on the cloned state:
                #     p_clone, (tr, tc), cap = move
                #     from_r, from_c = p_clone.row, p_clone.col
                #     # construct a new move tuple that references the clone in this state
                #     real_clone = state.board[from_r][from_c]
                #     new_move = (real_clone, (tr, tc), cap)

                #     next_state = deepcopy(state)
                #     next_state.make_move(new_move)
                for p_clone, (tr, tc), cap in state.get_all_moves(self.color):
                    from_r, from_c = p_clone.row, p_clone.col
                    next_state = deepcopy(state)
                    piece_copy = next_state.board[from_r][from_c]
                    new_move = (piece_copy, (tr, tc), cap)
                    next_state.make_move(new_move)

                    eval_score, _ = minimax(next_state, depth-1, alphas, beta, False)
                    if eval_score > max_eval:
                        max_eval, best_move = eval_score, new_move
                    alphas = max(alphas, eval_score)
                    if beta <= alphas:
                        break
                return max_eval, best_move
            else:
                min_eval = float('inf')
                opponent = 'b' if self.color == 'r' else 'r'
                for move in state.get_all_moves(opponent):
                    p_clone, (tr, tc), cap = move
                    from_r, from_c = p_clone.row, p_clone.col
                    real_clone = state.board[from_r][from_c]
                    new_move = (real_clone, (tr, tc), cap)

                    next_state = deepcopy(state)
                    next_state.make_move(new_move)

                    eval_score, _ = minimax(next_state, depth-1, alphas, beta, True)
                    if eval_score < min_eval:
                        min_eval, best_move = eval_score, new_move
                    beta = min(beta, eval_score)
                    if beta <= alphas:
                        break
                return min_eval, best_move

        # 2) Run minimax on the **copy**
        _, best = minimax(board_copy, self.max_depth, -float('inf'), float('inf'), True)
        if best is None:
            return None

        # 3) Unpack the clone-based move and return **coordinates only**
        _, (to_r, to_c), jumped = best
        from_r, from_c = best[0].row, best[0].col
        return (from_r, from_c), (to_r, to_c), jumped

    def evaluate(self, state):
        val = 0
        for row in state.board:
            for p in row:
                if p != 0:
                    sign = (1 if p.color == self.color else -1)
                    val += sign * (1 + 0.5 * p.king)
        return val