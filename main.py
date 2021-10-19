from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


from kivymd.app import MDApp as App
from kivy.lang import Builder


from wrapper import Wrapper
Builder.load_file('wrapper.kv')


class MainApp(App):
    def build(self):
        return Wrapper()


if __name__=='__main__':
    MainApp().run()

