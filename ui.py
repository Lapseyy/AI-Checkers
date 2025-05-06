import tkinter as tk
from tkinter import messagebox
from game import Game
from AI import MinimaxAI
import random

class CheckersUI:
    def __init__(self, root):
        # This is 
        self.root = root
        self.root.title("Checkers Game")
        self.game = Game()
        
        self.menu_frame = tk.Frame(self.root)
        self.board_frame = tk.Frame(self.root)
        # self.board_frame.pack()
        
        # This allows PvP or AI
        self.game_mode = None
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.ai = MinimaxAI("b")  # Initialize the AI with the black color

        self.start_menu()
        
        # self.create_board()
        # self.update_board()
    def start_menu(self):
        '''This creates the start menu'''
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.menu_frame.pack()
        tk.Label(self.menu_frame, text="Welcome to Competitive Checkers!", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Player vs Player", width=20,
                command=lambda: self.start_game("pvp")).pack(pady=5)
        tk.Button(self.menu_frame, text="Player vs AI", width=20,
                command=lambda: self.start_game("ai")).pack(pady=5)
        tk.Button(self.menu_frame, text="Quit", width=20, command=self.root.quit).pack(pady=5)
        
    def start_game(self, mode):
        '''This starts the game'''
        self.game_mode = mode
        self.menu_frame.pack_forget()
        self.board_frame.pack()
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
        print("Updating board...")
        for row in range(8):
            for col in range(8):
                piece = self.game.board.board[row][col]
                if piece == 0:
                    self.buttons[row][col].config(text="", state=tk.NORMAL)
                else:
                    self.buttons[row][col].config(text=str(
                        piece), state=tk.NORMAL if piece.color == self.game.turn else tk.DISABLED)
        print("Board updated.")

    def clear_highlights(self):
        # This is for the tile highlight 
        # for row in range(8):
        #     for col in range(8):
        #         self.buttons[row][col].config(bg="white" if (row + col) % 2 == 0 else "red")
        # Clear highlights on the board
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.buttons[row][col].config(bg=color)

    def highlight_moves(self, row, col):
        '''This highlights the valid moves for the selected piece'''
        piece = self.game.board.board[row][col]
        valid_moves = self.game.get_valid_moves(piece)
        for move in valid_moves:
            r, c = move
            self.buttons[r][c].config(bg="yellow")

    def ai_move(self):
        """Handles the AI's move"""

        # 1) Ask the AI for its best move
        move = self.ai.choose_move(self.game)
        if move is None:
            messagebox.showinfo("Game Over", "AI has no valid moves. Player wins!")
            self.root.quit()
            return

        # 2) Unpack what the AI returned
        orig_piece, (to_row, to_col), _ = move

        # 3) Locate the live Piece on the real board
        from_row, from_col = orig_piece.row, orig_piece.col
        real_piece = self.game.board.board[from_row][from_col]

        # 4) Perform the move via the Game API
        self.game.move(real_piece, to_row, to_col)

        # 5) Switch back to the human player …
        self.game.switch_turn()

        # 6) …then redraw so you see the piece in its new spot and no ghost left behind
        self.update_board()

        # 7) Finally, check for end‐of‐game
        if self.game.is_game_over():
            winner = self.game.get_winner()
            messagebox.showinfo(
                "Game Over", f"{winner} wins!" if winner else "It's a draw!"
            )
            self.root.quit()

    def on_square_click(self, row, col):
        '''This handles the square click event'''
        # If it's AI's turn, ignore clicks
        if self.game_mode == "ai" and self.game.turn == "b":
            print("It's AI's turn. Player interaction is disabled.")
            return

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
                piece = self.game.board.board[from_row][from_col]
                self.game.move(piece, to_row, to_col)
                self.game.switch_turn()
                self.selected_piece = None
                self.clear_highlights()
                self.update_board()

                if self.game.is_game_over():
                    winner = self.game.get_winner()
                    messagebox.showinfo(
                        "Game Over", f"{winner} wins!" if winner else "It's a draw!")
                    self.root.quit()
                elif self.game_mode == "ai" and self.game.turn == "b":
                    # Schedule AI move after a short delay
                    self.root.after(500, self.ai_move)
            else:
                self.selected_piece = None
                self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersUI(root)
    root.mainloop()