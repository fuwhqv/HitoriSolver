from ..Solver.board import Board
from ..Solver.solver import Solver


solver = Solver()


def isGameFinished(): return solver.isFinished()
def toggleCW (x, y): solver.game.toggleCW (x, y)
def toggleCCW(x, y): solver.game.toggleCCW(x, y)
def makeGame(brd=[[1,1],[1,2]]): solver.setBoard(Board(brd))