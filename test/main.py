from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

class MainMenu(Screen):
    name = StringProperty('main_menu')

class OtherMenu(Screen):
    name = StringProperty('other_menu')

class RootWidget(Widget):
    n = 1
    state = StringProperty('set_main_menu_state')
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if value == 'main_menu':
            self.screen_manager.current = 'main_menu'

    def set_state(self, state):
        if state == 'main_menu':
            if self.n == 5:
                self.screen_manager.current = 'other_menu'
            self.n += 1
        if state == 'other_menu':
            self.screen_manager.current = 'main_menu'


class TestApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    TestApp().run()