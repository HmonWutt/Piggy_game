from package import Player


class TestPlayer:
    """Test suite for Player class."""

    def setup_method(self):
        """Sets up an instance before test."""
        self.player = Player("Alice")

    def test_constructor_name(self):
        """The constructor should set the name correctly."""
        assert self.player.name == "Alice"
        assert isinstance(self.player.name, str)

    def test_change_name(self):
        """Name change should work."""
        self.player.change_name("Bob")
        assert self.player.name == "Bob"
        assert self.player.name != "Alice"

    def test_change_name_multiple(self):
        """Changing names multiple times should work."""
        names = ["Charlie", "Diana", "Eve"]

        for name in names:
            self.player.change_name(name)
            assert self.player.name == name
            assert isinstance(self.player.name, str)

    def test_name_type(self):
        """Name should always be a string."""
        self.player.change_name("Frank")
        assert isinstance(self.player.name, str)
        assert type(self.player.name) is str

    def test_name_not_empty(self):
        """Name should never be empty."""
        assert self.player.name != ""
        self.player.change_name("George")
        assert self.player.name != ""

    def test_initial_score(self):
        """Intial score should be 0."""
        assert self.player.get_score() == 0
        assert self.player.score == 0

    def test_set_score(self):
        """set_score method should update the score correctly."""
        self.player.set_score(10)
        assert self.player.get_score() == 10
        assert self.player.score == 10

    def test_set_score_many_times(self):
        """Update score many times correctly."""
        scores = [5, 20, 50, 0]
        for s in scores:
            self.player.set_score(s)
            assert self.player.get_score() == s
            assert self.player.score == s

    def test_score_non_negative(self):
        """Score can be 0 or positive."""
        self.player.set_score(0)
        assert self.player.get_score() == 0
        self.player.set_score(15)
        assert self.player.get_score() > 0

    def test_name_and_score(self):
        """Combination of name change and score."""
        self.player.change_name("Hannah")
        self.player.set_score(25)
        assert self.player.name == "Hannah"
        assert isinstance(self.player.name, str)
        assert self.player.get_score() == 25
        assert self.player.score == 25
