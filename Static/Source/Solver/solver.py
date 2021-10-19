if __name__ in ['__main__', 'solver']:
    from cell import Cell
    from board import Board, dxy
else:
    from .cell import Cell
    from .board import Board, dxy
import copy

class Solver:
    def __init__(self, arr:list = [[1,1],[1,2]]):
        self.game = Board(arr)

    def __repr__(self):
        return self.game.__repr__()

    def setBoard(self, brd:Board): self.game = brd
    def isFinished(self): return self.game.isFinished()
    def print(self): self.game.print()
    def printColorsOnly(self): self.game.printColorsOnly()
    def clear(self): self.game.clear()

    def toggleAdjEmptyToWhite(self, x, y):
        if not self.game.brd[y][x].isBlack(): return
        for [dx, dy] in dxy:
            [nx, ny] = [x+dx, y+dy]
            if not self.game.isInBoard(nx, ny): continue
            if not self.game.brd[ny][nx].isEmpty(): continue
            self.game.brd[ny][nx].toggleCW()

    def toggleFacingDupToBlack(self, x, y):
        if not self.game.brd[y][x].isWhite(): return
        for [dx, dy] in dxy:
            [nx, ny] = [x, y]
            while True:
                nx += dx; ny += dy
                if not self.game.isInBoard(nx, ny): break
                #print(x,y,nx,ny)
                if not self.game.brd[ny][nx].isEmpty(): continue
                if self.game.brd[ny][nx].getData() == self.game.brd[y][x].getData():
                    self.game.brd[ny][nx].toggleCCW()

    def stepX(self, x, y):
#Step X: make a copy and brute-force
        if not self.game.brd[y][x].isEmpty(): return
        temp = Solver()
        temp.setBoard(copy.deepcopy(self.game))
        #temp.print()
        temp.game.brd[y][x].toggleCW()
        temp.solve()
        if not temp.game.isOK():
            #print('did something at (%d,%d)!'%(x, y))
            self.game.brd[y][x].toggleCCW()
            return
        if temp.game.isFinished():
            self.game = temp.game

    def step0(self, x, y):
#Step 0: find empty which cannot be dup and toggle it to white
        if not self.game.brd[y][x].isEmpty(): return
        for i in range(self.game.n):
            if y == i: continue
            if((self.game.brd[i][x].getData() == self.game.brd[y][x].getData())
            and (not self.game.brd[i][x].isBlack())): return
        for j in range(self.game.m):
            if j == x: continue
            if((self.game.brd[y][j].getData() == self.game.brd[y][x].getData())
            and (not self.game.brd[y][j].isBlack())): return
        self.game.brd[y][x].toggleCW()

    def step1(self, x, y):
#Step 1: find any possible dup and toggle to black
        #if not self.game.brd[y][x].isWhite(): return
        self.toggleFacingDupToBlack(x, y)

    def step2(self, x, y):
#Step 2: find any empty adj to black and toggle to white
        #if not self.game.brd[y][x].isBlack(): return
        self.toggleAdjEmptyToWhite(x, y)

    def step3(self, x, y):
#Step 3: find any dup with only one empty between and toggle the one to white
        for [dx, dy] in dxy[:2]:
            nx = x + dx * 2; ny = y + dy * 2
            if not self.game.isInBoard(nx, ny): continue
            if self.game.brd[y][x].getData() == self.game.brd[ny][nx].getData():
                if self.game.brd[y+dy][x+dx].isEmpty():
                    self.game.brd[y+dy][x+dx].toggleCW()
                    self.toggleFacingDupToBlack(x+dx, y+dy)

    def step4(self, x, y):
#Step 4: find any triplet with two of them adj, toggle the last one to black
        for [dx, dy] in dxy[:2]:
            ax = x + dx; ay = y + dy
            if not self.game.isInBoard(ax, ay): continue
            if self.game.brd[y][x].getData() != self.game.brd[ay][ax].getData(): continue
            tx = -1; ty = -1
            if dx == 0: tx = x
            else      : ty = y
            while True:
                tx += dx; ty += dy
                if not self.game.isInBoard(tx, ty): break
                if((tx ==  x and ty ==  y)
                or (tx == ax and ty == ay)): continue
                if self.game.brd[y][x].getData() == self.game.brd[ty][tx].getData():
                    if self.game.brd[ty][tx].isEmpty():
                        self.game.brd[ty][tx].toggleCCW()
                        self.toggleAdjEmptyToWhite(tx, ty)

    def step5(self, x, y):
