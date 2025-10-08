import cmd
from game import Game
from dice import Dice
# game = Game()
# game.cmdloop()
dice = Dice()
for _ in range(10):
    dice.roll()
    print(dice.face)
