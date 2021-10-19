from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from ....Source.Manager.HSmanager import *
from ....Source.Classes.Lcell import Lcell


class Board(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init()

    def init(self):
        self.cols = solver.game.m
        self.rows = solver.game.n

        self.cells = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells.append(Lcell(
                    j, i,
                    text=f'{solver.game.brd[i][j].data}',
                    font_size=40
                ))

                self.add_widget(self.cells[-1].label)

    def on_touch_down(self, touch):
        if isGameFinished(): return
        for cell in self.cells:
            if not cell.isTouched(touch): continue

            if touch.button == 'left':
                cell.toggle(1)
                toggleCW(cell.x, cell.y)
            elif touch.button == 'right':
                cell.toggle(2)
                toggleCCW(cell.x, cell.y)
            
            if isGameFinished(): self.turn_cells_green()

    def make(self, brd):
        for cell in self.cells:
            self.remove_widget(cell.label)
        makeGame(brd)
        self.init()

    def skip(self):
        if isGameFinished(): return
        solver.clear()
        solver.solve()
        for cell in self.cells:
            while cell.cidx != solver.game.brd[cell.y][cell.x].getType():
                cell.toggle()
        if isGameFinished(): self.turn_cells_green()

    def clear(self):
        solver.clear()
        for cell in self.cells:
            while cell.cidx != 0:
                cell.toggle()

    def turn_cells_green(self):
        for cell in self.cells:
            if solver.game.brd[cell.y][cell.x].getType() != 1: continue
            cell.done()

    def play(self):
        #TODO: step by step solution
        print('play')

