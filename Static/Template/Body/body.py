from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


from .Board.board import Board
Builder.load_file('Static/Template/Body/Board/board.kv')


class Body(BoxLayout):
    pass

