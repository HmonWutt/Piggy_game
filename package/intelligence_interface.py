from abc import ABC, abstractmethod

class Intelligence(ABC):
    
    @abstractmethod
    def decide(self, turn_score: int, total_score: int, opponent_score: int) -> str:
        # AI decides the next move based on: 
        # turn_score = the score for the current round
        # total_score = the total score for the current game
        # -> str = method returns a string
        pass

    