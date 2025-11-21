"""__init__.py class."""

from .dice import Dice
from .game import Game
from .highscore import HighScore
from .histogram import Histogram
from .intelligence_easy import Easy
from .intelligence_hard import Hard
from .intelligence_medium import Medium
from .player import Player
from .utils import Utils

print("imported package")
__all__ = [
    "Utils",
    "Player",
    "Medium",
    "Hard",
    "Easy",
    "Histogram",
    "HighScore",
    "Game",
    "Dice"]