#Step 5: find any empty which can cut the white group into to, toggle it to white
        if not self.game.brd[y][x].isEmpty(): return
        self.game.brd[y][x].toggleCCW()
        partial = False
        for [dx, dy] in dxy:
            nx = x + dx; ny = y + dy
            if not self.game.isInBoard(nx, ny): continue
            if 0 < self.step5_sub_dfs(nx, ny, [[False] * self.game.m for _ in range(self.game.n)]):
                partial = True
                break
        if partial:
            self.game.brd[y][x].toggleCCW()
            self.toggleFacingDupToBlack(x,y)
            return
        self.game.brd[y][x].toggleCW()

    def step5_sub_dfs(self, x, y, vst):
#this function counts the size of area,
#which only includes white cells that are surrounded by black cells.
#but if there's any grey cells remaining, the area must not be counted as closed group,
#so in that case this returns very small negative number, which cannot be in normal case.
        if not self.game.isInBoard(x, y): return 0
        if vst[y][x]: return 0
        vst[y][x] = True
        if self.game.brd[y][x].isBlack(): return 0
        if self.game.brd[y][x].isEmpty(): return -9999
        area = 1
        for [dx, dy] in dxy:
            nx = x + dx; ny = y + dy
            area += self.step5_sub_dfs(nx, ny, vst)
        return area

    def step6(self, x, y):
#Step 6: find a triplet, two of which are neighboring same number with different position -
#but also the neighbors themselves are in the same line,
#toggle the last one to white
#ex: 1 4 1 5 6 5 1 => the leftmost 1 is must be Black - if not, two 5s gonna conflict
        if not self.game.brd[y][x].isEmpty(): return
        #print('step6 at (%d,%d)'%(x,y))
        for [dx, dy] in dxy[:2]:
            cnt = 0
            tx = ty = ax = ay = bx = by = -1
            if dx == 0: tx = ax = bx = x
            else      : ty = ay = by = y
            while True:
                if cnt == 2: break
                tx += dx; ty += dy
                if not self.game.isInBoard(tx, ty): break
                if(tx == x and ty == y): continue
                #print('__(%d,%d)'%(tx, ty))
                if self.game.brd[y][x].getData() == self.game.brd[ty][tx].getData():
                    if cnt<1: ax, ay = tx, ty
                    else    : bx, by = tx, ty
                    cnt += 1
            if cnt<2: continue

            for[ddx1, ddy1] in dxy:
                adx = ax + ddx1; ady = ay + ddy1
                for[ddx2, ddy2] in dxy:
                    bdx = bx + ddx2; bdy = by + ddy2
                    if not (self.game.isInBoard(adx, ady) and self.game.isInBoard(bdx, bdy)): continue
                    if adx != bdx and ady != bdy: continue
                    if adx == bdx and ady == bdy: continue
                    #print('(%d,%d)=%d,(%d,%d)=%d'%
                    #    (adx,ady,self.game.brd[ady][adx].getData(),bdx,bdy,self.game.brd[bdy][bdx].getData()))
                    if self.game.brd[ady][adx].getData() == self.game.brd[bdy][bdx].getData():
                        self.game.brd[y][x].toggleCCW()
                        #print('did something at (%d, %d)!'%(x, y))
                        self.toggleAdjEmptyToWhite(x, y)

    def step7(self, x, y):
