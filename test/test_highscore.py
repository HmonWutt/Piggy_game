import unittest, os, shutil
from pathlib import Path
from package.highscore import HighScore
from functools import wraps
from utils.utils import Utils


class TestHighscore(unittest.TestCase):
    def setUp(self):
        self.highscore = HighScore()
        self.file_content = {"content": "dummy_content"}
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "highscores.json")
        )

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
    def test_load_data_no_existing_file(self):
        self.assertTrue(
            os.path.exists(self.file_path),
            f"Expected data/highscores.json to exist but it doesn't",
        )

    @print_test_result
    def test_load_data_with_existing_file(self):
        Utils.write_to_file(self.file_path, self.file_content)
        retrieved = Utils.read_from_file(self.file_path)
        self.highscore.load_data()
        result = self.highscore.data
        self.assertEqual(result, retrieved)

    #
    @print_test_result
    def test_save_data(self):
        content = {"Greeting": {"Hello": "World"}}
        self.highscore.data = content
        self.highscore.save_data()
        self.assertEqual(self.highscore.data, content)

    @print_test_result
    def test_get_player_stats(self):
        self.highscore.data = {"Players": {"player_one": 45, "player_two": 89}}
        result = self.highscore.get_player_stats("player_one")
        self.assertEqual(
            result,
            45,
            f"Expected {45}, got {result}",
        )

    @print_test_result
    def test_get_all_players(self):
        self.highscore.data = {"Players": {"player_one": 100, "player_two": 200}}
        result = self.highscore.get_all_players()
        self.assertEqual(
            result,
            self.highscore.data["Players"],
            f"Expected {self.highscore.data['Players']}, got {result}",
        )

    def tearDown(self):
        if os.path.isdir(os.path.dirname(self.file_path)):
            shutil.rmtree(os.path.dirname(self.file_path))


if __name__ == "__main__":
    unittest.main()
