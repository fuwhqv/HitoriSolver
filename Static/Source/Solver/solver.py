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
        self.sidx = 0
        self.steps = [self.step0,
                      self.step1,
                      self.step2,
                      self.step3,
                      self.step4,
                      self.step5,
                      self.step6,
                      self.step7,
                      self.stepX
                     ]
        self.ridx = 0
        self.cidx = -1

    def __repr__(self): return self.game.__repr__()
    def isFinished(self): return self.game.isFinished()
    def print(self): self.game.print()
    def printColorsOnly(self): self.game.printColorsOnly()

    def setBoard(self, brd:Board):
        self.game = brd
        self.sidx = 0
        self.ridx = 0
        self.cidx = -1

    def clear(self):
        self.game.clear()
        self.sidx = 0
        self.ridx = 0
        self.cidx = -1

    def toggleAdjEmptyToWhite(self, x, y):
        if not self.game.brd[y][x].isBlack(): return None
        res = [2, [], [(x,y)]]
        for [dx, dy] in dxy:
            [nx, ny] = [x+dx, y+dy]
            if not self.game.isInBoard(nx, ny): continue
            if not self.game.brd[ny][nx].isEmpty(): continue
            self.game.brd[ny][nx].toggleCW()
            res[1].append((nx,ny))
        return res

    def toggleFacingDupToBlack(self, x, y):
        if not self.game.brd[y][x].isWhite(): return None
        res = [1, [], [(x,y)]]
        for [dx, dy] in dxy:
            [nx, ny] = [x, y]
            while True:
                nx += dx; ny += dy
                if not self.game.isInBoard(nx, ny): break
                #print(x,y,nx,ny)
                if not self.game.brd[ny][nx].isEmpty(): continue
                if self.game.brd[ny][nx].getData() == self.game.brd[y][x].getData():
                    self.game.brd[ny][nx].toggleCCW()
                    res[1].append((nx,ny))
        return res

    def stepX(self, x, y):
        #Step X: make a copy and brute-force
        if not self.game.brd[y][x].isEmpty(): return None
        temp = Solver()
        temp.setBoard(copy.deepcopy(self.game))
        temp.game.brd[y][x].toggleCW()
        temp.solve()
        if temp.game.isFinished():
            self.game = temp.game
            return [-2, [(x,y)], []]
        #print('did something at (%d,%d)!'%(x, y))
        self.game.brd[y][x].toggleCCW()
        return [-1, [(x,y)], []]

    def step0(self, x, y):
        #Step 0: find empty which cannot be dup and toggle it to white
        if not self.game.brd[y][x].isEmpty(): return None
        for i in range(self.game.n):
            if y == i: continue
            if((self.game.brd[i][x].getData() == self.game.brd[y][x].getData())
            and (not self.game.brd[i][x].isBlack())): return None
        for j in range(self.game.m):
            if j == x: continue
            if((self.game.brd[y][j].getData() == self.game.brd[y][x].getData())
            and (not self.game.brd[y][j].isBlack())): return None
        self.game.brd[y][x].toggleCW()
        return [0, [(x,y)], []]

    def step1(self, x, y):
        #Step 1: find any possible dup and toggle to black
        #if not self.game.brd[y][x].isWhite(): return
        return self.toggleFacingDupToBlack(x, y)

    def step2(self, x, y):
        #Step 2: find any empty adj to black and toggle to white
        #if not self.game.brd[y][x].isBlack(): return
        return self.toggleAdjEmptyToWhite(x, y)

    def step3(self, x, y):
        #Step 3: find any dup with only one empty between and toggle the one to white
        for [dx, dy] in dxy[:2]:
            nx = x + dx * 2; ny = y + dy * 2
            if not self.game.isInBoard(nx, ny): continue
            if self.game.brd[y][x].getData() == self.game.brd[ny][nx].getData():
                if self.game.brd[y+dy][x+dx].isEmpty():
                    self.game.brd[y+dy][x+dx].toggleCW()
                    return [3, [(x+dx,y+dy)], [(x,y), (nx,ny)]]
        return None

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
                        return [4, [(tx,ty)], [(x,y), (ax,ay)]]
        return None

    def step5(self, x, y):
        #Step 5: find any empty which can cut the white group into to, toggle it to white
        if not self.game.brd[y][x].isEmpty(): return None
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
            return [5, [(x,y)], []]
        self.game.brd[y][x].toggleCW()
        return None

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
        #toggle the last one to black
        #ex: 1 4 1 5 6 5 1 => the leftmost 1 is must be Black - if not, two 5s gonna conflict
        if not self.game.brd[y][x].isEmpty(): return None
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
                        return [6, [(x,y)], [(ax,ay), (bx,by), (adx,ady), (bdx, bdy)]]
        return None

    def step7(self, x, y):
        #Step 7: Similarly with step 6, find a pair of duplicate neighboring each other,
        #and then find another duplicate which is in orthogonal,
        #seemingly shapes like L. Target cell is the shared one.
        #check if two cells other than the target cell neighbors same number in the same line.
        #if yes, toggle the target cell to black.
        #ex) 1 4 2 5 1  <<in this case, if target cell is not black, the two 2s will conflict.
        #    2 3 5 2 1
        if not self.game.brd[y][x].isEmpty(): return None
        for [dx, dy] in dxy:
            ax = x + dx; ay = y + dy
            if not self.game.isInBoard(ax, ay): continue
            if self.game.brd[y][x].getData() != self.game.brd[ay][ax].getData(): continue
            bdx = dy * dy; bdy = dx * dx
            bx = x * bdy - bdx; by = y * bdx - bdy
            while True:
                bx += bdx; by += bdy
                if not self.game.isInBoard(bx, by): break
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
                                #print('did something at (%d,%d)!'%(x, y))
                                #self.printColorsOnly()
                                return [7, [(x,y)], [(ax,ay), (bx,by), (px,py), (qx,qy)]]
        return None
 
    def solve(self):
        steps = self.steps
        idx = 0

        while not self.isFinished():
            if idx >= len(steps): break
            prev = copy.deepcopy(self.game.brd)

            iloop = True
            for i in range(self.game.n):
                if not iloop: break

                for j in range(self.game.m):
                    res = steps[idx](j, i)
                    #if res is not None and len(res[1])>0:
                        #print(res)
                        #self.print()
                    if not isEqual(prev, self.game.brd):
                        idx = 1
                        iloop = False
                        break

            #print(('step%d: '%idx)+str(self.isFinished()))
            idx = idx+1 if isEqual(prev, self.game.brd) else 1
            #self.printColorsOnly()

    def next(self):
        while True:
            self.cidx += 1
            if self.cidx >= self.game.m:
                self.cidx = 0
                self.ridx += 1
            if self.ridx >= self.game.n:
                self.ridx = 0
                self.sidx += 1
            if self.sidx >= len(self.steps):
                self.sidx = 1
            res = self.steps[self.sidx](self.cidx, self.ridx)

            if res is None: continue
            if len(res[1]) == 0: continue

            if not self.sidx==0:
                self.sidx = 1
                self.cidx = -1
                self.ridx = 0

            return res


def isEqual(a, b):
    for arow, brow in zip(a, b):
        for aval, bval in zip(arow, brow):
            if aval != bval: return False
    return True

