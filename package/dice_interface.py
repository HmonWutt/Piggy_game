"""Interface for the dice class."""

from abc import ABC, abstractmethod


class Dice_interface(ABC):
    """Represent a dice."""

    @property
    def face(self):
        """Subclasses must have a face attribute."""

    @abstractmethod
    def roll(self, *args):
        """Give a random integer between 1 and 6, inclusive."""
        pass
