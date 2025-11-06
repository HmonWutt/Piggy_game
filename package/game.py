import cmd
import argparse
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
        self.intelligence_levels = {"l": Low(), "m": Medium(), "h": High()}

    def do_startR(self, arg):
        """Player starts a new game against robot with args."""
        self.is_opponent_robot = True
        self.parser.add_argument("--dice", type=int, choices=[1, 2], default=1)
        self.parser.add_argument("--name", type=str, default="Player_one")

        self.parser.add_argument(
            "--intel", type=str, choices=["l", "m", "h"], default="l"
        )
        """Parse arguments."""
        try:
            args = self.parser.parse_args(shlex.split(arg))
            """Instantiate one human and one robot player."""
            self.player_one = Player(args.name)
            self.player_two = Player("Robot 🤖")
            self.number_of_dice = args.dice
            self.intelligence = self.intelligence_levels[args.intel]
            print(f"Intelligence level chosen: {type(self.intelligence).__name__}")
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
        """Roll the dice"""
        if not self.is_paused:
            points = self.current_player.get_score()
            faces = []
            turn_score = 0
            face = 0
            """currently rolls both dices in a row. Will edit later to allow the user to roll one by one"""
            for i in range(self.number_of_dice):
                face = self.dice.roll()
                graphic = self.dice.show_graphic_face()
                print(f"Dice {i + 1}: {face} {graphic}")
                is_one = face == 1
                faces.append(is_one)
                turn_score += face

            if self.check_if_one_rolled(faces) < 1:
                self.current_player.set_score(turn_score + points)
            elif self.check_if_one_rolled(faces) == 1:
                self.lost_points_from_turn(self.current_player)
            elif self.check_if_one_rolled(faces) == 2:
                self.lose_points_from_game(self.current_player)
            else:
                pass
            self.check_if_round_end()
            if not self.is_round_over:
                updated_points = self.current_player.get_score()
                print(f"{self.current_player.player_name}'s points: {updated_points}")
                self.show_turn()
            else:
                self.announe_winner(self.current_player)
        else:
            print("game paused. type resume to continue playing\n")

    def do_hold(self, arg):
        """Turn ends and pass to opponent"""
        if not self.is_paused:
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
        else:
            self.switch_current_player()
            self.print_whose_turn_it_is_now(self.current_player)

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
        Game.prompt = self.player_one.player_name + ": "
        self.print_whose_turn_it_is_now(self.player_one)

    def auto_play(self):
        if not self.is_paused:
            self.print_whose_turn_it_is_now(self.player_two)
            points = self.player_two.get_score()
            temp_total_points = points
            faces = []
            turn_score = 0
            face = 0
            for i in range(self.number_of_dice):
                """opponent's score is set to 0 for now as it is not used"""
                action = self.intelligence.decide(temp_total_points, turn_score, 0)
                print(f"Robots action: {action}")
                if action == "hold":
                    break
                face = self.dice.roll()
                is_one = face == 1
                faces.append(is_one)
                turn_score += face
                temp_total_points += face
                graphic = self.dice.show_graphic_face()
                print(f"Dice {i + 1}: {face} {graphic}")

            if self.check_if_one_rolled(faces) < 1:
                self.player_two.set_score(turn_score + points)
            elif self.check_if_one_rolled(faces) == 1:
                self.lost_points_from_turn(self.player_two)
            elif self.check_if_one_rolled(faces) == 2:
                self.lose_points_from_game(self.player_two)
            self.check_if_round_end()
            if not self.is_round_over:
                print(f"Robots total points: {self.player_two.get_score()}")
                self.pass_to_human()
                Game.prompt = self.current_player.player_name + "$ "
            else:
                self.announe_winner(self.player_two)

    def display_score_board(self):
        """Display score board. To add info from saved file once it has been fixed"""
        # info = self.score_board.get_all_players()
        info = {
            self.player_one.player_name: self.player_one.get_score(),
            self.player_two.player_name: self.player_two.get_score(),
        }
        banner = """
    ╔═══════════════════════════════════════╗
    ║           Game statistics!            ║
    ╚═══════════════════════════════════════╝

    """
        Utils.print_dict_table(info, banner)

    def check_if_round_end(self):
        if self.player_one.get_score() >= 100 or self.player_two.get_score() >= 100:
            """Reset players scores"""
            self.player_two.set_score(0)
            self.player_one.set_score(0)
            self.is_round_over = True
            self.announce_round_end()

    def check_if_one_rolled(self, faces):
        if len(faces) > 1:
            if all(faces):
                return 2
            if faces[0] or faces[1]:
                return 1
        elif len(faces) == 1 and all(faces):
            return 1
        return 0

    def announe_winner(self, player):
        print(f"{player.player_name} has won. Congrats🎉")

    def lose_points_from_game(self, player):
        player.set_score(0)
        print(f"Oh no! {player.player_name} rolled double ones and lost all points. ")

    def lost_points_from_turn(self, player):
        print(
            f"Oh no! {player.player_name} rolled a one and lost all points from this turn."
        )

    def announce_round_end(self):
        print("Round over. Type 'again' to play another game")
        Game.prompt = "piggygame$ "

    def do_again(self, arg):
        """Play a new game"""
        if not self.is_paused:
            if self.is_round_over:
                self.is_round_over = False
                self.current_player = self.player_one
                self.display_score_board()
                self.print_whose_turn_it_is_now(self.current_player)
                Game.prompt = f"{self.current_player.player_name}$ "
            else:
                print("Can't start a new game while current game is in progress")

        else:
            print("game paused. type resume to continue playing\n")

    def do_cheat(self, arg):
        """Cheat to win"""
        if not self.is_paused:
            self.player_one.set_score(100)
            self.announe_winner(self.player_one)
            self.check_if_round_end()
        else:
            print("game paused. type resume to continue playing\n")

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
