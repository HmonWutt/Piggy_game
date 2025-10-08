from dice_interface import Dice_interface
from random import randint

class Dice(Dice_interface):
    def __init__(self):
        self.face = None

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self,value):
        self._face = value

    def roll(self):
        self._face = randint(1,7)

