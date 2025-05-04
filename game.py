# This file contains the Game class, which manages the game state and logic.

from board import Board, Piece

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "r"  # "r" = Red starts first

    def switch_turn(self):
        self.turn = "b" if self.turn == "r" else "r"

    def get_valid_moves(self, piece):
        # Will implement in next step
        pass

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
        # Will implement win detection later
        return False
    
    
    def get_valid_moves(self, piece):
        moves = {}  # key = (row, col), value = list of pieces jumped (if any)

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diag dirs
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
            jump_row = piece.row + drow * 2
            jump_col = piece.col + dcol * 2
            if (
                0 <= jump_row < 8 and 0 <= jump_col < 8
                and self.board.board[row + drow][col + dcol] != 0
                and self.board.board[row + drow][col + dcol].color != piece.color
                and self.board.board[jump_row][jump_col] == 0
            ):
                moves[(jump_row, jump_col)] = [(row + drow, col + dcol)]

        return moves
