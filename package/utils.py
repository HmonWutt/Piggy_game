"""The utils.py class."""

import json


class Utils:
    """Represent a Utils."""

    welcome_back_banner = """
    ╔═══════════════════════════════════════╗
    ║             Welcome back!             ║
    ╚═══════════════════════════════════════╝
"""
    banner_text = """Rules:
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

    welcome_banner = """
    ╔═══════════════════════════════════════╗
    ║         Welcome to PIG GAME!          ║
    ╚═══════════════════════════════════════╝

"""

    @staticmethod
    def write_to_file(file_path, file_content):
        """Write to file."""
        with open(file_path, "w") as f:
            json.dump(file_content, f)

    @staticmethod
    def read_from_file(file_path):
        """Read from file."""
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def print_dict_table(data, title="My Table"):  # pragma no cover
        """Print title."""
        print(f"\n{title}")

        """Calculate column width."""
        key_width = max(len(str(k)) for k in data.keys())
        val_width = max(len(str(v)) for v in data.values())

        """Print column names."""
        print(f"{'Key'.ljust(key_width)} | {'Value'.ljust(val_width)}")
        print("-" * (key_width + val_width + 3))

        """Print data."""
        for key, value in data.items():
            print(f"{str(key).ljust(key_width)} | {str(value).ljust(val_width)}\n")
