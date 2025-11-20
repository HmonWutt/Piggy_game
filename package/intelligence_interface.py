from abc import ABC, abstractmethod


class Intelligence(ABC):
    """
    Abstract base class for all AI difficulty strategies.

    Subclasses must implement decision-making logic that determines whether
    the AI should continue rolling or hold based on the game state.
    """

    @abstractmethod
    def decide(self, turn_score: int, total_score: int, opponent_score: int) -> str:
        """
        Choose the next move for the AI player.

        This method evaluates the current round score, the AI's total score,
        and the opponent's score to decide whether to keep rolling or hold.

        Parameters
        ----------
        turn_score : int
        Points earned so far in the current turn.
        total_score : int
        The AI player's total accumulated score.
        opponent_score : int
        The opponent's current total score.

        Returns
        -------
        str
            The chosen action. Expected values:
            - "roll": continue the turn
            - "hold": end the turn
        """

    pass
