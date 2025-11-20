import unittest

from package import Dice, Game, HighScore
from package.intelligence_interface import Intelligence


class TestGame(unittest.TestCase):
    def setUp(self):
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
        game = Game(is_new_game=True)
        self.assertTrue(game.is_new_game)

    # Tests for game setup
    def test_set_number_of_dice(self):
        game = Game()
        game.number_of_dice = 2
        self.assertEqual(game.number_of_dice, 2)

    def test_set_players(self):
        game = Game()
        game.player_one = "Steve"
        game.player_two = "James"
        self.assertEqual(game.player_one, "Steve")
        self.assertEqual(game.player_two, "James")

    def test_set_current_player(self):
        game = Game()
        game.current_player = "Steve"
        self.assertEqual(game.current_player, "Steve")

    def test_set_robot(self):
        game = Game()
        game.is_opponent_robot = True
        self.assertTrue(game.is_opponent_robot)

    def test_assign_intelligence(self):
        class DummyIntelligence(Intelligence):
            def decide(self, turn_score, total_score, opponent_score):
                return "hold"

        game = Game()
        game.intelligence = DummyIntelligence()

        self.assertIsInstance(game.intelligence, Intelligence)
        self.assertEqual(game.intelligence.decide(10, 20, 30), "hold")

    # Tests for game state
    def test_game_in_progress(self):
        game = Game()
        game.is_game_in_progress = True
        self.assertTrue(game.is_game_in_progress)

    def test_game_paused(self):
        game = Game()
        game.is_game_paused = True
        self.assertTrue(game.is_game_paused)

    def test_save_game(self):
        game = Game()
        game.save_game = True
        self.assertTrue(game.save_game)

    # Tests for dice
    def test_roll(self):
        game = Game()
        result = game.dice.roll()
        self.assertTrue(1 <= result <= 6)

    def test_multiple_roll(self):
        game = Game()
        game.number_of_dice = 2

        rolls = [game.dice.roll() for _ in range(10)]
        for r in rolls:
            self.assertTrue(1 <= r <= 6)


if __name__ == "__main__":
    unittest.main()
