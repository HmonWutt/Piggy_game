from abc import ABC, abstractmethod
from .player import Player


class HighScoreInterface(ABC):

    # adds a new player to the high svcore list
    @abstractmethod
    def add_player(self, player: Player):
        pass

    # records a finished match
    @abstractmethod
    def record_game(self, player1: Player, player2: Player, winner: Player):
        pass

    # returns stats for a specifc player
    @abstractmethod
    def get_player_stats(self, name: str) -> dict:
        pass

    # resturns stats for all players
    @abstractmethod
    def get_all_players(self) -> dict:
        pass
