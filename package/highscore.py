import json
import os
from .highscore_interface import HighScoreInterface
from .player import Player


class HighScore(HighScoreInterface):
    # initializing HighScore with json file path
    def __init__(self, filepath="data/highscores.json"):
        self.filepath = filepath
        self.data = {"Players": {}}
        self.load_data()

    # loads data from the json file or creates it if it doesnt exist
    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        else:
            self.save_data()  # creates empty file it it doesnt exists

    # saves the current data to the json file
    def save_data(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    # adds a new player if it doesnt already exist in the json file
    def add_player(self, player):
        name = player.name
        if name not in self.data["Players"]:
            self.data["Players"][name] = {
                "games_played": 0,
                "wins": 0,
                "highest_score": 0,
            }

    # updates player stats after a match
    def record_game(self, player1, player2, winner):
        self.add_player(player1)
        self.add_player(player2)

        for player in (player1, player2):
            name = player.name
            stats = self.data["Players"][name]
            stats["games_played"] += 1

            if player is winner:
                stats["wins"] += 1
            
            if player.get_score() > stats["highest_score"]:
                stats["highest_score"] = player.get_score()
        
        self.save_data()

    # retunrs stats for a specific player and an empty dict if not found
    def get_player_stats(self, name: str) -> dict:
        return self.data["Players"].get(name, {})

    # returns stats for all players
    def get_all_players(self) -> dict:
        return self.data["Players"]
