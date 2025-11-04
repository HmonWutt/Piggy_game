import pytest
from piggy_game.package.player import Player


class TestPlayer:

    def setup_method(self):
        self.player = Player("Alice")

    # the constructor sets the name correctly
    def test_constructor_name(self):
        assert self.player.player_name == "Alice"
        assert isinstance(self.player.player_name, str)

    # checks if change name works
    def test_change_name(self):
        self.player.change_name("Bob")
        assert self.player.player_name == "Bob"
        assert self.player.player_name != "Alice"

    # changing name multiple times
    def test_change_name_multiple(self):
        names = ["Charlie", "Diana", "Eve"]

        for name in names:
            self.player.change_name(name)
            assert self.player.player_name == name
            assert isinstance(self.player.player_name, str)

    # name should always be a string
    def test_name_type(self):
        self.player.change_name("Frank")
        assert isinstance(self.player.player_name, str)
        assert isinstance(self.player.player_name, str)

    # name is never empty
    def test_name_not_empty(self):
        assert self.player.player_name != ""
        self.player.change_name("George")
        assert self.player.player_name != ""
