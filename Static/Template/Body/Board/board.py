from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivymd.app import MDApp as App
from ....Source.Manager.HSmanager import *
from ....Source.Classes.Lcell import Lcell


class Board(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init()
        self.clockHandler = None

    def init(self):
        self.cols = solver.game.m
        self.rows = solver.game.n

        self.cells = []
        self.hints = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells.append(Lcell(
                    j, i,
                    text=f'{solver.game.brd[i][j].data}',
                    font_size=40
                ))

                self.add_widget(self.cells[-1].label)

    def on_touch_down(self, touch):
        App.get_running_app().root.ids.main.ids.tail.ids.play.state='normal'
        if self.clockHandler is not None:
            self.clockHandler.cancel()
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
        self.hints = []

    def turn_cells_green(self):
        for cell in self.cells:
            if solver.game.brd[cell.y][cell.x].getType() == 1: cell.done()
            else: cell.draw()

    def toggle(self, state):
        if state == 'down':
            Clock.schedule_once(lambda _: self.play())
            self.clockHandler = Clock.schedule_interval(lambda _: self.play(), 3)
        else:
            self.clockHandler.cancel()

    def play(self):
        if App.get_running_app().root.ids.main.ids.tail.ids.play.state=='normal': return False
        if isGameFinished():
            App.get_running_app().root.ids.main.ids.tail.ids.play.state='normal'
            return False
        self.removeHints()
        step = solver.next()

        for xy in step[1]:
            #print(xy)
            cidx = self.cols*xy[1] + xy[0]
            #print(cidx, step[0])
            self.cells[cidx].toggle(stepToColor[step[0]])
            solver.print()

        for xy in step[2]:
            cidx = self.cols*xy[1] + xy[0]
            self.cells[cidx].drawHint()
            self.hints.append(self.cells[cidx])

        #TODO: if step[0] == -1 then some cells don't turn into green, needa fix this

        if isGameFinished():
            self.turn_cells_green()
            App.get_running_app().root.ids.main.ids.tail.ids.play.state='normal'
            return False

        return True

    def removeHints(self):
        while len(self.hints)>0:
            self.hints[-1].draw()
            self.hints.pop()

