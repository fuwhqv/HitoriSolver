from Cell import Cell
from copy import deepcopy

dxy = [[1,0],[0,1],[-1,0],[0,-1]]

class Board:
    def __init__(self, arr = [[1,1],[1,2]]):
        self.n = len(arr   )
        self.m = len(arr[0])
        for row in arr:
            if len(row) != self.m:
                raise Exception('Invalid board')
        self.brd = [[None ] * self.m for _ in range(self.n)]
        self.vst = [[False] * self.m for _ in range(self.n)]

        for i, row in enumerate(arr):
            for j, val in enumerate(row):
                self.brd[i][j] = Cell(val)

    def __repr__(self):
        ret = ''
        for row in self.brd:
            for cell in row:
                ret += str(cell)
            ret += '\n'
        return ret

    def getColorsOnly(self):
        ret = ''
        for row in self.brd:
            for cell in row:
                ret += '■' if cell.isWhite() else ('□' if cell.isBlack() else '  ')
            ret += '\n'
        return ret

    def isInBoard(self, x, y): return x>=0 and y>=0 and x<self.m and y<self.n
    def print(self): print(self)
    def printColorsOnly(self): print(self.getColorsOnly())

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
                    for [dx, dy] in dxy[:1]:
                        nx = x+dx; ny = y+dy
                        if not self.isInBoard(nx, ny): continue
                        if self.brd[ny][nx].isBlack():
                            #print('adj Black')
                            return False

        # 3. is there any duplicate
                if self.brd[y][x].isWhite():
                    for [dx, dy] in dxy[:1]:
                        [nx, ny] = [x, y]
                        while True:
                            nx += dx; ny += dy
                            if not self.isInBoard(nx, ny): break
                            if (self.brd[ny][nx].isWhite()
                            and self.brd[ny][nx].getData() == self.brd[y][x].getData()
                            ):
                                #print('dup White')
                                return False
        return True

    def isFinished(self):    
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

        return self.isOK()

    def toggleCW (self, x, y): self.brd[y][x].toggleCW ()
    def toggleCCW(self, x, y): self.brd[y][x].toggleCCW()

if __name__=='__main__':
#for module debugging
    pass
