from random import randint
def smooth(grid):
    credit = 0
    for x in range(grid.size):
        for y in range(1, grid.size):
            if grid.map[x][y] is 0 or grid.map[x][y-1] is 0:
                continue

            if max(grid.map[x][y-1]/grid.map[x][y], grid.map[x][y]/grid.map[x][y-1]) < 4:
                credit += 1000

    for y in range(grid.size):
        for x in range(1, grid.size):
            if grid.map[x][y] is 0 or grid.map[x-1][y] is 0:
                continue

            if max(grid.map[x][y]/grid.map[x-1][y], grid.map[x-1][y]/grid.map[x][y]) < 4:
                credit += 1000

    # print ("smooth: %g"%credit)
    return credit

def monotony(grid):
    credit = 0
    if grid.size <= 2:
        return credit

    for x in range(grid.size):
        for y in range(1, grid.size):
            if grid.map[x][y] is 0:
                continue

            if grid.map[x][y-1] is 0:
                credit -= grid.map[x][y]*800

            elif grid.map[x][y-1]/grid.map[x][y] is 1:
                credit += 600 * grid.map[x][y-1]

            elif grid.map[x][y-1]/grid.map[x][y] is 2:
                credit += 500 * grid.map[x][y-1]

    for y in range(grid.size):
        for x in range(1, grid.size):
            if grid.map[x][y] is 0:
                continue

            if grid.map[x-1][y] is 0:
                credit -= grid.map[x][y]*800

            elif grid.map[x-1][y]/grid.map[x][y] is 1:
                credit += 600 * grid.map[x-1][y]

            elif grid.map[x - 1][y]/grid.map[x][y] is 2:
                credit += 500 * grid.map[x-1][y]

    # print("monotony: %g" % credit)
    return credit

def monotony1(grid):
    credit = 0
    if grid.size <= 2:
        return credit

    for x in range(grid.size):
        for y in range(grid.size):
            if x % 2 is 0:
                if y is 0 or grid.map[x][y] is 0:
                    continue

                if grid.map[x][y-1] is 0:
                    credit -= grid.map[x][y]*500 * (x+1)

                elif grid.map[x][y-1]/grid.map[x][y] is 1:
                    credit += 100 * grid.map[x][y-1] * (x+1)

                elif grid.map[x][y-1]/grid.map[x][y] is 2:
                    credit += 800 * grid.map[x][y-1] * (x+1)
            else:
                if y is grid.size-1 or grid.map[x][y] is 0:
                    continue

                if grid.map[x][y+1] is 0:
                    credit -= grid.map[x][y] * 500 * (x+1)

                elif grid.map[x][y+1] / grid.map[x][y] is 1:
                    credit += 100 * grid.map[x][y+1] * (x+1)

                elif grid.map[x][y+1] / grid.map[x][y] is 2:
                    credit += 800 * grid.map[x][y+1] * (x+1)

    # print("monotony: %g" % credit)
    return credit


def density(grid):
    space = 0
    s = 0

    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] is not 0:
                s += grid.map[x][y]
                space += 1
    # print("space: %g" % credit)
    return s/space, space


def score(grid):
    m = monotony1(grid)
    d, space = density(grid)

   # print (m, sp, 10 * grid.getMaxTile())
    score = m + 8000/space + d * 600 + grid.getMaxTile() * grid.getMaxTile()

    return score

