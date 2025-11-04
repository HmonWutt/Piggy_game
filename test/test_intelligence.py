import pytest
from piggy_game.package.intelligence_easy import Easy
from piggy_game.package.intelligence_medium import Medium
from piggy_game.package.intelligence_hard import Hard


class TestIntelligenceEasy:
    def setup_method(self):
        self.ai = Easy()

    def test_easy_roll_low_score(self):
        assert self.ai.decide(5, 0, 0) == "roll"
        assert self.ai.decide(9, 50, 10) == "roll"

    def test_easy_hold_high_score(self):
        assert self.ai.decide(10, 0, 0) == "hold"
        assert self.ai.decide(15, 40, 30) == "hold"

    def test_easy_boundary_values(self):
        assert self.ai.decide(0, 20, 5) == "roll"
        assert self.ai.decide(9, 90, 60) == "roll"
        assert self.ai.decide(10, 99, 90) == "hold"


class TestIntelligenceMedium:
    def setup_method(self):
        self.ai = Medium()

    def test_medium_roll_low_score(self):
        assert self.ai.decide(5, 0, 0) == "roll"
        assert self.ai.decide(19, 50, 10) == "roll"

    def test_medium_hold_high_score(self):
        assert self.ai.decide(20, 0, 0) == "hold"
        assert self.ai.decide(30, 70, 30) == "hold"

    def test_medium_boundary_values(self):
        assert self.ai.decide(0, 20, 5) == "roll"
        assert self.ai.decide(19, 99, 60) == "roll"
        assert self.ai.decide(20, 99, 90) == "hold"


class TestIntelligenceHard:
    def setup_method(self):
        self.ai = Hard()

    def test_hard_if_can_win_hold(self):
        assert self.ai.decide(20, 90, 80) == "hold"
        assert self.ai.decide(5, 97, 30) == "hold"

    def test_hard_roll_under_strategy_conditions(self):
        assert self.ai.decide(10, 50, 0) == "roll"
        assert self.ai.decide(24, 75, 70) == "roll"

    def test_hard_otherwise_hold(self):
        assert self.ai.decide(30, 50, 90) == "hold"
        assert self.ai.decide(25, 70, 50) == "hold"

    def test_hard_boundary_cases(self):
        assert self.ai.decide(0, 71, 0) == "roll"
        assert self.ai.decide(24, 71, 10) == "roll"
        assert self.ai.decide(25, 70, 30) == "hold"
