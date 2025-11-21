"""The interface for Histogram class."""

from abc import ABC, abstractmethod


class HistogramInterface(ABC):
    """Interface for Histogram class."""

    @abstractmethod
    def display_games_played(self):
        """Display the histogram of games played per player."""
        pass

    @abstractmethod
    def display_wins(self):
        """Display the histogram of wins per player."""
        pass
