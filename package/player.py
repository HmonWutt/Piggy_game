"""Class for player."""

# import dice
# import dicehand
# import highscore


class Player:
    """Represent a player."""

    def __init__(self, player_name):
        """Set the name and score of a player."""
        self.name = player_name
        # self.dicehand = dicehand()
        self.score = 0

    def change_name(self, new_name: str):
        """Rename a player."""
        self.name = new_name

    def get_name(self):
        """Get name of a player."""
        return self.name

    def set_score(self, score):
        """Set the score for a player."""
        self.score = score

    def get_score(self):
        """Get the score for a player."""
        return self.score
