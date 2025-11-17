""" The interface for the HighScore class. """

from abc import ABC, abstractmethod
from .player import Player


class HighScoreInterface(ABC):
    """ Interface for HighScore class. """

    @abstractmethod
    def add_player(self, player: Player):
        """ Adds a new player to the high score list. """
        pass

    @abstractmethod
    def record_game(self, player1: Player, player2: Player, winner: Player):
        """ Records a finished match. """
        pass

    @abstractmethod
    def get_player_stats(self, name: str) -> dict:
        """ Returns stats for a specifc player. """
        pass

    @abstractmethod
    def get_all_players(self) -> dict:
        """ Returns stats for all players. """
        pass
