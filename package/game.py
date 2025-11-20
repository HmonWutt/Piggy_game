import cmd
import pickle
import time

from InquirerPy import inquirer

from .dice import Dice
from .highscore import HighScore
from .histogram import Histogram
from .intelligence_easy import Easy as Low
from .intelligence_hard import Hard as High
from .intelligence_medium import Medium
from .player import Player
from .utils import Utils


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
    - Type 'start' to start a game
    - Type 'changename' to change your name
    - Type 'help' for all commands
    - Type 'play' to play
    - Type 'cheat' to win the round
    - Type 'pause' to pause the game
    - Type 'unpause' to resume the game
    - Type 'show' to see the leaderboard
    - Type 'exit' to exit the game

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
        self.score_record = HighScore()
        self.number_of_dice = 0
        self.intelligence = None
        self.save_game = False
        self.is_game_in_progress = False
        self.is_game_paused = False

    def check_is_new_game(func):
        """Check if the game new or restored from a previous game."""

        def wrapper(self, *args):
            if self.is_new_game:
                func(self, *args)
            else:
                print("\nResuming the old game")

        return wrapper

    def check_is_game_paused(func):
        """If the game is paused, disable all actions except
        'exit' and 'unpause' and
        prompt user to type 'unpause' to unpause the game"""

        def wrapper(self, *args):
            if not self.is_game_paused:
                func(self, *args)
            else:
                print("\nGame paused. Type 'unpause' to resume game")

        return wrapper

    def check_is_active_game(func):
        """Check if there is a game in progress.
        If a game is in progress,
        the 'start' action will be disabled
        to disallow players from starting a new game
        while current game is in progress.
        If there is no game in progress, all actions
        except 'start' and 'again' will be disabled
        since players can't do game play actions
        while there is no active game"""

        def wrapper(self, *args):
            if self.is_game_in_progress:
                func(self, *args)
            else:
                print("No active game. Type 'start' to start a new game")

        return wrapper

    def set_is_new_game(self, is_new_game):
        """Set if this is a new game or restored from the saved game"""
        self.is_new_game = is_new_game

    def preloop(self):
        """This wil run before the game loop begins,
        and start the game right away
        if the properties are restored from the saved game.
        If not this will be skipped and players will be asked
        to add game settings such as the number of die,
        player names etc."""
        if not self.is_new_game:
            self.start_game()
            self.display_score_board()

    def choose_number_of_dice(self):
        """Choose if one or two dice"""
        num_of_dice = inquirer.select(
            message="How many dice?", choices=["1", "2"]
        ).execute()
        if num_of_dice.startswith("1"):
            return 1
        return 2

    def choose_robot_or_human(self):
        """Player chooses if they want to play with a robot or a human"""
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

    def choose_intelligence_level(self):
        """Choose the IQ of the robot"""
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

    @check_is_new_game
    def do_start(self, arg):
        if self.is_game_in_progress:
            print("Can't start a game while there is one in progress")
            return
        self.is_game_in_progress = True
        """Start the game"""
        self.number_of_dice = self.choose_number_of_dice()
        self.choose_robot_or_human()

    def start_game(self):
        """Game starts or resumes"""
        print("Game started")
        self.is_paused = False
        self.current_player = self.player_one
        self.is_game_in_progress = True
        Game.prompt = self.current_player.get_name() + "> "

    @check_is_active_game
    @check_is_game_paused
    def do_play(self, arg):
        turn_score = 0
        """Play. You will be asked to choose to roll or hold"""
        points = self.current_player.get_score()

        print(
            f"\n{
                self.current_player.get_name()}'s total points: {points}, Round total: {turn_score}"
        )

        choice = self.choose_roll_or_hold()
        is_winner_found = False
        while not choice.startswith("H"):
            result, result_list = self.roll()
            num_of_ones_rolled = self.count_ones(result_list)

            if num_of_ones_rolled == 0:
                turn_score += result
            else:
                if num_of_ones_rolled == 2:
                    points = 0
                turn_score = 0
                self.print_rolled_one_outcome(num_of_ones_rolled)
                break
            print(
                f"Total points: {
                    points +
                    turn_score}, Round total: {turn_score}")
            if points + turn_score >= 100:
                points = 0
                turn_score = 0
                self.run_winner_found_sequence(self.current_player)
                is_winner_found = True
                break
            choice = self.choose_roll_or_hold()

        self.current_player.set_score(points + turn_score)
        if not is_winner_found:
            if not self.is_opponent_robot:
                print()
                self.switch_current_player()
            else:
                print("\nRobot coming up with a strategy...")
                time.sleep(1)
                self.auto_play()

    @check_is_game_paused
    def auto_play(self):
        """Robot plays"""
        points = self.player_two.get_score()
        turn_score = 0
        print(f"Robot's total points: {points}, Round total: {turn_score}")
        """opponent's score is set to 0 for now as it is not used"""
        action = self.intelligence.decide(turn_score, points, 0)
        is_winner_found = False
        while action != "hold":
            print(f"Robots action: {action}")
            result, result_list = self.roll()

            num_ones_rolled = self.count_ones(result_list)
            if num_ones_rolled == 0:
                turn_score += result
            else:
                if num_ones_rolled == 2:
                    points = 0
                turn_score = 0
                self.print_rolled_one_outcome(num_ones_rolled)
                break
            if points + turn_score >= 100:
                points = 0
                turn_score = 0
                self.run_winner_found_sequence(self.player_two)
                is_winner_found = True
                break
            print(
                f"Total points: {
                    points +
                    turn_score}, Round total: {turn_score}.\n")
            action = self.intelligence.decide(turn_score, points, 0)
        if action == "hold":
            print(f"Robots action: {action}\n")
        self.player_two.set_score(turn_score + points)
        if not is_winner_found:
            self.pass_to_human()

    def choose_roll_or_hold(self):
        """Human chooses to roll the dice or hold"""
        choice = inquirer.select(
            message="Roll or hold", choices=["Roll", "Hold"]
        ).execute()
        if choice.startswith("R"):
            return "Roll"
        return "Hold"

    def roll(self):
        """Roll the dice once or twice depending on how many dice there are"""
        result_list = []
        result = 0
        print("Dice: ", end="")
        for i in range(self.number_of_dice):
            face = self.dice.roll()
            result += face
            result_list.append(face)
            graphic = self.dice.show_graphic_face()
            print(f"{graphic} ({face}) ", end="")
        print()
        return result, result_list

    def count_ones(self, faces):
        """Count the number of ones in the list "faces"""
        count = faces.count(1)
        return count

    def print_rolled_one_outcome(self, num_of_ones):
        """Check how many ones have been rolled this round to decide if the player had lost
        points from this round, points from this game, or no points at all"""
        if num_of_ones == 1:
            print("Rolled a single one and lost all the points from this turn.")
        if num_of_ones == 2:
            print("Rolled double ones and lost all points from this game.")
        print("TURN ENDS.\n")

    def switch_current_player(self):
        """Set current player to the other player when current player's turn ends.
        Change name in prompt"""
        if self.player_one is self.current_player:
            self.current_player = self.player_two
        else:
            self.current_player = self.player_one
        Game.prompt = self.current_player.get_name() + "> "

    def pass_to_human(self):
        """Change current player to human. Change name in prompt"""
        self.current_player = self.player_one
        Game.prompt = self.player_one.get_name() + "> "

    def run_winner_found_sequence(self, winner):
        """Set that there is no active game;
        Announce winner;
        Announce that game ended;
        save the game to json file;
        reset player points to zero"""
        print()
        self.is_game_in_progress = False
        self.announce_winner(winner)
        self.announce_game_end()
        self.score_record.record_game(self.player_one, self.player_two, winner)
        self.reset_player_scores()

    def reset_player_scores(self):
        """Reset players scores"""
        self.player_two.set_score(0)
        self.player_one.set_score(0)

    def display_score_board(self):
        """Display in game score board."""
        info = {
            self.player_one.get_name(): self.player_one.get_score(),
            self.player_two.get_name(): self.player_two.get_score(),
        }
        banner = """
    ╔═══════════════════════════════════════╗
    ║           Game statistics!            ║
    ╚═══════════════════════════════════════╝

    """
        Utils.print_dict_table(info, banner)

    def announce_winner(self, player):
        print(f"{player.get_name()} has won. Congrats🎉")

    def announce_game_end(self):
        print("\nGAME OVER!. Type 'start' to play another game")
        Game.prompt = "piggygame> "

    @check_is_active_game
    @check_is_game_paused
    def do_cheat(self, arg):
        """Cheat to win"""
        self.current_player.set_score(100)
        self.run_winner_found_sequence(self.current_player)

    @check_is_active_game
    def do_pause(self, arg):
        """Save game data to file and pause the game"""
        # self.save_game()
        self.is_game_paused = True
        print("Game paused. Type 'unpause' to resume game\n")
        Game.prompt = "piggygame> "

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    @check_is_active_game
    def do_unpause(self, arg):
        """Unpause the game"""
        self.is_paused = False
        self.display_score_board()
        Game.prompt = self.current_player.name + "> "

    @check_is_active_game
    @check_is_game_paused
    def do_changename(self, arg):
        """Change your username"""
        old_name = self.current_player.get_name()
        new_name = input("Enter your new name: ")
        self.current_player.change_name(new_name)
        print(
            f"\nYou have changed your name to {
                self.current_player.get_name()}.\n")
        self.score_record.update_player_name(old_name, new_name)
        Game.prompt = self.current_player.get_name() + "> "

    def do_show(self, arg):
        """Show statistics"""
        choice = inquirer.select(
            message="What would you like to see?",
            choices=["Leaderboard", "Player names"],
        ).execute()
        stats = Histogram(self.score_record)
        if choice.startswith("L"):
            stats.display_wins()
        else:
            stats.display_games_played()

    def do_exit(self, arg):
        """Exit the game"""
        choice = inquirer.select(
            message="Save the game to resume later?",
            choices=["✔️ Yes", "❌No"],
        ).execute()
        if choice.startswith("✔️ Yes"):
            self.save_game = True
            self.is_new_game = False
        else:
            self.save_game = False
            print("Game exited without saving.")
        self.is_game_in_progress = False

        return True

    def __getstate__(self):
        """Added this to solve "can't pickle
        TextIOwrapper" error when pickling"""
        """Copy instance dictionary"""
        state = self.__dict__.copy()

        """Remove unpickleable cmd.Cmd attributes"""
        for key in ("stdin", "stdout", "stderr"):
            if key in state:
                del state[key]
        return state

    def __setstate__(self, state):
        """Added this to solve "can't pickle
        TextIOwrapper" error when pickling"""
        self.__dict__.update(state)
        import sys

        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def postloop(self):
        if self.save_game:
            """Pickle the whole game object"""
            with open("game_state.pkl", "wb") as f:
                pickle.dump(self, f)
                print("Game saved. Good bye!")
