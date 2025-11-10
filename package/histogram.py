""" Histogram class shows player wins and games played. """
from .histogram_interface import HistogramInterface
from .highscore import HighScore


class Histogram(HistogramInterface):
    """ Represents a Histogram. """

    def __init__(self, highscore: HighScore):
        """ Initializes Histogram with a HighScore object.
        Args:
            highscore (HighScore): A HighScore object. """
        self.highscore = highscore

    def display_games_played(self):
        """ Displays ASCII bar chart for games played per player. """
        print("Games Played:")
        for name, stats in self.highscore.get_all_players().items():
            bar = "#" * stats["games_played"]
            print(f"{name:10} | {bar} ({stats['games_played']})")
        print()

    def display_wins(self):
        """ Display ASCII bar chart for wins per player. """
        print("Wins:")
        for name, stats in self.highscore.get_all_players().items():
            bar = "#" * stats["wins"]
            print(f"{name:10} | {bar} ({stats['wins']})")
        print()
