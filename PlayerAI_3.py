from random import randint
from BaseAI_3 import BaseAI

# "Up": 0, "Down": 1, "Left": 2, "Right": 3
class PlayerAI(BaseAI):
        def getMove(self, grid):
            moves = grid.getAvailableMoves()
            return moves[randint(0, len(moves) - 1)] if moves else None
