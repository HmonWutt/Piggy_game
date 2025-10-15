from abc import ABC, abstractmethod


class HighScoreInterface(ABC):

    # adds a new player to the high svcore list
    @abstractmethod
    def add_player(self, name: str):
        pass

    # records a finished game for a player (its name, score and wins)
    @abstractmethod
    def record_game(self, name: str, score: int, won: bool):
        pass

    # returns stats for a specifc player
    @abstractmethod
    def get_player_stats(self, name: str) -> dict:
        pass

    # resturns stats for all players
    @abstractmethod
    def get_all_players(self) -> dict:
        pass
