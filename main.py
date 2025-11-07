from package import Game
from InquirerPy import inquirer
import pickle


"""Take input before the main command loop starts"""
action = inquirer.select(
    message="Resume saved game?", choices=["👍 Yes", "👎 No. Start a new game."]
).execute()
game = None
if action.startswith("👍"):
    """Load the saved game object"""
    with open("game_state.pkl", "rb") as f:
        game = pickle.load(f)
        game.set_is_new(False)
        game.intro = """
    ╔═══════════════════════════════════════╗
    ║             Welcome back!             ║
    ╚═══════════════════════════════════════╝
    
                """
else:
    game = Game(True)
game.cmdloop()
