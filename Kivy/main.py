from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import sqlite3 as db
import kivy
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from functools import partial
from kivy.clock import Clock
from kivy.uix.popup import Popup

from ctypes import windll, c_int64

windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
Config.set('input', 'mouse', 'mouse,disable_multitouch') #multitouch atslēgšana
kivy.require("2.0.0")

#===============================# Colors #===============================#

primaryWhite = (250/255, 250/255, 255/255, 1)   #FAFAFF
secondaryWhite = (223/255, 223/255, 230/255, 1) #DFDFE6
black = (48/255, 52/255, 63/255, 1)             #30343F
textBlack = (41/225, 41/225, 40/255, 1)         #292928
accent1 = (17/255, 138/255, 178/255, 1)         #118AB2
accent2 = (239/255, 71/255, 111/255, 1)         #EF476F
accent3 = (6/255, 214/255, 160/255, 1)          #06D6A0
accent4 = (178/255, 73/255, 179/255, 1)         #b249b3 #d864d9

Window.clearcolor = secondaryWhite
#===============================# Colors #===============================#

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    accent1k = ListProperty(accent4)

    def verify_credentials(self):
        if self.ids["login"].text == "" and self.ids["passw"].text == "":
            self.manager.current = "main"
   

class MainScreen(Screen):
    klase = StringProperty('Klase:\n')
    vards = StringProperty('Vards Uzvards:\n')
    pk = StringProperty('Personas kods:\n')
    dzimsanas_d = StringProperty('Dzimšanas dati:\n')
    tel = StringProperty('Telefona nummurs:\n')
    med = StringProperty('Med. karte:\n')
    slimibas = StringProperty('Hroniskās slimības:\n')
    piezimes = StringProperty('Piezīmes:\n')
    accent1k = ListProperty(accent4)

class AmbulatoraisZurnals(Screen):
    pass

class WindowManager(ScreenManager):
    pass

with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT * FROM skolenu_saraksts ORDER BY klase, klases_burts, vards_uzvards
    """)
    skoleni = cur.fetchall()
    
class RoundedBox(BoxLayout):
    def __init__(self, box_color, corner_radius, **kwargs):
        super().__init__(**kwargs) 
        self.box_color = box_color
        self.corner_radius = corner_radius
        with self.canvas.before:
            Color(rgba=self.box_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius= self.corner_radius)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        
    def update_canvas(self, *args):
        Color(rgba=self.box_color)
        self.corner.pos = self.pos
        self.corner.size = self.size
        
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=primaryWhite)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=[5,])
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
    
    def change_color(self,time):
        with self.canvas.before:
            Color(rgba=primaryWhite)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=[5,])
            #print(time) laiks kas tika padots
             
    def on_press(self):
        with self.canvas.before:
            Color(rgba=secondaryWhite)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=[5,])
            Clock.schedule_once(self.change_color, 0.05)
            
    def update_canvas(self, *args):
        global black
        Color(rgba=primaryWhite)
        self.corner.pos = self.pos
        self.corner.size = self.size

class Ieraksti(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

    def update(self,id):
        self.clear_widgets()
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM ambulatorais_zurnals WHERE skolena_id = {id}""")
            ieraksti = cur.fetchall()
            self.spacing = 1
            for i in ieraksti:
                box = RoundedBox(orientation='horizontal', size_hint_y=None, height=230, box_color=(1,1,1,1), corner_radius=[10,])
            
                if i[8] == 'nav':
                    trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=(0,1,.5,1), corner_radius=[10,0,0,10])
                elif i[8] == 'ir':
                    trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=(1,0,.3,1), corner_radius=[10,0,0,10])
                box.add_widget(trauma_box)
                
                main_content_box = BoxLayout(orientation='vertical')
                
                name_boxx = BoxLayout(size_hint_y=None, height=30)
                
                
                name = Label(text=f'{i[4]} {i[5]}', halign='left', valign='middle', padding=(5,5), text_size=(None, None),font_size=25,color=textBlack)
                name.bind(size=self.on_button_size)
                
                name_boxx.add_widget(name)
                main_content_box.add_widget(name_boxx)
                
                content_box = BoxLayout(orientation='horizontal',spacing=10,padding=10)
                si_un_pa_box = RoundedBox(orientation='vertical', box_color=(.9,.9,.93,1), corner_radius=[5,])
                
                content_simptomi = Label(text=f'{i[6]}',size_hint=(1,None), height=35, halign='left', valign='middle', padding=(5,5), text_size=(None, None),color=textBlack)
                content_simptomi.bind(size=self.on_button_size)
                
                content_palidz = Label(text=f'{i[7]}', halign='left', valign='top', padding=(5,5), text_size=(None, None),color=textBlack)
                content_palidz.bind(size=self.on_button_size)
                
                si_un_pa_box.add_widget(content_simptomi)
                si_un_pa_box.add_widget(content_palidz)
                content_box.add_widget(si_un_pa_box)
                
                piezimes_layout = RoundedBox(orientation='vertical', box_color=(.9,.9,.93,1), corner_radius=[5,])
                piezimes_box = Label(text=f'{i[9]}',size_hint=(0.4,1), halign='left', valign='top', padding=(5,5), text_size=(None, None),color=textBlack)
                piezimes_box.bind(size=self.on_button_size)
                
                piezimes_layout.add_widget(piezimes_box)
                content_box.add_widget(piezimes_layout)
                
                main_content_box.add_widget(content_box)
                
                time_box = Label(text=f'{i[3]} • {i[2]}',size_hint_y=None, height=20, halign='right', valign='middle', padding=(5,5), text_size=(None, None), color=textBlack)
                time_box.bind(size=self.on_button_size)
                
                main_content_box.add_widget(time_box)
                
                box.add_widget(main_content_box)
                
                self.add_widget(box)
            
    def on_button_size(self, instance, size):
        instance.text_size = size    
                
