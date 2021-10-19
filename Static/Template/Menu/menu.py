from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp as App


class Menu(MDBoxLayout):
    def on_readText(self, widget):
        try:
            brd = list(map(
                lambda s: list(map(int, s.split())),
                widget.text.strip().split('\n')
            ))
            n = len(brd)
            for row in brd:
                if len(row) != n:
                    raise Exception

        except:
            self.ids.invalidInput.text = 'The input is invalid!'
            return

        App.get_running_app().root.ids.main.ids.body.ids.board.make(brd)
        App.get_running_app().root.ids.nav_drawer.set_state('close')

    def on_restart(self):
        App.get_running_app().root.ids.main.ids.body.ids.board.clear()
        App.get_running_app().root.ids.nav_drawer.set_state('close')

    def on_newGame(self):
        #TODO: find a way to select the sizes from a list
        pass

