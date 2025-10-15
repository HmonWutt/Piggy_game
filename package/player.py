# import dice
# import dicehand
# import highscore

""""Class for player"""
class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        # self.dicehand = dicehand()
        # self.highscore = highscore()

    # rename player
    def change_name(self, new_name: str):
        self.player_name = new_name

# 
