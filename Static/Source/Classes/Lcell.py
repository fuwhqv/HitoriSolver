from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


bcolors = [(.5, .5, .5,  1), ( 1,  1,  1,  1),
           ( 0,  0,  0,  1), (.5,  1, .5,  1)]
fcolors = [( 0,  0,  0,  1), ( 0,  0,  0,  1),
           ( 1,  1,  1,  1), ( 0,  0,  0,  1)]


class Lcell:
    def __init__(self, x: int, y: int, **kwargs):
        self.x = x
        self.y = y
        self.cidx = 0
        self.label = Label(**kwargs)
        self.label.color = fcolors[self.cidx]
        self.bgColor = bcolors[self.cidx]

        self.draw()

        def update(lab, *args):
            lab.rect.pos = lab.pos
            lab.rect.size = lab.size

        self.label.bind(pos = update, size = update)

    def toggle(self, n: int=1): #1: CW, 2: CCW
        if not n in [1, 2]:
            raise Exception('invalid toggle value')
        self.cidx = (self.cidx+n)%3
        self.label.color = fcolors[self.cidx]
        self.bgColor = bcolors[self.cidx]

        self.draw()

    def isTouched(self, touch):
        return self.label.collide_point(*touch.pos)

    def done(self):
        self.cidx = 3
        self.label.color = fcolors[self.cidx]
        self.bgColor = bcolors[self.cidx]
        self.draw()

    def draw(self):
        self.label.canvas.before.clear()
        with self.label.canvas.before:
            Color(*self.bgColor)
            self.label.rect = Rectangle(pos = self.label.pos, size = self.label.size)

