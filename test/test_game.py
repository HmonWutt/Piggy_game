"""Test for game class."""

import unittest
from package import Dice, Game, HighScore
from package.intelligence_interface import Intelligence


class TestGame(unittest.TestCase):
    """Test suite for game class."""

    def setUp(self):
        """Set up the test."""
        game = Game()

        self.assertFalse(game.is_new_game)
        self.assertIsNone(game.player_one)
        self.assertIsNone(game.player_two)
        self.assertFalse(game.is_opponent_robot)
        self.assertIsNone(game.current_player)
        self.assertIsInstance(game.dice, Dice)
        self.assertIsInstance(game.score_record, HighScore)
        self.assertEqual(game.number_of_dice, 0)
        self.assertIsNone(game.intelligence)
        self.assertFalse(game.save_game)
        self.assertFalse(game.is_game_in_progress)
        self.assertFalse(game.is_game_paused)

    def test_new_game(self):
        """Test a new game."""
        game = Game(is_new_game=True)
        self.assertTrue(game.is_new_game)

    def test_set_number_of_dice(self):
        """Test game setup."""
        game = Game()
        game.number_of_dice = 2
        self.assertEqual(game.number_of_dice, 2)

    def test_set_players(self):
        """Test setting players."""
        game = Game()
        game.player_one = "Steve"
        game.player_two = "James"
        self.assertEqual(game.player_one, "Steve")
        self.assertEqual(game.player_two, "James")

    def test_set_current_player(self):
        """Test setting the current player."""
        game = Game()
        game.current_player = "Steve"
        self.assertEqual(game.current_player, "Steve")

    def test_set_robot(self):
        """Test setting a robot."""
        game = Game()
        game.is_opponent_robot = True
        self.assertTrue(game.is_opponent_robot)

    def test_assign_intelligence(self):
        """Test assigning an intelligence."""
        class DummyIntelligence(Intelligence):
            def decide(self, turn_score, total_score, opponent_score):
                return "hold"

        game = Game()
        game.intelligence = DummyIntelligence()

        self.assertIsInstance(game.intelligence, Intelligence)
        self.assertEqual(game.intelligence.decide(10, 20, 30), "hold")

    def test_game_in_progress(self):
        """Test game state."""
        game = Game()
        game.is_game_in_progress = True
        self.assertTrue(game.is_game_in_progress)

    def test_game_paused(self):
        """Test if game is paused."""
        game = Game()
        game.is_game_paused = True
        self.assertTrue(game.is_game_paused)

    def test_save_game(self):
        """Test saving a game."""
        game = Game()
        game.save_game = True
        self.assertTrue(game.save_game)

    def test_roll(self):
        """Test a dice roll."""
        game = Game()
        result = game.dice.roll()
        self.assertTrue(1 <= result <= 6)

    def test_multiple_roll(self):
        """Test multiple dice rolls."""
        game = Game()
        game.number_of_dice = 2

        rolls = [game.dice.roll() for _ in range(10)]
        for r in rolls:
            self.assertTrue(1 <= r <= 6)


if __name__ == "__main__":
    unittest.main()
