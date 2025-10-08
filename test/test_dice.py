import sys
import os
import unittest

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from package.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_roll(self):
        self.dice.roll()
        value = self.dice.face
        self.assertTrue(1<=value<=6, f"{value} is not within 1-6")

if __name__ == "__main__":
    unittest.main()
