from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp as App


class Tail(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_menu(self):
        App.get_running_app().root.ids.menu.ids.invalidInput.text=''
        App.get_running_app().root.ids.nav_drawer.set_state('open')

    def on_play(self, widget): widget.play()
    def on_skip(self, widget): widget.skip()

