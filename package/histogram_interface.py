""" The interface for Histogram class. """

from abc import ABC, abstractmethod


class HistogramInterface(ABC):
    """ Interface for Histogram class. """

    @abstractmethod
    def display_games_played(self):
        """ Method for displaying the histogram of games played per player. """
        pass

    @abstractmethod
    def display_wins(self):
        """ Method for displaying the histogram of wins per player. """
        pass
