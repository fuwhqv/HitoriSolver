from ..Solver.board import Board
from ..Solver.solver import Solver


solver = Solver()
stepToColor=[1, 2, 1, 1, 2, 1, 2, 2, None, 1, 2]
#      step= 0  1  2  3  4  5  6  7   |    X  X

def isGameFinished(): return solver.isFinished()
def toggleCW (x, y): solver.game.toggleCW (x, y)
def toggleCCW(x, y): solver.game.toggleCCW(x, y)
def makeGame(brd=[[1,1],[1,2]]): solver.setBoard(Board(brd))

