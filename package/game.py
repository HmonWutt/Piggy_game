import cmd

class Game(cmd.Cmd):
    intro = "Hi welcome to pig game." 
    prompt = "piggame: "
    # def __init__(self):
    #     super().__init__()
    #     self.player = Player("Name")

    def do_explain(self,arg):
        """Explain the game."""
        print("Some explanation of the game....")

    def do_exit(self,arg):
        """Exit the game"""
        print("Exiting the game now..")
        return True
