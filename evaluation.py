#暴力，全取2, minmax
from random import randint
import math

def space(grid):
    space = 0
    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] is 0:
                space += 1
    return space

def monotony(grid):
    credit = 0
    if grid.size <= 2:
        return credit

    for x in range(grid.size):
        for y in range(1, grid.size):
            if grid.map[x][y] is 0:
                continue

            if grid.map[x][y-1]/grid.map[x][y] is 1:
                credit += 40 * (grid.map[x][y-1]**4)

            elif grid.map[x][y-1]/grid.map[x][y] is 2:
                credit += 20 * (grid.map[x][y-1])
            else:
                credit -= 10 * (grid.map[x][y])

    for y in range(grid.size):
        for x in range(1, grid.size):
            if grid.map[x][y] is 0:
                continue

            if grid.map[x-1][y]/grid.map[x][y] is 1:
                credit += 40 * (grid.map[x-1][y]**4)

            elif grid.map[x-1][y]/grid.map[x][y] is 2:
                credit += 20 * (grid.map[x-1][y])

            else:
                credit -= 10 * (grid.map[x][y])
    return credit

def density(grid):
    space = 0
    s = 0

    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] is not 0:
                s += grid.map[x][y]**2
            else: space += 1
    # print("space: %g" % credit)
    return s/(16-space), space


def monotony1(grid):
    credit = 0
    if grid.size <= 2:
        return credit

    for x in range(grid.size):
        for y in range(1, grid.size):
            if grid.map[x][y] is 0:
                credit -= grid.map[x][y-1] ** 1.5
                continue

            elif grid.map[x][y-1] is 0:
                credit -= grid.map[x][y] ** 1.5
                continue
            rate = (grid.map[x][y-1]/grid.map[x][y])**3
            test = rate + 1.0 / rate
            credit += 10 * grid.map[x][y] / test


    for y in range(grid.size):
        for x in range(1, grid.size):
            if grid.map[x][y] is 0:
                credit -= grid.map[x-1][y] ** 1.5
                continue

            elif grid.map[x-1][y] is 0:
                credit -= grid.map[x][y] ** 1.5
                continue

            rate = (grid.map[x-1][y] / grid.map[x][y])**3
            test = rate + 1.0 / rate

            credit += 10 * grid.map[x][y] / test

    return credit

def density1(grid):
    space = 0
    s = 0

    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] is not 0:
                s += grid.map[x][y]**2
            else: space += 1
    # print("space: %g" % credit)
    return s/(16-space), space


def score(grid):
    d, space = density1(grid)
    highest = grid.getMaxTile()

   # print (m, sp, 10 * grid.getMaxTile())
    # 50的时候可以达到1024 median
    if highest < 1024:
        m = monotony(grid)
        d, space = density(grid)
        score = m * math.sqrt(highest) + d * highest
    else:
        m = monotony1(grid)
        score = m * math.sqrt(highest) + 5 * d * highest + 10 * highest**2

    return score

