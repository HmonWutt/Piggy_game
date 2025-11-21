"""Test for dice class."""

import unittest
from package.dice import Dice


class TestDice(unittest.TestCase):
    """Test suite for dice.py."""

    def test_roll(self):
        """Test if the return value of function is between 1 and 6, inclusive."""
        dice = Dice()
        dice.roll()
        value = dice.face
        self.assertTrue(1 <= value <= 6, f"{value} is not within 1-6")


if __name__ == "__main__":
    unittest.main()
