from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.properties import StringProperty
import sqlite3 as db

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch') #multitouch atslēgšana

with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT klase, vards_uzvards, skolena_id FROM skolenu_saraksts
    """)
    skoleni = cur.fetchall()
    
class List(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in skoleni:
            self.add_widget(Button(
                    text=f'{i[0]} - {i[1]}',
                    text_size= (200,None),    
                    halign= 'left',
                    valign= 'bottom',
                    size_hint=(1,None),
                    size=(dp(20),dp(20))
                    ))
                
class BoxlayoutEx(BoxLayout):
    pass
class Aplikacija(App):
    pass


Aplikacija().run()