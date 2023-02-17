from kivy.app import App
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

from functools import partial

Config.set('input', 'mouse', 'mouse,disable_multitouch') #multitouch atslēgšana
kivy.require("2.0.0")

with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT * FROM skolenu_saraksts ORDER BY klase, klases_burts, vards_uzvards
    """)
    skoleni = cur.fetchall()
    #izveletais_skolens = skoleni[0][0]
    #print(izveletais_skolens)

class List(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in skoleni:
            if i[10] == 1:
                self.add_widget(Button(
                        text=f'{i[1]}.{i[2]} - {i[3]}',
                        text_size= (200,None),    
                        halign= 'left',
                        valign= 'bottom',
                        size_hint=(1,None),
                        size=(dp(20),dp(25)),
                        on_press= partial(set_variables,i[0])
                        ))
                
def set_variables(skolena_id,a):
    print(skolena_id)
                
class BoxlayoutEx(BoxLayout):
    pass
class Aplikacija(App):
    pass

Aplikacija().run()