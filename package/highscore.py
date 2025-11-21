"""The HighScore class which saves and loads data from a json file."""

import json
import os

from .highscore_interface import HighScoreInterface


class HighScore(HighScoreInterface):
    """Represent a HighScore."""

    def __init__(self, filepath="data/highscores.json"):
        """Initialize HighScore with json file path.

        Args:
            filepath (str): Path to the json file.
        """
        self.filepath = filepath
        self.data = {"Players": {}}
        self.load_data()

    def load_data(self):
        """Load data from json file or create a new one."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        else:
            self.save_data()

    def save_data(self):
        """Save the current data to the json file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_player(self, player):
        """Add a new player if they dont already exist in the json file.

        Args:
            player (Player): Player object.
        """
        name = player.name
        if name not in self.data["Players"]:
            self.data["Players"][name] = {
                "games_played": 0,
                "wins": 0,
                "highest_score": 0,
            }
        self.save_data()

    def update_player_name(self, old_name: str, new_name: str):
        """Update a players name in the json file.

        Args:
            old_name (str): The players current name saved in the json file.
            new_name (str): The new name which will replace the old one.
        """
        players = self.data["Players"]

        if old_name not in players:
            return

        players[new_name] = players[old_name]
        del players[old_name]
        self.save_data()

    def record_game(self, player1, player2, winner):
        """Update player stats after a match.

        Args:
            player1 (Player): First Player object.
            player2 (Player): Second Player object.
            winner (Player): The Player object who won.
        """
        self.add_player(player1)
        self.add_player(player2)

        for player in (player1, player2):
            name = player.name
            stats = self.data["Players"][name]
            stats["games_played"] += 1

            if player is winner:
                stats["wins"] += 1

            if player.get_score() > stats["highest_score"]:
                stats["highest_score"] = player.get_score()

        self.save_data()

    def get_player_stats(self, name: str) -> dict:
        """Return stats for a player.

        Args:
            name (str): The name of the player.

        Returns:
            dict: Player stats stored as dictionary.
        """
        return self.data["Players"].get(name, {})

    def get_all_players(self) -> dict:
        """Return stats for all players.

        Returns:
            dict: Stats of all players stored as dictionary.
        """
        return self.data["Players"]
