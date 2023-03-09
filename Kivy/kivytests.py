from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.properties import StringProperty
import sqlite3 as db
import kivy
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial

class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class AmbulatoraisZurnals(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("test.kv")

class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()