import json
import os
from .highscore_interface import HighScoreInterface


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
    def add_player(self, name: str):
        if name not in self.data["Players"]:
            self.data["Players"][name] = {
                "games_played": 0,
                "wins": 0,
                "highest_score": 0,
            }
            self.save_data()

    # updates player stats after a game
    def record_game(self, name: str, score: int, won: bool):
        self.add_player(name)
        player = self.data["Players"][name]
        player["games_played"] += 1
        if won:
            player["wins"] += 1
        if score > player["highest_score"]:
            player["highest_score"] = score
        self.save_data()

    # retunrs stats for a specific player and an empty dict if not found
    def get_player_stats(self, name: str) -> dict:
        return self.data["Players"].get(name, {})

    # returns stats for all players
    def get_all_players(self) -> dict:
        return self.data["Players"]
