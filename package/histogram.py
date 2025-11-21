"""Histogram class shows player wins and games played."""

from .highscore import HighScore
from .histogram_interface import HistogramInterface


class Histogram(HistogramInterface):
    """Represent ASCII Histogram for player statistics."""

    def __init__(self, highscore: HighScore):
        """Initialize Histogram with a HighScore object.

        Args:
            highscore (HighScore): A HighScore object.
        """
        self.highscore = highscore

    def display_games_played(self):
        """Display ASCII bar chart for games played per player."""
        players = self.highscore.get_all_players()

        sorted_players = sorted(
            players.items(), key=lambda item: item[1]["games_played"], reverse=True
        )
        print("Games played:")
        for name, stats in sorted_players:
            count = stats["games_played"]
            bar = "🎮" * count
            print(f"{name:12} | {count:3} {bar}")
        print()

    def display_wins(self):
        """Display ASCII bar chart for wins per player."""
        players = self.highscore.get_all_players()

        sorted_players = sorted(
            players.items(), key=lambda item: item[1]["wins"], reverse=True
        )
        print("Wins:")
        for name, stats in sorted_players:
            count = stats["wins"]
            bar = "🏆" * count
            print(f"{name:12} | {count:3} {bar}")
        print()
