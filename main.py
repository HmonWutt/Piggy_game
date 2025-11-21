"""The main class to run the game."""

import pickle
from InquirerPy import inquirer
from package import Game

"""Take input before the main command loop starts."""
action = inquirer.select(
    message="Resume saved game?", choices=["✅ Yes", "❌No. Start a new game."]
).execute()
game = None
if action.startswith("✅"):
    """Load the saved game object."""
    with open("game_state.pkl", "rb") as f:
        game = pickle.load(f)
        game.set_is_new_game(False)
        game.intro = """
    ╔═══════════════════════════════════════╗
    ║             Welcome back!             ║
    ╚═══════════════════════════════════════╝
      Rules:
    - Race to 100 points to win
    - Roll dice to accumulate points in your turn
    - If you roll a 1, you lose all turn points and your turn ends.
      If you roll double 1s (in two-dice game), you lose all accumulated
      points for the game and your turn ends

    Actions:
    - Type 'start' to start a game
    - Type 'changename' to change your name
    - Type 'help' for all commands
    - Type 'play' to play
    - Type 'cheat' to win the round
    - Type 'pause' to pause the game
    - Type 'unpause' to resume the game
    - Type 'show' to see the leaderboard
    - Type 'exit' to exit the game
 """
else:
    game = Game(True)
game.cmdloop()