class IzveidotIerakstu(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_press(self):
        popup_layout = BoxLayout()
        popup_button = Button(text='Close')
        popup_layout.add_widget(popup_button)
        popup = Popup(title='Ieraksta izveide', content=popup_layout, size_hint=(None, None), size=(600, 400),background="",separator_color=accent3,title_color=textBlack)
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

class SkoleniSearch(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.background_normal = "..\\images\\searchUp.png"
        self.background_down = "..\\images\\searchUp.png"
        self.color = black
        self.background_color = (0.2,0.2,0.2,1)

class List(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
        self.spacing = 1
        self.padding = 1
        for i in skoleni:
            if i[10] == 1:#Parbaude vai skolnieks ir arhivēts
                button = RoundedButton(
                        text=f'{i[1]}.{i[2]} - {i[3]}',
                        text_size= (200,None),    
                        halign= 'left',
                        valign= 'bottom',
                        size_hint=(1,None),
                        size=(dp(20),dp(50)),
                        on_press=  partial(self.set_variable,i[0]),
                        background_color = (0,0,0,0),#Color of the button
                        color= textBlack,#Text color
                        background_normal=""
                        )
                self.add_widget(button)
                            
    def set_variable(self,id,button_object): # Metode, kura atbild par to lai informācija par skolēnu nomainās uz ekrāna

        #=========================================================================================================# Skolena info
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM skolenu_saraksts WHERE skolena_id = {id}""")
            skolnieks = cur.fetchone()            
            self.parent.parent.parent.parent.parent.ids.klase.text = f'{skolnieks[1]}.{skolnieks[2]}' # klases nummurs
            self.parent.parent.parent.parent.parent.ids.vards.text = f'{skolnieks[3]}' # vards uzvards
            self.parent.parent.parent.parent.parent.ids.pk.text = f'{skolnieks[4]}' # personas kods
            self.parent.parent.parent.parent.parent.ids.dzimsanas_d.text = f'{skolnieks[5]}' # dzimšanas dati
            self.parent.parent.parent.parent.parent.ids.tel.text = f'{skolnieks[6]}' # telefons
            self.parent.parent.parent.parent.parent.ids.med.text = f'{skolnieks[7]}' # med karte
            self.parent.parent.parent.parent.parent.ids.slimibas.text = f'{skolnieks[8]}' # hroniskās slimības
        #=========================================================================================================#

        #=========================================================================================================# Ierakstu info
        self.parent.parent.parent.parent.parent.ids.ieraksti.update(id)
        #=========================================================================================================#
          
kv = Builder.load_file("main.kv")


class MedSistēma(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MedSistēma().run()