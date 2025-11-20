"""
Defines the Easy AI difficulty strategy for the Piggy Game.

This module contains the Easy class, implementing a strategy for the AI.
The Easy intelligence rolls the
dice until the turn score reaches 10, then chooses to hold.
"""

from .intelligence_interface import Intelligence


class Easy(Intelligence):
    """
    Easy difficulty level strategy for the AI.

    The Easy intelligence makes decisions based on the following premises:

    it will roll the dice until the turn score reaches 10, then it will choose to hold.
    """

    def decide(self, turn_score, total_score, opponent_score):
        if turn_score < 10:
            return "roll"
        else:
            return "hold"
