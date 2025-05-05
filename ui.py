import tkinter as tk
from tkinter import messagebox
from game import Game


class CheckersUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers Game")

        self.game = Game()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None

        self.create_board()
        self.update_board()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                button = tk.Button(self.board_frame, bg=color, width=4, height=2,
                                   command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def update_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board.board[row][col]
                if piece == 0:
                    self.buttons[row][col].config(text="", state=tk.NORMAL)
                else:
                    self.buttons[row][col].config(text=str(
                        piece), state=tk.NORMAL if piece.color == self.game.turn else tk.DISABLED)

    def clear_highlights(self):
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.buttons[row][col].config(bg=color)

    def on_square_click(self, row, col):
        self.clear_highlights()  # Clear previous highlights
        if self.selected_piece is None:
            piece = self.game.board.board[row][col]
            if piece != 0 and piece.color == self.game.turn:
                self.selected_piece = (row, col)
                self.highlight_moves(row, col)
        else:
            from_row, from_col = self.selected_piece
            to_row, to_col = row, col
            valid_moves = self.game.get_valid_moves(
                self.game.board.board[from_row][from_col])
            if (to_row, to_col) in valid_moves:
                self.game.move(
                    self.game.board.board[from_row][from_col], to_row, to_col)
                for j_row, j_col in valid_moves[(to_row, to_col)]:
                    self.game.remove_piece(j_row, j_col)
                self.game.switch_turn()
                self.selected_piece = None
                self.update_board()

                if self.game.is_game_over():
                    winner = self.game.get_winner()
                    messagebox.showinfo(
                        "Game Over", f"{winner} wins!" if winner else "It's a draw!")
                    self.root.quit()
            else:
                self.selected_piece = None
                self.update_board()

    def highlight_moves(self, row, col):
        piece = self.game.board.board[row][col]
        valid_moves = self.game.get_valid_moves(piece)
        for move in valid_moves:
            r, c = move
            self.buttons[r][c].config(bg="yellow")


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersUI(root)
    root.mainloop()