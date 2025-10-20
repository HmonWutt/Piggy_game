import sys
import os
import unittest

from package import Dice


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_roll(self):
        self.dice.roll()
        value = self.dice.face
        self.assertTrue(1 <= value <= 6, f"{value} is not within 1-6")


if __name__ == "__main__":
    unittest.main()
