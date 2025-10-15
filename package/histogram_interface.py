from abc import ABC, abstractmethod


class HistogramInterface(ABC):

    # method for displaying the histogram of games played per player
    @abstractmethod
    def display_games_played(self):
        pass

    # method for displaying the histogram of wins per player
    @abstractmethod
    def display_wins(self):
        pass
