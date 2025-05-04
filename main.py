# This marks the begenining of checkers AI

from game import Game

def get_input():
    try:
        from_row = input("Enter piece ROW (or 'q' to quit): ")
        if from_row.lower() == 'q':
            return None
        from_row = int(from_row)
        
        from_col = int(input("Enter piece COL: "))
        to_row = int(input("Enter DESTINATION ROW: "))
        to_col = int(input("Enter DESTINATION COL: "))
        return (from_row, from_col, to_row, to_col)
    except:
        print("Invalid input format. Try again.")
        return get_input()

def main():
    game = Game()
    show_instructions()
    
    while not game.is_game_over():
        print(f"\nCurrent Turn: {'Red' if game.turn == 'r' else 'Black'}")
        game.board.print_board()

        move = get_input()
        if move is None:
            print("\nGame quit by player.")
            return
            
        from_row, from_col, to_row, to_col = move
        piece = game.board.board[from_row][from_col]

        if piece == 0 or piece.color != game.turn:
            print("Invalid piece selected. Try again.")
            continue

        valid_moves = game.get_valid_moves(piece)

        if (to_row, to_col) in valid_moves:
            game.move(piece, to_row, to_col)

            # Handle capture
            jumped = valid_moves[(to_row, to_col)]
            for j_row, j_col in jumped:
                game.remove_piece(j_row, j_col)

            game.switch_turn()
        else:
            print("Invalid move. Try again.")

    # Game is over, show winner
    winner = game.get_winner()
    if winner:
        print(f"\nGame Over! {winner} wins!")
    else:
        print("\nGame Over! It's a draw!")

def show_instructions():
    print("\n" + "="*40)
    print("Welcome to Competitive Checkers!")
    print("="*40)
    print("HOW TO PLAY:")
    print("- Players take turns: Red ('r') goes first, then Black ('b')")
    print("- Pieces move diagonally on dark squares")
    print("- To move, enter coordinates as:")
    print("  → ROW and COLUMN of the piece to move")
    print("  → ROW and COLUMN of the destination square")
    print("- Example:")
    print("  Enter piece ROW: 2")
    print("  Enter piece COL: 1")
    print("  Enter DESTINATION ROW: 3")
    print("  Enter DESTINATION COL: 0")
    print("- Captures and king promotions are automatic")
    print("- Kings are shown as uppercase (R or B)")
    print("Press Ctrl+C to quit at any time.")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
