import pytest
from package.intelligence_easy import Easy
from package.intelligence_medium import Medium
from package.intelligence_hard import Hard


class TestIntelligenceEasy:
    """Test suite for intelligence_easy class."""

    def setup_method(self):
        """Sets up an instance of Easy Ai before each test."""
        self.ai = Easy()

    def test_easy_roll_low_score(self):
        """Easy Ai should choose roll when turn score is < 10."""
        assert self.ai.decide(5, 0, 0) == "roll"
        assert self.ai.decide(9, 50, 10) == "roll"

    def test_easy_hold_high_score(self):
        """Easy Ai should choose hold when turn score is >= 10."""
        assert self.ai.decide(10, 0, 0) == "hold"
        assert self.ai.decide(15, 40, 30) == "hold"

    def test_easy_boundary_values(self):
        """Easy Ai should choose roll when turn score is < 10 and
        hold when turn score is >= 10."""
        assert self.ai.decide(0, 20, 5) == "roll"
        assert self.ai.decide(9, 90, 60) == "roll"
        assert self.ai.decide(10, 99, 90) == "hold"


class TestIntelligenceMedium:
    """Test suite for intelligence_medium class."""

    def setup_method(self):
        """Sets up an instance of Medium Ai before each test."""
        self.ai = Medium()

    def test_medium_roll_low_score(self):
        """Medium Ai should choose roll when turn score is < 20."""
        assert self.ai.decide(5, 0, 0) == "roll"
        assert self.ai.decide(19, 50, 10) == "roll"

    def test_medium_hold_high_score(self):
        """Medium Ai should choose hold when turn score is >= 20."""
        assert self.ai.decide(20, 0, 0) == "hold"
        assert self.ai.decide(30, 70, 30) == "hold"

    def test_medium_boundary_values(self):
        """Medium Ai should choose roll when turn score is < 20 and
        hold when turn score is >= 20."""
        assert self.ai.decide(0, 20, 5) == "roll"
        assert self.ai.decide(19, 99, 60) == "roll"
        assert self.ai.decide(20, 99, 90) == "hold"


class TestIntelligenceHard:
    """Test suite for intelligence_hard class."""

    def setup_method(self):
        """Sets up an instance of Hard Ai before each test."""
        self.ai = Hard()

    def test_hard_if_can_win_hold(self):
        """Hard Ai should choose hold when total score < 71 or
        turn score > 25."""
        assert self.ai.decide(27, 50, 80) == "hold"
        assert self.ai.decide(26, 56, 30) == "hold"

    def test_hard_roll_under_strategy_conditions(self):
        """Hard Ai should choose roll when total_score >= 71 or
        turn_score < 25."""
        assert self.ai.decide(10, 50, 0) == "roll"
        assert self.ai.decide(24, 75, 70) == "roll"

    def test_hard_otherwise_hold(self):
        """Hard Ai should choose hold when total score < 71 or
        turn score > 25."""
        assert self.ai.decide(30, 50, 90) == "hold"
        assert self.ai.decide(25, 70, 50) == "hold"

    def test_hard_boundary_cases(self):
        """Hard Ai should choose roll when total_score >= 71 or
        turn_score < 25 otherwise hold."""
        assert self.ai.decide(0, 81, 0) == "roll"
        assert self.ai.decide(24, 72, 10) == "roll"
        assert self.ai.decide(25, 50, 30) == "hold"
