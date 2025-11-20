from abc import ABC, abstractmethod


class Dice_interface(ABC):
    @property
    def face(self):
        """subclasses must have a face attribute"""

    @abstractmethod
    def roll(self, *args):
        pass
