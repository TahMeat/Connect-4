#!/usr/bin/env python
"""
Original by : Copyright (C) 2016 Chris Conly (chris.conly@uta.edu)

Name : Ron Nguyen
ID : 1001762342
"""
from MaxConnect4Game import *
import sys


# reduces repeated lines of code found in oneMoveGame and makeMove
def pushConsole(currentGame: maxConnect4Game) -> None:
    print('Game state after move:')
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()


def oneMoveGame(currentGame: maxConnect4Game) -> None:
    if currentGame.pieceCount == 42:  # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)

    # determine MAX and MIN
    if currentGame.currentTurn == 1:
        move = miniMax(currentGame, True, 0, float('-inf'), float('inf'))
    else:
        move = miniMax(currentGame, False, 0, float('-inf'), float('inf'))
    currentGame.playPiece(move)
    currentGame.currentTurn = 2 if currentGame.currentTurn == 1 else 1
    pushConsole(currentGame)
    currentGame.gameFile.close()


def makeMove(currentGame: maxConnect4Game, move: int) -> None:
    print('\n\nmove %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, move + 1))
    currentGame.currentTurn = 2 if currentGame.currentTurn == 1 else 1
    pushConsole(currentGame)


def interactiveGame(currentGame: maxConnect4Game) -> None:
    while currentGame.pieceCount != 42:  # Indefinite loop until max pieces.
        if currentGame.currentTurn == 1:  # Players' turn
            # Get input
            print("Your turn!")
            playerMove = input("Enter column number (0-6) to place piece: ")

            # Check if given input is a digit. Self-explanatory.
            if playerMove.isdigit():
                playerMove = int(playerMove)
            else:
                print("%s is NOT a number, try again." % playerMove)
                continue
            if not 0 <= playerMove <= 6:
                print("%s is NOT within 0 and 6, try again." % playerMove)
                continue
            if not currentGame.playPiece(playerMove):
                print("Column %s is full, try again." % playerMove)
                continue
            try:
                currentGame.gameFile = open("human.txt", 'w')
            except:
                sys.exit('Error opening output file.')
            makeMove(currentGame, playerMove)
        else:  # Else, computer.
            move = miniMax(currentGame, False, 0, float('-inf'), float('inf'))
            try:
                currentGame.gameFile = open("computer.txt", 'w')
            except:
                sys.exit('Error opening output file.')
            currentGame.playPiece(move)
            makeMove(currentGame, move)

    # Max pieces met, close and check scoring.
    if currentGame.player1Score > currentGame.player2Score:
        print("You won, with a %d lead!" % (currentGame.player1Score - currentGame.player2Score))
    elif currentGame.player1Score == currentGame.player2Score:
        print("Draw!")
    else:
        print("The computer won, good try!")


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game(int(argv[4]))  # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print('\nMaxConnect-4 game\n')
    print('Game state before move:')
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        interactiveGame(currentGame)  # Be sure to pass whatever else you need from the command line
    else:  # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame)  # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
