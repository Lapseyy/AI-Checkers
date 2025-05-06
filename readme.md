# Checkers AI Game

This project is a Checkers game with an optional AI opponent. The game progresses through multiple phases, starting with core game logic and culminating in a graphical user interface (GUI) if time permits.


## 📁 File Overview

| File           | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| `main.py`      | Runs the game loop (human vs. human or AI)                              |
| `board.py`     | Contains `Board` and `Piece` classes — handles data structure           |
| `game.py`      | Manages player turns, checks valid moves, handles promotion and captures |
| `search.py`    | (Provided) AI search algorithms — likely supports `minimax`, `alpha-beta` |
| `ai.py`        | Connects the AI logic from `search.py` to your current board state      |
| `utils.py` *(optional)* | Board rendering, debug logging, or math helpers                |

- 8x8 checkers board with correct initial setup
- Legal move enforcement and turn-based play
- Capture and king promotion rules
- Win condition detection
- AI opponent via Minimax (coming soon!)
- Modular design for easy extension and testing

---

## Notes

- Developed as a final AI course project
- Initial AI algorithms provided by course (`search.py`)
- Goal is functional, interactive play — GUI optional

---
## Running checkers
Running the GUI (Tkinter) on macOS

If you're using macOS and installed Python via Homebrew, you must use Python 3.11 to ensure Tkinter works correctly.
# One-time setup (if not already done):
brew install python-tk@3.11

# Run the game GUI with correct Python version:
- /opt/homebrew/bin/python3.11 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python main.py (for terminal gameplay)

# Please select interpreter 3.11 for UI
press CTRL+P, type or select python
then select 3.11 venv
run command: python ui.py
# You can also create an alias for convenience:
echo 'alias py311="/opt/homebrew/bin/python3.11"' >> ~/.zshrc
source ~/.zshrc

# Now you can run:
py311 -m venv venv

## Future Enhancements

- PyGame or Tkinter GUI visualizations
- Smarter AI using evaluation heuristics