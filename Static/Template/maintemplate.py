from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


from .Head.head import Head
from .Body.body import Body
from .Tail.tail import Tail
from .Menu.menu import Menu
Builder.load_file('Static/Template/Head/head.kv')
Builder.load_file('Static/Template/Body/body.kv')
Builder.load_file('Static/Template/Tail/tail.kv')
Builder.load_file('Static/Template/Menu/menu.kv')


class MainTemplate(BoxLayout):
    pass

