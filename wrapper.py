from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


from Static.Template.maintemplate import MainTemplate
Builder.load_file('Static/Template/maintemplate.kv')


class Wrapper(MDScreen):
    pass