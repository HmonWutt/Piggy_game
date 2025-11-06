import cmd
import argparse
from os import wait
import shlex


from .dice import Dice
from .player import Player
from .highscore import HighScore
from .intelligence_easy import Easy as Low
from .intelligence_medium import Medium
from .intelligence_hard import Hard as High
from .highscore import HighScore as Score_board
from utils import Utils


class Game(cmd.Cmd):
    intro = """
    ╔═══════════════════════════════════════╗
    ║         Welcome to PIG GAME!          ║
    ╚═══════════════════════════════════════╝
    
    Rules:
    - Race to 100 points to win
    - Roll dice to accumulate points in your turn
    - If you roll a 1 (in one dice game) and roll double 1s (in two-dice game), you lose all turn points and your turn ends
          
    Choose your game mode:
    - To play with a \033[1mrobot\033[0m, Type 'startR --dice {1,2} --n {name} --intel {l,m,h}'.
      The robot has three intelligence levels: l:low, m: medium, h: high.
    - To play with another \033[1mhuman\033[0m, Type 'startH --n1 {name1} --n2 {name2} --dice {1,2}'
 
    Actions: 
    - Type 'help' for all commands
    - Type 'roll' to roll 
    - Type 'hold' to pass dice to the next player
    - Type 'cheat' to win the round
    - Type 'surrender' to lose and end the round
    - Type 'pause' to pause the game
    - Type 'resume' to resume the game
    - Type 'exit' to exit the game
    - Type 'show' to see players' statistics [COMING]

   """

    prompt = "piggame$ "

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(prog="start")
        self.player_one = None
        self.player_two = None
        self.dice = Dice()
        self.score_board = Score_board()
        self.is_round_over = False
        self.is_paused = False
        self.number_of_dice = 0
        self.current_player = None
        self.intelligence = ""
        self.is_opponent_robot = False
        low = Low()
        medium = Medium()
        high = High()
        self.intelligence_levels = {"l": low, "m": medium, "h": high}

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
            self.intelligence = self.intelligence_levels[args.intel]
            self.start_game()
        except SystemExit as e:
            """User typed help"""
            if e.code != 0:
                print("Type 'startR --dice {1,2} --n {name} --intel {l,m,h}'\n")
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
                print("Type 'startH --n1 {name1} --n2 {name2} --dice {1,2}'\n")
            return

    def start_game(self):
        print("Game started")
        self.is_paused = False
        """Player one will be the first to play"""
        self.current_player = self.player_one
        """Add players to the score board"""
        self.score_board.add_player(self.player_one.player_name)
        self.score_board.add_player(self.player_two.player_name)
        self.display_score_board()
        self.print_whose_turn_it_is_now(self.current_player)
        Game.prompt = self.current_player.player_name + "$ "

    def do_roll(self, arg):
        if not self.is_paused:
            points = 0
            current_points = self.current_player.get_score()
            """currently rolls both dices in a row. Will edit later to allow the user to roll one by one"""
            for i in range(self.number_of_dice):
                face = self.dice.roll()
                points += face
            current_points += points
            self.current_player.set_score(current_points)
            updated_points = self.current_player.get_score()
            print(f"{self.current_player.player_name}'s points: {updated_points}")
            self.show_turn()
        else:
            print("game paused. type resume to continue playing\n")

    def do_hold(self, arg):
        if not self.is_paused:
            """Turn ends and pass to opponent"""
            self.show_turn()
        else:
            print("game paused. type resume to continue playing\n")

    def save_game(self, name, score, is_winner):
        """Save points before passing to opponent"""
        self.score_board.record_game(name, score, is_winner)

    def show_turn(self):
        """Robot auto_play and pass back to human"""
        if self.is_opponent_robot:
            self.auto_play()
            if not self.is_round_over:
                self.pass_to_human()
                Game.prompt = self.current_player.player_name + "$ "

        else:
            self.switch_current_player()
            self.print_whose_turn_it_is_now(self.current_player)
            self.decide_winner()

    def print_whose_turn_it_is_now(self, player):
        print(f"\nIt's {player.player_name}'s turn. Points: {player.get_score()}")

    def switch_current_player(self):
        if self.player_one is not self.current_player:
            self.current_player = self.player_one
        else:
            self.current_player = self.player_two
        Game.prompt = self.current_player.player_name + "$ "

    def pass_to_human(self):
        """Do nothing just print that it's human's turn now"""
        prompt = self.player_one.player_name + ": "
        self.print_whose_turn_it_is_now(self.player_one)

    def auto_play(self):
        if not self.is_paused:
            self.print_whose_turn_it_is_now(self.player_two)
            action = "roll"
            points = self.player_two.get_score()
            while action == "roll" and not self.is_round_over:
                for _ in range(self.number_of_dice):
                    turn_score = self.dice.roll()
                    points += turn_score
                    self.player_two.set_score(points)
                    """opponent's score is set to 0 for now as it is not used"""
                    action = self.intelligence.decide(
                        self.player_two.get_score(), turn_score, 0
                    )
                    self.decide_winner()
                    if action == "hold" or self.is_round_over:
                        break

            print(f"Robots total points: {self.player_two.get_score()}")
            self.decide_winner()

    def display_score_board(self):
        """Display score board"""
        info = self.score_board.get_all_players()
        banner = """
    ╔═══════════════════════════════════════╗
    ║           Game statistics!            ║
    ╚═══════════════════════════════════════╝

    """
        Utils.print_dict_table(info, banner)

    def decide_winner(self):
        if not self.is_round_over:
            one_player_reached_100 = (
                self.player_one.get_score() >= 100 or self.player_two.get_score() >= 100
            )
            one_player_rolled_one = (
                self.player_one.get_score() == 1 or self.player_two.get_score() == 1
            )
            self.is_round_over = one_player_reached_100 or one_player_rolled_one
        else:
            print("Round over. Type 'again' to play another game")
            self.display_score_board()
            Game.prompt = "piggygame$ "

    def do_again(self, arg):
        """Reset players scores"""
        self.player_two.set_score(0)
        self.player_one.set_score(0)
        self.is_round_over = False
        self.current_player = self.player_one
        self.print_whose_turn_it_is_now(self.current_player)
        Game.prompt = f"{self.current_player.player_name}$ "

    def do_cheat(self, arg):
        """Cheat to win"""
        self.player_one.set_score(100)
        self.is_round_over = True
        self.decide_winner()

    def do_surrender(self, arg):
        """Surrender and end this round"""
        self.player_one.set_score(1)
        self.is_round_over = True
        self.decide_winner()

    def do_pause(self, arg):
        """Save game data to file and pause the game"""
        # self.save_game()
        self.is_paused = True
        print("Game paused. Type 'resume' to resume game\n")
        Game.prompt = "piggygame$ "

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    def do_resume(self, arg):
        """Resuming game"""
        self.is_paused = False
        self.display_score_board()
        self.print_whose_turn_it_is_now(self.current_player)
        Game.prompt = self.current_player.player_name + "$ "

    def do_exit(self, arg):
        """Exit the game"""
        print("Exiting the game now..")
        return True
