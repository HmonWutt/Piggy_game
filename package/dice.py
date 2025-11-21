"""Represents a Dice."""

from random import randint
from .dice_interface import Dice_interface


class Dice(Dice_interface):
    """Dice constructor."""

    def __init__(self):
        """Initialize values."""
        self.face = None
        self.dice_faces = [
            "\u2680",
            "\u2681",
            "\u2682",
            "\u2683",
            "\u2684",
            "\u2685"]

    @property
    def face(self):
        """Return a face."""
        return self._face

    @face.setter
    def face(self, value):
        """Set a face."""
        self._face = value

    def roll(self):
        """Give a random integer between 1 and 6, inclusive."""
        self._face = randint(1, 6)
        return self.face

    def show_graphic_face(self):
        """Give graphical representation of integers."""
        return self.dice_faces[self.face - 1]
