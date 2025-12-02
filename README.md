A fully unbeatable Tic-Tac-Toe game built using Python and Pygame, featuring an AI powered by Minimax with Alpha-Beta pruning, memoization, and board symmetry recognition. The AI plays perfectly, ensuring it never loses, while the human player can enjoy a visually interactive experience.

Features

  Perfect AI:
  The AI uses Minimax with Alpha-Beta pruning and canonical board forms to never lose.
  
  Board Symmetry Optimization:
  Rotations and reflections prevent recalculating equivalent board positions, making AI faster.
  
  Interactive GUI:
  Built with Pygame: click to place your move, see real-time updates, and visually highlighted winning lines.
  
  Player Flexibility:
  You can toggle which player starts (X or O) anytime during the game.

Visual Feedback:

  Turn indicator showing whose move it is.
  
  Result displayed in a colored, highlighted section.
  
  Winning line highlighted in green.
  
  Helpful instructions for first-time players.
  
  Keyboard Shortcut:
  Press R to restart the game instantly

How It Works

  Board Representation:
  The game board is a tuple of 9 elements representing the 3x3 grid. Each element is ' ', 'X', or 'O'.
  
  AI Logic:
  
  Minimax Algorithm: Explores all possible moves to find the optimal one.
  
  Alpha-Beta Pruning: Cuts off branches of the game tree that cannot affect the final decision.
  
  Canonical Form: Rotates and reflects the board to avoid recalculating “look-alike” positions, improving efficiency.
  
  Game Flow:
  
  Human player (O) clicks a cell to move.

  AI (X) responds immediately with its optimal move.
  
  The game continues until a win or draw.
  
  Winning lines are highlighted, and the final result is displayed.
  
  Helper Functions:
  
  empty_board(): Initializes an empty board.
  
  is_terminal(board): Checks if the game has ended.
  
  find_winning_line(board): Determines the winning line.
  
  draw_X() / draw_O(): Draws the symbols on the screen.
  
  highlight_line(): Highlights the winning line.
