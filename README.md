# Pig game

Terminal-based implementation of the dice game Pig using Python. We used a test-driven developmental approach.

## Table of Contents

- [Rules](#rules)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

---

## Rules

The aim of the game is to be the first player to reach 100 points. Before the game starts, the user selects if they are using one or two dice. They also decide if they are playing against another human or the computer (robot).On a players turn, the roll the dice. They can then choose if they want to continue rolling or hold. If they choose to hold, the turn score is added to their total score. If a player rolls a 1, they lose their points for that turn and the play goes over to the next player. If two dice are used and the player rolls two 1's, they lose all their points for that game and the turn goes over to the next player.

## Installation

Provide instructions on how to install your project.

```bash
# Clone the repository
git clone https://github.com/HmonWutt/Piggy_game.git

# Navigate to the project folder
cd piggy_game

# Install dependencies
pip install -r requirements.txt
```

You can also choose to install the dependencies using:
`make install`

You can generate UML diagrams by running:
`make uml`

## Usage

To start the game:
`make run`

When the game is running, see available commands:
`make help`

## Testing

To start the tests:
`make test`

To view the test coverage:
`make coverage`

To test the code structure:
`make lint`

## Features

- Play against either another player or the computer
- Three difficulty levels for the AI/computer: easy, medium, and hard
- Leaderboard showing the amount of wins per player
- Save game and resume saved game
- Possible to change player name, which also changes the name if the player is already on the leaderboard
- Cheat functionality for demo purposes (we won't judge you for using it!)
- Pause functionality
- Tests are made using pytest and unittest

## Contributing

- [Rebecca Blixt](https://github.com/rebeccablixt/)

- [Dechen Dolkar](https://github.com/ddolkar61dechen/)

- [Hmon Wutt](https://github.com/HmonWutt/)

The game based on a test-driven development (TDD) assignment for the course Methods for Sustainable Programming (DA214A) at Kristianstad University for the autumn term of 2025.

## License

- [MIT License](LICENSE.md)
