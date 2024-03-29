if __name__ in ['__main__', 'board']:
    from cell import Cell
else:
    from .cell import Cell
from copy import deepcopy

dxy = [[1,0],[0,1],[-1,0],[0,-1]]
colorType = ['  ', '■', '□'] #empty, white, black

class Board:
    def __init__(self, arr = [[1,1],[1,2]]):
        self.n = len(arr   )
        self.m = len(arr[0])
        for row in arr:
            if len(row) != self.m:
                raise Exception('Invalid board')
        self.brd = [[None ] * self.m for _ in range(self.n)]
        self.vst = [[False] * self.m for _ in range(self.n)]
        self.isDone = False

        for i, row in enumerate(arr):
            for j, val in enumerate(row):
                self.brd[i][j] = Cell(val)

    def __repr__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.brd])

    def getColorsOnly(self):
        return '\n'.join([''.join(map(lambda x: colorType[x.getType()], row)) for row in self.brd])

    def isInBoard(self, x, y): return x>=0 and y>=0 and x<self.m and y<self.n
    def print(self): print(self)
    def printColorsOnly(self): print(self.getColorsOnly())

    def clear(self):
        for row in self.brd:
            for cell in row:
                while cell.getType() != 0:
                    cell.toggleCW()
        self.isDone = False

    def fillVst(self, x, y):
        if not self.isInBoard(x, y): return
        if self.vst[y][x]: return
        if self.brd[y][x].isEmpty(): return
        self.vst[y][x] = True
        if self.brd[y][x].isBlack(): return
        for [dx, dy] in dxy: self.fillVst(x+dx, y+dy)

    def isOK(self):
        for y in range(self.n):
            for x in range(self.m):
        # 2. is there any adjecent black
                if self.brd[y][x].isBlack():
                    for [dx, dy] in dxy[:2]:
                        nx = x+dx; ny = y+dy
                        if not self.isInBoard(nx, ny): continue
                        if self.brd[ny][nx].isBlack():
                            #print('adj Black')
                            return False

        # 3. is there any duplicate
                if self.brd[y][x].isWhite():
                    #print(f'W({x},{y})')
                    for [dx, dy] in dxy[:2]:
                        [nx, ny] = [x, y]
                        while True:
                            nx += dx; ny += dy
                            if not self.isInBoard(nx, ny): break
                            #print(f'({x},{y})={self.brd[ny][nx]}')
                            if (self.brd[ny][nx].isWhite()
                            and self.brd[ny][nx].getData() == self.brd[y][x].getData()
                            ):
                                #print('dup White')
                                return False
        return True

    def isFinished(self):
        if self.isDone: return True

        # 0-1. is all white connected - part 1
        self.vst = [[False] * self.m for _ in range(self.n)]
        self.fillVst(0,0); self.fillVst(1,0)

        for y in range(self.n):
            for x in range(self.m):
                #print(('(%d,%d)'%(x,y))+str(self.brd[y][x]))
        # 0-2. is all white connected - part 2
                if not self.vst[y][x]:
                    #print('vst Fail')
                    return False

        # 1.is all cell is either black or white
                if self.brd[y][x].isEmpty():
                    #print('empty Cell')
                    return False

        self.isDone = self.isOK()
        return self.isDone

    def toggleCW (self, x, y):
        self.brd[y][x].toggleCW ()
    def toggleCCW(self, x, y): self.brd[y][x].toggleCCW()

if __name__=='__main__':
    game = Board()
    game.toggleCW(0,0)
    game.toggleCCW(1,0)
    game.toggleCW(0,1)
    game.toggleCW(1,1)
    print(game.isFinished())
#for module debugging
'''
    game = Board([[2,4,2,3,3,6],
                  [2,6,3,4,1,3],
                  [5,5,3,2,4,2],
                  [3,3,6,5,1,1],
                  [6,5,6,2,3,4],
                  [3,3,4,1,4,5]])

    game.toggleCCW(0, 0)
    game.toggleCCW(0, 0)
    game.toggleCCW(0, 0)
    game.toggleCCW(0, 0)
    game.toggleCCW(4, 0)
    game.toggleCCW(2, 1)
    game.toggleCCW(1, 2)
    game.toggleCCW(3, 2)
    game.toggleCCW(0, 3)
    game.toggleCCW(4, 3)
    game.toggleCCW(2, 4)
    game.toggleCCW(1, 5)
    game.toggleCCW(4, 5)

    game.toggleCW(1, 0)
    game.toggleCW(1, 0)
    game.toggleCW(1, 0)
    game.toggleCW(1, 0)
    game.toggleCW(2, 0)
    game.toggleCW(3, 0)
    game.toggleCW(5, 0)
    game.toggleCW(0, 1)
    game.toggleCW(1, 1)
    game.toggleCW(3, 1)
    game.toggleCW(4, 1)
    game.toggleCW(5, 1)
    game.toggleCW(0, 2)
    game.toggleCW(2, 2)
    game.toggleCW(4, 2)
    game.toggleCW(5, 2)
    game.toggleCW(1, 3)
    game.toggleCW(2, 3)
    game.toggleCW(3, 3)
    game.toggleCW(5, 3)
    game.toggleCW(0, 4)
    game.toggleCW(1, 4)
    game.toggleCW(3, 4)
    game.toggleCW(4, 4)
    game.toggleCW(5, 4)
    game.toggleCW(0, 5)
    game.toggleCW(2, 5)
    game.toggleCW(3, 5)
    game.toggleCW(5, 5)

    print(game.isFinished())
    print(game)
    print(game.getColorsOnly())
'''