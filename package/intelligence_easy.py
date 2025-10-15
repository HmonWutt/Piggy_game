import random
from intelligence_interface import Intelligence

class Easy(Intelligence):
    def decide(self, turn_score, total_score, opponent_score):
        if (turn_score < 10):
            return "roll"
        else:
            return "hold"
