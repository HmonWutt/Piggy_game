import cmd
import argparse
from os import wait
import shlex

from package import intelligence

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
        self.intelligence = ""
        self.is_opponent_robot = False
        # low = Low()
        # medium = Medium()
        # high = High()
        # self.intelligence_levels = {l: low,m:medium,h:high]
        self.intelligence_levels = ["low", "medium", "high"]

    def do_startR(self, arg):
        """Player starts a new game against robot with args."""
        self.is_opponent_robot = True
        self.parser.add_argument("--dice", type=int, choices=[1, 2], default=1)
        self.parser.add_argument("--name", type=str, default="Player_one")

        self.parser.add_argument(
            "--intel", type=str, choices=["l", "m", "h"], default="e"
        )
        """Parse arguments."""
        try:
            args = self.parser.parse_args(shlex.split(arg))
            """Instantiate one human and one robot player."""
            self.player_one = Player(args.name)
            self.player_two = Player("Robot 🤖")
            self.number_of_dice = args.dice
            self.intelligence = args.intel
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
        print(
            f"It's {self.current_player.player_name}'s turn. Points: {self.current_player.get_score()}"
        )

    def do_roll(self, arg):
        points = 0
        current_points = self.current_player.get_score()
        for i in range(self.number_of_dice):
            self.dice.roll()
            points += self.dice.face
        current_points += points
        self.current_player.set_score(current_points)
        updated_points = self.current_player.get_score()
        print(f"{self.current_player.player_name}'s points: {updated_points}")
        self.show_turn()

    def show_turn(self):
        """show whose turn it is and the cumulated points"""
        if self.is_opponent_robot:
            print(
                f"It's {self.player_two.player_name}'s turn. Points: {self.player_two.get_score()}"
            )
            self.auto_play()
            self.pass_to_human()
        else:
            self.switch_current_player()

    def switch_current_player(self):
        if self.player_one is not self.current_player:
            self.current_player = self.player_one
        else:
            self.current_player = self.player_two

        print(
            f"It's {self.current_player.player_name}'s turn. Points: {self.current_player.get_score()}"
        )

    def pass_to_human(self):
        print(
            f"It's {self.current_player.player_name}'s turn. Points: {self.current_player.get_score()}"
        )

    def auto_play(self):
        """to implement with intelligence class later"""
        print(f"Played with {self.intelligence} intelligence and earned 3 points")

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    def do_exit(self, arg):
        """Exit the game"""
        print("Exiting the game now..")
        return True
