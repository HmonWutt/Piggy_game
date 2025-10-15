from histogram_interface import HistogramInterface
from highscore import HighScore


class Histogram(HistogramInterface):

    # initializes Histogram with a HighScore object
    def _init_(self, highscore: HighScore):
        self.highscore = highscore

    # display ASCII bar chart for games played per player
    def display_games_played(self):
        print("Games Played:")
        for name, stats in self.highscore.get_all_players().items():
            bar = "#" * stats["games_played"]
            print(f"{name:10} | {bar} ({stats['games_played']})")
        print()

    # display ASCII bar chart for wins per player
    def display_wins(self):
        print("Wins:")
        for name, stats in self.highscore.get_all_players().items():
            bar = "#" * stats["wins"]
            print(f"{name:10} | {bar} ({stats['wins']})")
        print()
