"""
Defines the Medium AI difficulty strategy for the Piggy Game.

This module contains the Medium class, implementing a strategy for the AI.
The Medium intelligence rolls the
dice until the turn score reaches 20, then it will hold.
"""

from .intelligence_interface import Intelligence


class Medium(Intelligence):
    """
    Medium difficulty level strategy for the AI.

    The Medium intelligence makes decisions based on the following premises:
    it will roll the dice until the turn score reaches 20, then it will
    choose to hold.
    """

    def decide(self, turn_score, total_score, opponent_score):
        """Decide to roll or hold."""
        if turn_score < 20:
            return "roll"
        else:
            return "hold"
