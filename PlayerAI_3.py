from BaseAI_3 import BaseAI
from evaluation import score
from random import randint
import sys
# "Up": 0, "Down": 1, "Left": 2, "Right": 3

class PlayerAI(BaseAI):
    def getMove(self, grid):
        (nextMove, _) = self.maximize(grid, 2, -sys.maxsize-1, sys.maxsize)
        print(nextMove)
        return nextMove

    def maximize(self, grid, depth, alpha, beta):
        moves = grid.getAvailableMoves()

        #terminal test
        if moves is None:
            return (None, sys.maxsize)

        # test all possibilities and choose the one with highest score.
        maxMove = None
        maxUtility = -sys.maxsize-1

        for move in moves:
            gridCopy = grid.clone()
            gridCopy.move(move)
            if depth is 0:
                utility = score(grid)
            else:
                (_, utility) = self.minimize(gridCopy, depth-1, alpha, beta)

            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return (maxMove, maxUtility)

    def minimize(self, grid, depth, alpha, beta):
        cells = grid.getAvailableCells()

        # terminal test
        if cells is None:
            return (None, 0)

        minMove = None
        minUtility = sys.maxsize

        val_list = [2, 4]
        for cell in cells:
            for val in val_list:
                gridCopy = grid.clone()
                gridCopy.map[cell[0]][cell[1]] = val
                (minMove, minUtility) = self.maximize(gridCopy, depth-1, alpha, beta)
                if minUtility <= alpha:
                    break
                if minUtility < beta:
                    beta = minUtility

        return (minMove, minUtility)