#Step 7: Similarly with step 6, find a pair of duplicate neighboring each other,
#and then find another duplicate which is in orthogonal,
#seemingly shapes like L. Target cell is the shared one.
#check if two cells other than the target cell neighbors same number in the same line.
#if yes, toggle the target cell to black.
#ex) 1 4 5 1 2  <<in this case, if target cell is not black, the two 2s will conflict.
#    2 3 2 1 5
        if not self.game.brd[y][x].isEmpty(): return
        for [dx, dy] in dxy:
            ax = x + dx; ay = y + dy
            if not self.game.isInBoard(ax, ay): continue
            if self.game.brd[y][x].getData() != self.game.brd[ay][ax].getData(): continue
            bdx = dy * dy; bdy = dx * dx
            bx = x * bdy - bdx; by = y * bdx - bdy
            while True:
                bx += bdx; by += bdy
                if not self.game.isInBoard(bx, by): return
                if(bx == x and by == y): continue
                if self.game.brd[y][x].getData() == self.game.brd[by][bx].getData():
                    for [ddx1, ddy1] in dxy:
                        px = ax + ddx1; py = ay + ddy1
                        for [ddx2, ddy2] in dxy:
                            qx = bx + ddx2; qy = by + ddy2
                            if not (self.game.isInBoard(px, py) and self.game.isInBoard(qx, qy)): continue
                            if px != qx and py != qy: continue
                            if px == qx and py == qy: continue
                            if self.game.brd[py][px].getData() == self.game.brd[qy][qx].getData():
                                self.game.brd[y][x].toggleCCW()
                                self.toggleAdjEmptyToWhite(x, y)
                                #print('did something at (%d,%d)!'%(x, y))
                                #self.printColorsOnly()
                                return
 
    def solve(self):
        steps = [self.step0,
                 self.step1,
                 self.step2,
                 self.step3,
                 self.step4,
                 self.step5,
                 self.step6,
                 self.step7,
                 self.stepX
                 ]
        idx = 0

        while not self.isFinished():
            if idx >= len(steps): break

            prev = copy.deepcopy(self.game.brd)
            for i in range(self.game.n):
                for j in range(self.game.m):
                    steps[idx](j, i)
            #print(('step%d: '%idx)+str(self.isFinished()))
            idx = idx+1 if isEqual(prev, self.game.brd) else 1
            #self.printColorsOnly()

def isEqual(a, b):
    for arow, brow in zip(a, b):
        for aval, bval in zip(arow, brow):
            if aval != bval: return False
    return True

if __name__=='__main__':
#for module debugging
    game = Solver([
        [ 7, 7, 9, 6, 9, 5, 8, 2, 8, 3, 1, 5],
        [ 9,12, 7, 2,11, 9, 1, 1, 2, 6, 4, 4],
        [ 9, 5,12, 9, 1,12, 7, 1,11,10,11, 2],
        [ 6, 9, 5, 3,12, 1, 2,12, 8, 4, 5, 7],
        [10,11, 3, 8,12,11, 7,12, 2, 2, 7, 8],
        [10,11, 7, 7, 4, 5, 5, 3, 1,12, 1,10],
        [ 2, 3, 1,12,11, 9,10, 4, 5, 5, 4,11],
        [11, 5,12, 9, 7, 4, 9, 4,12, 5,11, 8],
        [ 5, 8, 3, 2,10, 4, 3, 2,11, 1,12, 9],
        [ 2,10, 9,11, 2, 8, 6, 8,12,11, 6, 5],
        [ 7, 2, 4,11, 1, 8,10,10, 7, 9, 5, 9],
        [ 5, 4, 4, 5, 3,11,11, 9, 7, 9, 6, 1]
        ])
    
    print(str(game) + '\n')

    import time

    st = time.time()
    game.solve()
    ed = time.time()

    print('Solved in %.3fs'%(ed - st) if game.isFinished() else 'unsolved')
    game.print()
    game.printColorsOnly()
    print('□: Black\n■: White')

'''
        [ 4, 4,12, 2, 8, 8, 6, 7,12, 7, 6, 1],
        [ 7, 8, 5, 4, 1,11, 2, 6, 4, 9, 3,12],
        [ 6, 1,10, 4,12, 6, 9,10, 4, 9, 7, 1],
        [11, 5,11,12, 9, 4,12, 2, 8, 1,10,10],
        [11,12, 7, 8, 1, 1, 3, 6, 6,12, 2, 7],
        [10, 4, 4, 9, 6,12, 3,11, 6, 3, 5, 5],
        [ 5, 9,10,10,12, 6, 8,12,11, 7, 7, 3],
        [ 7, 2, 7, 6, 8, 5, 2, 1, 8,10, 9, 4],
        [ 2, 8, 8, 7, 7, 5, 4, 2, 1, 6, 6, 5],
        [ 8, 3, 1, 7, 9,10, 6, 9, 7,12, 4, 3],
        [ 9, 1, 5, 3, 5,12,12, 9, 7, 1,11,10],
        [ 4, 5,12, 1, 7, 7, 5,10, 9,11, 8, 4]
#from Brainbashers' Daily Hitory, 01/01/2021's Weekly Special

        [5,2,2,7,6,3,5],
        [6,2,1,4,2,7,1],
        [3,7,1,3,4,4,7],
        [2,7,6,3,1,4,5],
        [1,3,3,7,7,5,1],
        [7,3,4,1,4,2,6],
        [2,6,6,5,2,1,1]
#from Brainbasher's Daily Hitory, 08/08/2021's 7x7 Medium
'''