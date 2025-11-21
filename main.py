"""The main class to run the game."""

import pickle
from InquirerPy import inquirer
from package import Game, Utils

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
        game.intro = Utils.welcome_back_banner + Utils.banner_text
else:
    game = Game(True)
game.cmdloop()
