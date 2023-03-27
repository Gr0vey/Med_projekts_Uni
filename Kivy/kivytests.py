import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(BoxLayout):

    def login(self, instance):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if username == 'admin' and password == 'password':
            print('Access granted')
        else:
            print('Access denied')


class MyApp(App):

    def build(self):
        Builder.load_file('test.kv')
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
