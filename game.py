# This file contains the Game class, which manages the game state and logic.

from board import Board, Piece

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "r"  # "r" = Red starts first

    def switch_turn(self):
        self.turn = "b" if self.turn == "r" else "r"

    def get_valid_moves(self, piece):
        # Ensures moves are only generated for the current player's pieces
        if piece.color != self.turn:
            return {}
        
        moves = {}

        def explore_jumps(piece, row, col, visited):
            '''Recursively explore all jump moves for a piece'''
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                mid_row, mid_col = row + dr, col + dc
                end_row, end_col = row + 2*dr, col + 2*dc

                if 0 <= mid_row < 8 and 0 <= mid_col < 8 and \
                0 <= end_row < 8 and 0 <= end_col < 8:

                    mid_piece  = self.board.board[mid_row][mid_col]
                    end_square = self.board.board[end_row][end_col]

                    if (mid_piece and mid_piece.color != piece.color
                            and end_square == 0
                            and (end_row, end_col) not in visited):
                        moves.setdefault((end_row, end_col), []).append((mid_row, mid_col))

                        # simulate capture
                        self.board.board[mid_row][mid_col] = 0
                        explore_jumps(piece, end_row, end_col, visited | {(end_row, end_col)})
                        # restore
                        self.board.board[mid_row][mid_col] = mid_piece

        # Start by exploring jumps
        explore_jumps(piece, piece.row, piece.col, set())

        # Add normal moves if no jumps are available
        if not moves:
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                row, col = piece.row + dr, piece.col + dc
                if 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] == 0:
                    if piece.king or (piece.color == "r" and dr > 0) or (piece.color == "b" and dr < 0):
                        moves[(row, col)] = []

        return moves

    def _get_valid_moves_recursive(self, piece, moves, jumped, start_row, start_col):
        """Recursively find all valid moves including multiple jumps"""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # If this is not the first move and we haven't captured anything yet,
        # we must capture if possible
        must_capture = len(jumped) > 0
        
        for drow, dcol in directions:
            if not piece.king:
                # Red moves down, Black moves up
                if piece.color == 'r' and drow == -1:
                    continue
                if piece.color == 'b' and drow == 1:
                    continue

            row = start_row + drow
            col = start_col + dcol

            # Regular move (only allowed if no captures are possible)
            if not must_capture and 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] == 0:
                moves[(row, col)] = []

            # Capture move
            if 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] != 0:
                if self.board.board[row][col].color != piece.color:
                    jump_row = row + drow
                    jump_col = col + dcol
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board.board[jump_row][jump_col] == 0:
                        # Check if we've already jumped this piece
                        if (row, col) not in jumped:
                            # Add this capture to the moves
                            moves[(jump_row, jump_col)] = jumped + [(row, col)]
                            
                            # Recursively check for more captures from this position
                            self._get_valid_moves_recursive(piece, moves, jumped + [(row, col)], jump_row, jump_col)

    def has_valid_moves(self, color):
        """Check if a player has any valid moves"""
        pieces = self.board.get_all_pieces(color)
        for piece in pieces:
            if self.get_valid_moves(piece):
                return True
        return False

    def move(self, piece, row, col):
        """Move a piece and handle captures and promotions"""
        # Get the valid moves to check for captures
        valid_moves = self.get_valid_moves(piece)
        
        # Move the piece
        self.board.board[piece.row][piece.col] = 0
        piece.row, piece.col = row, col
        self.board.board[row][col] = piece

        # Handle captures
        if (row, col) in valid_moves:
            jumped = valid_moves[(row, col)]
            for j_row, j_col in jumped:
                self.remove_piece(j_row, j_col)

        # Promote to king if reaching end row
        if (piece.color == "r" and row == 7) or (piece.color == "b" and row == 0):
            piece.make_king()

    def remove_piece(self, row, col):
        """Remove a piece from the board"""
        self.board.board[row][col] = 0

    def is_game_over(self):
         """Check if the game is over (no pieces or no moves for *either* side)"""
         red_count, black_count = self.board.count_pieces()
         # if one side has no pieces, we’re done
         if red_count == 0 or black_count == 0:
             return True
 
         # check moves for both players, regardless of whose turn it is
         original = self.turn
         # can red move?
         self.turn = "r"
         red_can = self.has_valid_moves("r")
         # can black move?
         self.turn = "b"
         black_can = self.has_valid_moves("b")
         # restore
         self.turn = original
 
         # game is over if either side has no moves
         return not (red_can and black_can)

    def get_winner(self):
         """Determine the winner of the game (by pieces or by no‐move for one side)"""
         red_count, black_count = self.board.count_pieces()
         if red_count == 0:
             return "Black"
         if black_count == 0:
             return "Red"
         
         # again, test each color’s mobility
         original = self.turn
         self.turn = "r"
         red_can = self.has_valid_moves("r")
         self.turn = "b"
         black_can = self.has_valid_moves("b")
         self.turn = original
         if not red_can:
             return "Black"
         
         if not black_can:
             return "Red"
         return None
    def evaluate_board(self, color):
        red_score = 0
        black_score = 0
        for row in self.board.board:
            for piece in row:
                if piece != 0:
                    value = 1 + (0.5 if piece.king else 0)
                if piece.color == "r":
                    red_score += value
                else:
                    black_score += value

        return (red_score - black_score) if color == "r" else (black_score - red_score)
    
def minimax(self, depth, alpha, beta, maximizing_player, color):
    """Returns the best score for the current player (maximizing or minimizing)"""
    # Base case: If the depth is 0 or game is over, return the evaluation of the board
    if depth == 0 or self.is_game_over():
        return self.evaluate_board(color)

    # Maximizing for AI 
    if maximizing_player:
        max_eval = float('-inf')
        for move in self.get_all_valid_moves(color):
            self.make_move(move)
            eval = self.minimax(depth - 1, alpha, beta, False, color)
            self.undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  

        return max_eval

    # Minimizing for opponent
    else:
        min_eval = float('inf')
        opponent_color = "r" if color == "b" else "b"
        for move in self.get_all_valid_moves(opponent_color):
            self.make_move(move)
            eval = self.minimax(depth - 1, alpha, beta, True, color)
            self.undo_move(move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  

        return min_eval
    
def ai_move(self):
    """Make the AI move based on the minimax algorithm"""
    best_move = None
    max_eval = float('-inf')
    for move in self.get_all_valid_moves(self.turn):
        self.make_move(move)
        eval = self.minimax(3, float('-inf'), float('inf'), False, self.turn)  
        self.undo_move(move)
        
        if eval > max_eval:
            max_eval = eval
            best_move = move
    
    # Execute the best move
    if best_move:
        self.make_move(best_move)

def make_move(self, move):
    """Simulate making a move on the board"""
    piece, row, col = move
    self.move(piece, row, col)

def undo_move(self, move):
    """Undo a move (restores the board state)"""
    piece, old_row, old_col, captured_positions = move
    # Restore original position
    self.board.board[old_row][old_col] = piece
    self.board.board[piece.row][piece.col] = 0
    piece.row = old_row
    piece.col = old_col

    # Restore captured pieces 
    for captured in captured_positions:
        self.board.board[captured[0]][captured[1]] = captured[2]  


