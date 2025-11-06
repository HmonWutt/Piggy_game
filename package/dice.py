from .dice_interface import Dice_interface
from random import randint


class Dice(Dice_interface):
    def __init__(self):
        self.face = None
        self.dice_faces = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, value):
        self._face = value

    def roll(self):
        self._face = randint(1, 6)
        return self.face

    def show_graphic_face(self):
        return self.dice_faces[self.face - 1]
