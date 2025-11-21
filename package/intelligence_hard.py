"""
Defines the Hard AI difficulty strategy for the Piggy Game.

This module contains the Hard class, implementing a strategy for the AI.
The AI will roll the dice while the total score is greater than or equal to 71.
It will also continue rolling if the turn score is less than 25.
Otherwise it will hold.
"""

from .intelligence_interface import Intelligence


class Hard(Intelligence):
    """
    Hard difficulty level strategy for the AI.

    The Hard intelligence makes decisions based on the following premises:
    The AI will roll the dice while the total score is greater than or
    equal to 71. It will also continue rolling if the turn score is less
    than 25. Otherwise it will hold.
    """

    def decide(self, turn_score, total_score, opponent_score):
        """Decide to roll or hold."""
        if total_score >= 71 or turn_score < 25:
            return "roll"
        else:
            return "hold"
