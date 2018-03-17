from BaseAI_3 import BaseAI
from evaluation import score, space
from random import randint
import sys
# "Up": 0, "Down": 1, "Left": 2, "Right": 3

class PlayerAI(BaseAI):
    def getMove(self, grid):
        s = space(grid)
        if s > 5:
            depth = 2
        else: depth = 3
        (nextMove, _) = self.maximize(grid, depth, -sys.maxsize-1, sys.maxsize)
        # print(nextMove)
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
                _, utility = self.minimize(gridCopy, depth-1, alpha, beta)

            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)

            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return (maxMove, maxUtility)

    def chance(self, grid, depth, alpha, beta):
        if depth is 0:
            return (None, score(grid))

        cells = grid.getAvailableCells()
        if cells is None:
            return (None, -sys.maxsize-1)
        s = 0
        for val, prob in ((2, 0.9), (4, 0.1)):
            s_list = []
            for cell in cells:
                gridCopy = grid.clone()
                gridCopy.setCellValue(cell, val)
                _, minVal = self.minimize(gridCopy, depth, alpha, beta)
                s_list.append(minVal)
            s += sum(s_list)/len(s_list)*prob
        return (None, s)

    def minimize(self, grid, depth, alpha, beta):
        if depth is 0:
            return (None, score(grid))
        cells = grid.getAvailableCells()

        # terminal test
        if cells is None:
            return (None, -sys.maxsize-1)

        minUtility = sys.maxsize

        for cell in cells:
            gridCopy = grid.clone()
            gridCopy.map[cell[0]][cell[1]] = 2
            (_, minUtility) = self.maximize(gridCopy, depth, alpha, beta)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        return (None, minUtility)