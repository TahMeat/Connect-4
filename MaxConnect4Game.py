#!/usr/bin/env python
"""
Original by : Copyright (C) 2016 Chris Conly (chris.conly@uta.edu)

Name : Ron Nguyen
ID : 1001762342
"""
import copy
import random

from typing import List


# Minimax implementation with depth and alpha-beta prune.
# Returns all valid moves.
def validMoves(state) -> List[int]:
    return [col for col, colVal in enumerate(state.gameBoard[0]) if colVal == 0]


# Creates a new state to keep original intact.
def createState(state, move) -> 'maxConnect4Game':
    # create a new game, deep copy it over.
    newGame = maxConnect4Game(state.maxDepth)
    newGame.gameBoard = copy.deepcopy(state.gameBoard)
    newGame.currentTurn = state.currentTurn
    newGame.player1Score = state.player1Score
    newGame.player2Score = state.player2Score
    newGame.pieceCount = state.pieceCount

    # make move
    newGame.playPiece(move)
    newGame.checkPieceCount()
    newGame.countScore()

    # change turn
    newGame.currentTurn = 2 if newGame.currentTurn == 1 else 1

    return newGame


def minEvaluate(state: 'maxConnect4Game', alpha: int, beta: int, depth: int) -> (float, int):
    bestVal, bestMove = float('inf'), None
    for move in validMoves(state):
        newState = createState(state, move)
        val = miniMax(newState, True, depth + 1, alpha, beta)
        if val is not None and val < bestVal:
            bestVal, bestMove = val, move
        beta = min(beta, bestVal)
        if beta <= alpha:
            break
    return bestVal, bestMove


def maxEvaluate(state: 'maxConnect4Game', alpha: int, beta: int, depth: int) -> (float, int):
    bestVal, bestMove = float('-inf'), None
    for move in validMoves(state):
        newState = createState(state, move)
        val = miniMax(newState, False, depth + 1, alpha, beta)
        if val is not None and val > bestVal:
            bestVal, bestMove = val, move
        alpha = max(alpha, bestVal)
        if beta <= alpha:
            break
    return bestVal, bestMove


# Main algorithm, self-explanatory.
def miniMax(state: 'maxConnect4Game', isMaximizing: bool, depth: int, alpha: int, beta: int) -> float:
    # Max pieces or max depth.
    if state.pieceCount == 42 or depth == state.maxDepth:
        return state.player1Score - state.player2Score

    # Continue with algo.
    if isMaximizing:
        value, move = maxEvaluate(state, alpha, beta, depth)
        return move if depth == 0 else value
    else:
        value, move = minEvaluate(state, alpha, beta, depth)
        return move if depth == 0 else value


class maxConnect4Game:
    def __init__(self, depth):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.maxDepth = depth
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print(' -----------------')
        for i in range(6):
            print(' |', end=" ")
            for j in range(7):
                print('%d' % self.gameBoard[i][j], end=" ")
            print('| ')
        print(' -----------------')

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently, plays randomly.
    def aiPlay(self):
        randColumn = random.randrange(0, 7)
        result = self.playPiece(randColumn)
        if not result:
            self.aiPlay()
        else:
            print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, randColumn + 1))
            if self.currentTurn == 1:
                self.currentTurn = 2
            elif self.currentTurn == 2:
                self.currentTurn = 1

    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0

        def check_line(line, player):
            return line == [player] * 4

        def count_horizontal(player):
            return sum(1 for row in self.gameBoard for i in range(4) if check_line(row[i:i + 4], player))

        def count_vertical(player):
            return sum(1 for col in range(7) for row in range(3) if check_line([self.gameBoard[row + i][col]
                                                                                for i in range(4)], player))

        def count_diagonal(player):
            score = 0
            for row in range(3):
                for col in range(4):
                    if check_line([self.gameBoard[row + i][col + i] for i in range(4)], player) or \
                            check_line([self.gameBoard[row + i][col + 3 - i] for i in range(4)], player):
                        score += 1
            return score

        self.player1Score = count_horizontal(1) + count_vertical(1) + count_diagonal(1)
        self.player2Score = count_horizontal(2) + count_vertical(2) + count_diagonal(2)
