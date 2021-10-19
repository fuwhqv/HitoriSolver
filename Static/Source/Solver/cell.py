class Cell:
    def __init__(self, val = 0, copyFrom = None):
        self.type = 0
        self.data = val

        if copyFrom is not None:
            self.type = copyFrom.type
            self.data = copyFrom.data

    def __eq__(self, o):
        return (self.type == o.type) and (self.data == o.data)

    def __ne__(self, o):
        return not (self == o)

    def toggleCW (self): self.type = (self.type+1)%3
    def toggleCCW(self): self.type = (self.type+2)%3

    def getData(self): return self.data
    def getType(self): return self.type

    def isEmpty(self): return self.type == 0
    def isWhite(self): return self.type == 1
    def isBlack(self): return self.type == 2

    def __repr__(self):
        ret = '['
        if   self.type == 0: ret += 'E'
        elif self.type == 1: ret += 'W'
        elif self.type == 2: ret += 'B'
        else: raise Exception('Corrupted Cell')
        ret += '%02d]'%self.data
        return ret

if __name__=='__main__':
#for module debugging
    a = Cell()
    b = Cell(2); b.toggleCCW()
    c = Cell(copyFrom=b); c.toggleCW()
    print(a, b, c)
    c.toggleCW()
    b.toggleCCW()
    print(a,b,c)