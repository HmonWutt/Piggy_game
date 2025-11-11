import cmd
import time
from textwrap import wrap
from InquirerPy import inquirer
import pickle
from functools import wraps


from .dice import Dice
from .player import Player
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
    - If you roll a 1, you lose all turn points and your turn ends. 
      If you roll double 1s (in two-dice game), you lose all accumulated points for the game 
      and your turn ends
          
    Actions: 
    - Type 'start' to start the game
    - Type 'help' for all commands
    - Type 'roll' to roll 
    - Type 'hold' to pass dice to the next player
    - Type 'cheat' to win the round
    - Type 'pause' to pause the game
    - Type 'resume' to resume the game
    - Type 'exit' to exit the game
    - Type 'show' to see players' statistics [COMING]

   """

    prompt = "piggame> "

    def __init__(self, is_new_game=False):
        super().__init__()
        self.is_new_game = is_new_game
        self.player_one = None
        self.player_two = None
        self.is_opponent_robot = False
        self.current_player = None
        self.dice = Dice()
        self.score_board = Score_board()
        self.number_of_dice = 0
        self.intelligence = None
        self.save_game = False
        self.is_game_in_progress = True
        self.is_game_paused = False

    def check_is_new_game(func):
        @wraps(func)
        def wrapper(self, *args):
            if self.is_new_game:
                func(self, *args)
            else:
                print("\nResuming the old game")

        return wrapper

    def check_is_game_paused(func):
        @wraps(func)
        def wrapper(self, *args):
            if not self.is_game_paused:
                func(self, *args)
            else:
                print("\nGame paused. Type 'resume' to resume game")

        return wrapper

    def check_if_active_game(func):
        @wraps(func)
        def wrapper(self, *args):
            if self.is_game_in_progress:
                func(self, *args)
            else:
                print("No active game. Type 'again' to start a new game")

        return wrapper

    def set_is_new_game(self, is_new_game):
        self.is_new_game = is_new_game

    def preloop(self):
        if not self.is_new_game:
            self.start_game()
            self.display_score_board()

    def choose_number_of_dice(self):
        num_of_dice = inquirer.select(
            message="How many dice?", choices=["1", "2"]
        ).execute()
        if num_of_dice.startswith("1"):
            return 1
        return 2

    def choose_intelligence_level(self):
        intel = inquirer.select(
            message="How smart do you want your robot friend to be?",
            choices=["Low", "Medium", "High"],
        ).execute()

        intelligence_levels = {"l": Low(), "m": Medium(), "h": High()}
        if intel.startswith("L"):
            return intelligence_levels["l"]
        elif intel.startswith("M"):
            return intelligence_levels["m"]
        return intelligence_levels["h"]

    def choose_robot_or_human(self):
        action = inquirer.select(
            message="Play with?", choices=["🦾 a robot", "💪 a human"]
        ).execute()
        if action.startswith("🦾"):
            name = input("Enter your name: ")
            self.player_one = Player(name)
            self.player_two = Player("Robot")
            self.intelligence = self.choose_intelligence_level()
            self.is_opponent_robot = True
        else:
            name1 = input("Enter player one name: ")
            name2 = input("Enter player two name: ")
            self.player_one = Player(name1)
            self.player_two = Player(name2)
        self.start_game()

    @check_is_new_game
    @check_if_active_game
    def do_start(self, arg):
        """Start a new game"""
        self.is_game_in_progress = True
        self.number_of_dice = self.choose_number_of_dice()
        self.choose_robot_or_human()

    def rolled_one(self, face, faces, turn_score, points):
        if self.count_ones(faces) == 1:
            return 1, 0, points
        elif self.count_ones(faces) == 2:
            return 1, 0, 0
        return 0, turn_score + face, face + points

    def print_rolled_one_outcome(self, num_of_ones):
        if num_of_ones == 1:
            print("Rolled a single one and lost all the points from this turn.")
        if num_of_ones == 2:
            print("Rolled double ones and lost all points from this game.")
        print("TURN ENDS.\n")

    @check_is_new_game
    def start_game(self):
        print("Game started")

        self.is_paused = False
        """Add players to the score board"""
        # self.score_board.add_player(self.player_one.name)
        self.current_player = self.player_one
        # self.score_board.add_player(self.player_two.name)
        self.is_game_in_progress = True
        Game.prompt = self.current_player.name + "> "

    def reset_player_scores(self):
        """Reset players scores"""
        self.player_two.set_score(0)
        self.player_one.set_score(0)

    def roll(self):
        face = self.dice.roll()
        graphic = self.dice.show_graphic_face()
        print(f"Dice: {face} {graphic}")
        return face

    def run_winner_found_sequence(self, winner):
        print()
        self.is_game_in_progress = False
        self.announce_winner(winner)
        self.announce_game_end()
        self.reset_player_scores()

    def choose(self):
        choice = inquirer.select(
            message="Roll or hold", choices=["Roll", "Hold"]
        ).execute()
        if choice.startswith("R"):
            return "Roll"
        return "Hold"

    @check_if_active_game
    @check_is_game_paused
    def do_play(self, arg):
        """Roll the dice"""
        faces = []
        turn_score = 0
        choice = self.choose()
        points = self.current_player.get_score()
        is_winner_found = False
        print(f"\n{self.current_player.name}'s total points: {points}")
        while not choice.startswith("H"):
            face = self.roll()
            faces.append(face)
            num_of_ones_rolled, turn_score, points = self.rolled_one(
                face, faces, turn_score, points
            )

            if num_of_ones_rolled > 0:
                self.print_rolled_one_outcome(num_of_ones_rolled)
                self.switch_current_player()
                break
            print(f"Total points: {points}, Round total: {turn_score}")
            self.current_player.set_score(points)
            is_winner_found, winner = self.check_if_winner_found()

            if is_winner_found:
                self.run_winner_found_sequence(winner)
                break
            choice = self.choose()
        if not is_winner_found:
            if not self.is_opponent_robot:
                self.switch_current_player()
            else:
                print(f"\nRobot coming up with a strategy...")
                time.sleep(1)
                self.auto_play()

    @check_is_game_paused
    def auto_play(self):
        points = self.player_two.get_score()
        print(f"Robot's points: {points}")
        turn_score = 0
        faces = []
        """opponent's score is set to 0 for now as it is not used"""
        action = self.intelligence.decide(points, turn_score, 0)
        while action != "hold":
            print(f"Robots action: {action}")
            face = self.roll()
            faces.append(face)
            num_ones_rolled, turn_score, points = self.rolled_one(
                face, faces, turn_score, points
            )

            if num_ones_rolled > 0:
                self.print_rolled_one_outcome(num_ones_rolled)
                self.pass_to_human()
                break
            print(f"Total points: {points}, Round total: {turn_score}")
            is_winner_found, winner = self.check_if_winner_found()
            if is_winner_found:
                self.run_winner_found_sequence(winner)
                break
            self.player_two.set_score(points)
            action = self.intelligence.decide(points, turn_score, 0)

        if action == "hold":
            print(f"Robots action: {action}\n")
        self.pass_to_human()

    def hold(self):
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

    def switch_current_player(self):
        if self.player_one is not self.current_player:
            self.current_player = self.player_one
        else:
            self.current_player = self.player_two
        self.is_player_switched = True
        Game.prompt = self.current_player.name + "> "

    def pass_to_human(self):
        """Do nothing just print that it's human's turn now"""
        self.current_player = self.player_one
        Game.prompt = self.player_one.name + "> "

    def display_score_board(self):
        """Display score board. To add info from saved file once it has been fixed"""
        # info = self.score_board.get_all_players()
        info = {
            self.player_one.name: self.player_one.get_score(),
            self.player_two.name: self.player_two.get_score(),
        }
        banner = """
    ╔═══════════════════════════════════════╗
    ║           Game statistics!            ║
    ╚═══════════════════════════════════════╝

    """
        Utils.print_dict_table(info, banner)

    def check_if_winner_found(self):
        if self.player_one.get_score() >= 100:
            return True, self.player_one
        elif self.player_two.get_score() >= 100:
            return True, self.player_two
        return False, None

    def count_ones(self, faces):
        count = faces.count(1)
        return count

    def announce_winner(self, player):
        print(f"{player.name} has won. Congrats🎉")

    def lose_points_from_game(self, player):
        player.set_score(0)
        print(f"Oh no! {player.name} rolled double ones and lost all points. ")

    def lost_points_from_turn(self, player):
        print(f"Oh no! {player.name} rolled a one and lost all points from this turn.")

    def announce_game_end(self):
        print("\nGAME OVER!. Type 'again' to play another game")
        Game.prompt = "piggygame> "

    @check_is_game_paused
    def do_again(self, arg):
        """Play a new game"""
        if not self.is_game_in_progress:
            self.reset_player_scores()
            self.start_game()

    @check_if_active_game
    @check_is_game_paused
    def do_cheat(self, arg):
        """Cheat to win"""
        self.current_player.set_score(100)
        is_winner_found, winner = self.check_if_winner_found()
        if is_winner_found:
            self.run_winner_found_sequence(winner)

    @check_if_active_game
    def do_pause(self, arg):
        """Save game data to file and pause the game"""
        # self.save_game()
        self.is_game_paused = True
        print("Game paused. Type 'resume' to resume game\n")
        Game.prompt = "piggygame> "

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    @check_if_active_game
    def do_resume(self, arg):
        """Resuming game"""
        self.is_paused = False
        self.display_score_board()
        Game.prompt = self.current_player.name + "> "

    @check_if_active_game
    @check_is_game_paused
    def do_namechange(self, arg):
        """Change your username"""
        new_name = input("Enter your new name: ")
        self.current_player.name = new_name
        print(f"\nYou have changed your name to {self.current_player.name}.\n")
        Game.prompt = self.current_player.name + "> "

    def do_exit(self, arg):
        """Exit the game"""
        choice = inquirer.select(
            message="Save the game to resume later?",
            choices=["✔️ Yes", "❌No"],
        ).execute()
        if choice.startswith("✔️ Yes"):
            self.save_game = True
        else:
            self.save_game = False
            print("Game exited without saving.")
        self.is_game_in_progress = False

        return True

    def __getstate__(self):
        """Added this to solve "can't pickle TextIOwrapper" error when pickling"""
        """Copy instance dictionary"""
        state = self.__dict__.copy()

        """Remove unpickleable cmd.Cmd attributes"""
        for key in ("stdin", "stdout", "stderr"):
            if key in state:
                del state[key]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        import sys

        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def postloop(self):
        if self.save_game:
            """Save the whole object to a pickle file"""
            with open("game_state.pkl", "wb") as f:
                pickle.dump(self, f)
                print("Game saved. Good bye!")
