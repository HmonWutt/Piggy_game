import cmd
import argparse
from os import wait
import shlex

from .dice import Dice
from .player import Player
from .highscore import HighScore


class Game(cmd.Cmd):
    intro = """
    ╔═══════════════════════════════════════╗
    ║         Welcome to PIG GAME!          ║
    ╚═══════════════════════════════════════╝
    
    Rules:
    - Race to 100 points to win
    - Roll dice to accumulate points in your turn
    - If you roll a 1 (in one dice game) and roll double 1s (in two-dice game), you lose all turn points and your turn ends
    - Type 'hold' to bank your turn points and pass to next player
    - Type 'pause' to pause the game
    - Type 'resume' to pick up the game from where you left off
    - Type 'help' for all commands
    
    Choose your game mode:
    - To play with a \033[1m robot \033[1m , Type 'startR --dice {1,2} --n {name} --intel {l,m,h}'.
      The robot has three intelligence levels: l:low, m: medium, h: high.
    - To play with another \033[1m human \033[1m , Type 'startH --n1 {name1} --n2 {name2} --dice {1,2}'
 
    Actions: 
    -Type 'roll' to roll 
    -Type 'hold' to pass dice to the next player
   """

    prompt = "piggame$ "

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(prog="start")
        self.player_one = None
        self.player_two = None
        self.dice = Dice()
        self.score_board = HighScore()
        self.is_paused = False
        self.number_of_dice = 0
        self.current_player = None
        self.players = []

    def do_startR(self, arg):
        """Player starts a new game against robot with args."""
        self.parser.add_argument("--dice", type=int, choices=[1, 2], default=1)
        self.parser.add_argument(
            "--intel", type=str, choices=["e", "m", "h"], default="e"
        )
        """Parse arguments."""
        try:
            args = self.parser.parse_args(shlex.split(arg))
            print(args)
            """Instantiate one human and one robot player."""
            self.player_one = Player(name)
            self.player_two = Player("Robot 🤖")
            self.start_game()
        except SystemExit as e:
            """User typed help"""
            if e.code != 0:
                print("Type 'startR --dice {1,2} --n {name} --intel {l,m,h}'")
            return

    def do_startH(self, arg):
        """Player starts a new game against another human"""

        self.parser.add_argument("--dice", type=int, choices=[1, 2], default=1)
        self.parser.add_argument("--n1", type=str, default="Player_one")
        self.parser.add_argument("--n2", type=str, default="Player_two")
        try:
            args = self.parser.parse_args(shlex.split(arg))
            self.number_of_dice = args.dice
            name1 = args.n1
            name2 = args.n2
            """Instantiate two human players"""
            self.player_one = Player(name1)
            self.player_two = Player(name2)
            self.start_game()
        except SystemExit as e:
            if e.code != 0:
                print("Type 'startH --n1 {name1} --n2 {name2} --dice {1,2}'")
            return

    def start_game(self):
        print("Game started")
        self.is_paused = False
        self.current_player = self.player_one
        self.players = [self.player_one, self.player_two]
        while not self.is_paused:
            self.show_turn()

    def do_roll(self):
        points = 0
        for i in range(self.number_of_dice):
            points += self.dice.roll()
        current_points += points
        self.current_player.set_score(current_points)

    def show_turn(self):
        """show whose turn it is and the cumulated points"""
        for player in self.players:
            if player is not self.current_player:
                self.current_player = player
        print(
            f"It's {self.current_player}'s turn. Points: {self.current_player.get_score()}"
        )

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    def do_exit(self, arg):
        """Exit the game"""
        print("Exiting the game now..")
        return True
