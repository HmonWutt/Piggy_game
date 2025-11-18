import unittest, os, shutil
from functools import wraps

from piggy_game.package import HighScore, Utils


def print_test_result(test_func):
    @wraps(test_func)
    def wrapper(*args):
        try:
            test_func(*args)
            print(f"✓ {test_func.__name__} passed")
            print(
                "----------------------------------------------------------------------"
            )
        except AssertionError as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            raise

    return wrapper


class TestHighscore(unittest.TestCase):
    def setUp(self):
        self.highscore = HighScore()
        self.file_content = {"content": "dummy_content"}
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "highscores.json")
        )

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

    @print_test_result
    def test_add_player(self):
        dict = {
            "Players": {
                "John": {
                    "games_played": 0,
                    "wins": 0,
                    "highest_score": 0,
                }
            }
        }
        self.highscore.add_player("John")
        self.assertEqual(self.highscore.data, dict)

    @print_test_result
    def test_record_game_win(self):
        old_record = {
            "Players": {
                "Julie": {
                    "games_played": 1,
                    "wins": 1,
                    "highest_score": 20,
                }
            }
        }
        self.highscore.record_game("Julie", 20, True)
        self.assertEqual(self.highscore.data, old_record)

    @print_test_result
    def test_record_game_loss(self):
        old_record = {
            "Players": {
                "Jenny": {
                    "games_played": 1,
                    "wins": 0,
                    "highest_score": 40,
                }
            }
        }
        self.highscore.record_game("Jenny", 40, False)
        self.assertEqual(self.highscore.data, old_record)

    def tearDown(self):
        if os.path.isdir(os.path.dirname(self.file_path)):
            shutil.rmtree(os.path.dirname(self.file_path))


if __name__ == "__main__":
    unittest.main()
