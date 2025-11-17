import random
from .intelligence_interface import Intelligence


class Hard(Intelligence):
    def decide(self, turn_score, total_score, opponent_score):
        if total_score >= 71 or turn_score < 25:
            return "roll"
        else:
            return "hold"
