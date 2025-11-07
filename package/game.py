import cmd
from InquirerPy import inquirer
import pickle


from .dice import Dice
from .player import Player
from .intelligence_easy import Easy as Low
from .intelligence_medium import Medium
from .intelligence_hard import Hard as High

# from .highscore import HighScore as Score_board
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

    def __init__(self, is_new=False):
        super().__init__()
        self.is_new = is_new
        self.player_one = None
        self.player_two = None
        self.is_opponent_robot = False
        self.current_player = None
        self.dice = Dice()
        # self.score_board = Score_board()
        self.is_round_over = False
        self.number_of_dice = 0
        self.intelligence_levels = {"l": Low(), "m": Medium(), "h": High()}
        self.intelligence = None
        self.save_game = False

    def set_is_new(self, is_new):
        self.is_new = is_new

    def preloop(self):
        if not self.is_new:
            self.start_game()
            self.display_score_board()

    def do_start(self, arg):
        if self.is_new:
            """Start a new game"""
            num_of_dice = inquirer.select(
                message="How many dice?", choices=["1", "2"]
            ).execute()
            if num_of_dice.startswith("1"):
                self.number_of_dice = 1
            else:
                self.number_of_dice = 2

            action = inquirer.select(
                message="Play with?", choices=["🦾 a robot", "💪 a human"]
            ).execute()
            if action.startswith("🦾"):
                name = input("Enter your name: ")
                self.player_one = Player(name)
                self.player_two = Player("Robot")
                self.is_opponent_robot = True

                intel = inquirer.select(
                    message="How smart do you want your robot friend to be?",
                    choices=["Low", "Medium", "High"],
                ).execute()
                if intel.startswith("L"):
                    self.intelligence = self.intelligence_levels["l"]
                elif intel.startswith("M"):
                    self.intelligence = self.intelligence_levels["m"]
                else:
                    self.intelligence = self.intelligence_levels["h"]
            else:
                name1 = input("Enter player one name: ")
                name2 = input("Enter player two name: ")
                self.player_one = Player(name1)
                self.player_two = Player(name2)
            self.current_player = self.player_one
            self.start_game()
        else:
            print("\nResuming the old game")

    def start_game(self):
        print("Game started")
        self.is_paused = False
        """Add players to the score board"""
        # self.score_board.add_player(self.player_one.player_name)
        # self.score_board.add_player(self.player_two.player_name)
        Game.prompt = self.current_player.player_name + "> "

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
        Game.prompt = self.current_player.player_name + "> "

    def pass_to_human(self):
        """Do nothing just print that it's human's turn now"""
        Game.prompt = self.player_one.player_name + "> "
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
                Game.prompt = self.current_player.player_name + "> "
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
        Game.prompt = "piggygame> "

    def do_again(self, arg):
        """Play a new game"""
        if not self.is_paused:
            if self.is_round_over:
                self.is_round_over = False
                self.current_player = self.player_one
                self.display_score_board()
                self.print_whose_turn_it_is_now(self.current_player)
                Game.prompt = f"{self.current_player.player_name}> "
            else:
                print("Can't start a new game while current game is in progress")

        else:
            print("game paused. type resume to continue playing\n")

    def do_cheat(self, arg):
        """Cheat to win"""
        if not self.is_paused:
            self.current_player.set_score(100)
            self.announe_winner(self.current_player)
            self.check_if_round_end()
        else:
            print("game paused. type resume to continue playing\n")

    def do_pause(self, arg):
        """Save game data to file and pause the game"""
        # self.save_game()
        self.is_paused = True
        print("Game paused. Type 'resume' to resume game\n")
        Game.prompt = "piggygame> "

    def do_explain(self, arg):
        """Explain the rules of the game."""
        just_the_rules = Game.intro.splitlines()[4:14]
        print("\n".join(just_the_rules))

    def do_resume(self, arg):
        """Resuming game"""
        self.is_paused = False
        self.display_score_board()
        self.print_whose_turn_it_is_now(self.current_player)
        Game.prompt = self.current_player.player_name + "> "

    def do_namechange(self, arg):
        """Change your username"""
        new_name = input("Enter your new name: ")
        self.current_player.player_name = new_name
        print(f"\nYou have changed your name to {self.current_player.player_name}.\n")
        Game.prompt = self.current_player.player_name + "> "

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
        return True

    def __getstate__(self):
        """Added this to solve "can't pickle TextIOwrapper" error"""
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
