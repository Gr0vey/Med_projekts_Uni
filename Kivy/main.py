from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
import sqlite3 as db
import kivy
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial

Config.set('input', 'mouse', 'mouse,disable_multitouch') #multitouch atslēgšana
kivy.require("2.0.0")

#with db.connect('datubaze.db') as con:
#    cur = con.execute("""SELECT * FROM """)
class LoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "admin" and self.ids["passw"].text == "admin":
            self.manager.current = "main"
class MainScreen(Screen):
    klase = StringProperty('Klase')

class AmbulatoraisZurnals(Screen):
    pass

class WindowManager(ScreenManager):
    pass

with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT * FROM skolenu_saraksts ORDER BY klase, klases_burts, vards_uzvards
    """)
    skoleni = cur.fetchall()
    #izveletais_skolens = skoleni[0][0]
    #print(izveletais_skolens)
class BoxlayoutEx(BoxLayout):
    klase = StringProperty('--klase--')
    def set_variable():
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM skolenu_saraksts WHERE skolena_id = {id}""")
            skolnieks = cur.fetchone()           
            print(skolnieks)
        klase = StringProperty(skolnieks[2]) #.\python.exe -m pip install sqlcipher3
        print()

class List(BoxLayout):
    klase = StringProperty('--klase--')
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
                        size=(dp(20),dp(25))#,
                        #on_press=  partial(self.set_variable,1[0])
                        ))

    def set_variable(self,id):
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM skolenu_saraksts WHERE skolena_id = {id}""")
            skolnieks = cur.fetchone()           
            print(skolnieks)
        klase = skolnieks[2]
        print(self.klase)
          
        #BoxlayoutEx.klase = '{}.{}'.format(skolnieks[1],skolnieks[2])
#partial(set_variables,i[0])
#def set_variables(skolena_id,a):
#    print(skolena_id)

    #def set_variables(self,id):
    #    print(skolena_id)
kv = Builder.load_file("main.kv")


class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()