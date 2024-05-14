# Connect-4
This is a Python script that implements an AI opponent to play against the user or another AI opponent.

This script implements the minimax algorithm with alpha-beta pruning to ensure optimal placement. This game is played within the user's console.

Thank you to Chris Conly for providing the sample Connect4 game code.

## Badges

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Run Locally

Clone the project

```bash
  git clone https://github.com/TahMeat/Connect-4/
```

Go to the project directory

```bash
  cd Connect-4/
```

Run the program

```bash
  python .\maxconnect4.py [game_type] [input_file] [output_file] [depth]
```

#### Arguments

- `game_type`: Specifies the type of game. Valid options are:
  - `interactive`: Allows a user to play against the computer.
  - `one-move`: The computer performs a single move, and saves it into the output_file. This allows for the program to compete against itself.
- `input_file`: The path to the file containing the initial state of the game board.
- `output_file`: The path where the resulting state of the game board should be saved after the move.
- `depth`: Integer representing the maximum depth the AI should use for its decision-making process.

## Screenshots
![Sample console view.](https://github.com/TahMeat/Connect-4/assets/40926372/70ff4883-8fc7-4960-93a9-e19d0eba8083)
