# This file contains the Game class, which manages the game state and logic.

from board import Board, Piece

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "r"  # "r" = Red starts first

    def switch_turn(self):
        self.turn = "b" if self.turn == "r" else "r"

    def get_valid_moves(self, piece):
        # key = (row, col), value = list of pieces jumped (if any)
        moves = {}  
        # diag dirs
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  
        for drow, dcol in directions:
            if not piece.king:
                # Red moves down, Black moves up
                if piece.color == 'r' and drow == -1:
                    continue
                if piece.color == 'b' and drow == 1:
                    continue

            row = piece.row + drow
            col = piece.col + dcol

            # Regular move
            if 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] == 0:
                moves[(row, col)] = []

            # Capture move
            if 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] != 0:
                if self.board.board[row][col].color != piece.color:
                    jump_row = row + drow
                    jump_col = col + dcol
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board.board[jump_row][jump_col] == 0:
                        moves[(jump_row, jump_col)] = [(row, col)]

        return moves

    def has_valid_moves(self, color):
        """Check if a player has any valid moves"""
        pieces = self.board.get_all_pieces(color)
        for piece in pieces:
            if self.get_valid_moves(piece):
                return True
        return False

    def move(self, piece, row, col):
        # Move piece and handle promotion
        self.board.board[piece.row][piece.col] = 0
        piece.row, piece.col = row, col
        self.board.board[row][col] = piece

        # Promote to king if reaching end row
        if (piece.color == "r" and row == 7) or (piece.color == "b" and row == 0):
            piece.make_king()

    def remove_piece(self, row, col):
        self.board.board[row][col] = 0

    def is_game_over(self):
        """Check if the game is over"""
        # Count pieces for both players
        red_count, black_count = self.board.count_pieces()
        
        # Game is over if one player has no pieces
        if red_count == 0 or black_count == 0:
            return True
            
        # Game is over if current player has no valid moves
        if not self.has_valid_moves(self.turn):
            return True
            
        return False

    def get_winner(self):
        """Determine the winner of the game"""
        red_count, black_count = self.board.count_pieces()
        
        if red_count == 0:
            return "Black"
        if black_count == 0:
            return "Red"
            
        if not self.has_valid_moves("r"):
            return "Black"
        if not self.has_valid_moves("b"):
            return "Red"
            
        return None