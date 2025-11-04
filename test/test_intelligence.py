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
