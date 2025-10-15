import random
from intelligence_interface import Intelligence

class Medium(Intelligence):
    def decide(self, turn_score, total_score, opponent_score):
        if (turn_score < 20):
            return "roll"
        else:
            return "hold"
