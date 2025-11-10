import pytest
from package.player import Player


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
        assert type(self.player.player_name) is str

    # name is never empty
    def test_name_not_empty(self):
        assert self.player.player_name != ""
        self.player.change_name("George")
        assert self.player.player_name != ""
    
    # intial score should be 0
    def test_initial_score(self):
        assert self.player.get_score() == 0
        assert self.player.score == 0
    
    # set score method updates the score correctly
    def test_set_score(self):
        self.player.set_score(10)
        assert self.player.get_score() == 10
        assert self.player.score == 10

    # update score many times
    def test_set_score_many_times(self):
        scores = [5, 20, 50, 0]
        for s in scores:
            self.player.set_scores(s)
            assert self.player.get_score() == s
            assert self.player.score == s

    # score can be 0 or positive
    def test_score_non_negative(self):
        self.player.set_score(0)
        assert self.player.get_score() == 0
        self.player.set_score(15)
        assert self.player.get_score() > 0

    # combination of name change and score
    def test_name_and_score(self):
        self.player.change_name("Hannah")
        self.player.set_score(25)
        assert self.player.player_name == "Hannah"
        assert isinstance(self.player.player_name, str)
        assert self.player.get_score() == 25
        assert self.player.score == 25
