from abc import ABC, abstractmethod


class Player_interface(AB):
    @property
    @abstractmethod
    def name(self, name: str) -> str:
        """Player's name"""
        pass

    @property
    @abstractmethod
    def total_score(self) -> int:
        """Player's total score so far"""
        pass

    @abstractmethod
    def change_name(self, name: str) -> None:
        """Change player's name"""
        pass

    @abstractmethod
    def play(self) -> None:
        """Human player plays or robot plays using any of the intelligence level chosen"""
        pass
