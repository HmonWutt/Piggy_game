import json
from this import d
import unittest
from unittest.mock import mock_open, patch
from package import Utils
from .test_highscore import print_test_result


class TestUtils(unittest.TestCase):
    @print_test_result
    def test_write_to_file(self):
        mock = mock_open()

        with patch("builtins.open", mock), patch("json.dump") as mock_dump:
            Utils.write_to_file("data/test.json", {"Greeting": "Hello World"})
        mock.assert_called_once_with("data/test.json", "w")
        mock_dump.assert_called_once_with({"Greeting": "Hello World"}, mock())

    @print_test_result
    def test_read_from_file(self):
        mock = mock_open()
        with (
            patch("builtins.open", mock),
            patch("json.load", return_value={"Greeting": "Hello World"}) as mock_load,
        ):
            result = Utils.read_from_file("data/test.json")
        mock.assert_called_once_with("data/test.json", "r")
        mock_load.assert_called_once_with(mock())
        assert result == {"Greeting": "Hello World"}


if __name__ == "__main__":
    unittest.main()
