# import dice
# import dicehand
# import highscore

""" "Class for player"""


class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        # self.dicehand = dicehand()
        self.score = 0

    # rename player
    def change_name(self):
        self.player_name = input("Enter your new name: ")

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
