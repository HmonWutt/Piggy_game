import unittest, os
from package.highscore import HighScore
from functools import wraps


class TestHighscore(unittest.TestCase):
    def setUp(self):
        self.highscore = HighScore()

    def print_test_result(test_func):
        @wraps(test_func)
        def wrapper(self):
            try:
                test_func(self)
                print(f"✓ {test_func.__name__} passed")
                print(
                    "----------------------------------------------------------------------"
                )
            except AssertionError as e:
                print(f"✗ {test_func.__name__} failed: {e}")
                raise

        return wrapper

    @print_test_result
    def test_load_data(self):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "package", "data", "highscores.json"
            )
        )
        self.assertTrue(
            os.path.exists(file_path),
            f"Expected data/highscores.json to exist but it doesn't",
        )

    @print_test_result
    def test_get_player_stats(self):
        self.highscore.data = {"Players": {"player_one": 45, "player_two": 89}}
        result = self.highscore.get_player_stats("player_one")
        self.assertTrue(
            result == 45,
            f"Expected {45}, got {result}",
        )


if __name__ == "__main__":
    unittest.main()
