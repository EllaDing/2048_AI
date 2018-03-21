from BaseAI_3 import BaseAI
import sys
import time

timeLimit = 0.19

# "Up": 0, "Down": 1, "Left": 2, "Right": 3

class PlayerAI(BaseAI):

    def __init__(self):
        self.time_limit = 0.18
        self.prevTime = time.clock()
        self.DEPTH = 3

    def check_time(self, currTime):
        if currTime - self.prevTime >= timeLimit:
            #print (currTime - self.prevTime)
            return True
        return False

    def getMove(self, grid):
        self.prevTime = time.clock()
        (nextMove, _) = self.maximize(grid, self.DEPTH, -sys.maxsize-1, sys.maxsize)
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
                utility = self.score(grid)
            else:
                _, utility = self.minimize(gridCopy, depth-1, alpha, beta)

            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)

            if maxUtility >= beta or self.check_time(currTime=time.clock()):
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return (maxMove, maxUtility)

    def chance(self, grid, depth, alpha, beta):
        if depth is 0:
            return (None, self.score(grid))

        cells = grid.getAvailableCells()
        if cells is None:
            return (None, -sys.maxsize-1)
        s = 0
        for cell in cells:
            minVal = sys.maxsize
            for val, prob in ((2, 0.9), (4, 0.1)):
                gridCopy = grid.clone()
                gridCopy.setCellValue(cell, val)
                _, val = self.minimize(gridCopy, depth, alpha, beta)
                minVal = min(val*prob, minVal)
            s += minVal * 0.5

        return (None, s)

    def minimize(self, grid, depth, alpha, beta):
        if depth is 0:
            return (None, self.score(grid))
        cells = grid.getAvailableCells()

        # terminal test
        if cells is None:
            return (None, -sys.maxsize-1)

        minUtility = sys.maxsize

        for cell in cells:
            gridCopy = grid.clone()
            gridCopy.map[cell[0]][cell[1]] = 2
            (_, minUtility) = self.maximize(gridCopy, depth, alpha, beta)
            if minUtility <= alpha or self.check_time(currTime=time.clock()):
                break
            if minUtility < beta:
                beta = minUtility

        return (None, minUtility)

    def space(self, grid):
        space = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] is 0:
                    space += 1
        return space

    def monotony(self, grid):
        credit = 0
        if grid.size <= 2:
            return credit

        for x in range(grid.size):
            for y in range(1, grid.size):
                if grid.map[x][y] is 0:
                    continue

                if grid.map[x][y - 1] / grid.map[x][y] is 1:
                    credit += 40 * (grid.map[x][y - 1] ** 4)

                elif grid.map[x][y - 1] / grid.map[x][y] is 2:
                    credit += 20 * (grid.map[x][y - 1])
                else:
                    credit -= 10 * grid.map[x][y]

        for y in range(grid.size):
            for x in range(1, grid.size):
                if grid.map[x][y] is 0:
                    continue

                if grid.map[x-1][y] / grid.map[x][y] is 1:
                    credit += 40 * (grid.map[x - 1][y] ** 4)

                elif grid.map[x-1][y] / grid.map[x][y] is 2:
                    credit += 20 * (grid.map[x - 1][y])

                else:
                    credit -= 10 * grid.map[x][y]
        return credit

    def density(self, grid):
        space = 0
        s = 0

        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] is not 0:
                    s += grid.map[x][y] ** 2
                else:
                    space += 1
        # print("space: %g" % credit)
        return s / (16 - space), space

    def monotony1(self, grid, highest):
        mask = [[highest, highest/2, highest/4, highest/8],
                [highest/2, highest/4, highest/8, highest/16],
                [highest/4, highest/8, highest/16, highest/32],
                [highest/8, highest/16, highest/32, highest/64]]

        credit = 0
        for i in range(4):
            for j in range(4):
                credit += grid.map[i][j] * mask[i][j]
        return credit

    def monotony2(self, grid, highest):
        credit = 0
        corners = [[0,0],[grid.size-1, 0], [0, grid.size-1], [grid.size-1, grid.size-1]]
        for corner in corners:
            if grid.map[corner[0]][corner[1]] == highest:
                credit += 50
        return credit


    def score(self, grid):
        d, space = self.density(grid)
        highest = grid.getMaxTile()
        m1 = self.monotony(grid)
        m2 = self.monotony1(grid, highest)
        m3 = self.monotony2(grid, highest)
        score = 0.3 * m1 + 0.4 * m2 + 0.4 * d + 0.4 * m3 + 10 * space + 0.5 * highest**2
        return score

