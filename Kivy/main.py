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

import colorConfig

from ctypes import windll, c_int64

windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
Config.set('input', 'mouse', 'mouse,disable_multitouch') #multitouch atslēgšana
kivy.require("2.0.0")

#===============================# Colors #===============================#

primaryWhite = colorConfig.primaryWhite         #FFFFFF
secondaryWhite = colorConfig.secondaryWhite     #EEEEF3
transparentGray = colorConfig.transparentGray

lightGray = colorConfig.lightGray               #C3C6D6
primaryGray = colorConfig.primaryGray           #4B4D58
primaryBlack = colorConfig.primaryBlack         #212227
secondaryBlack = colorConfig.secondaryBlack

primaryAccent = colorConfig.primaryAccent       #D864D9
accentGreen = colorConfig.accentGreen           #62C370
accentRed = colorConfig.accentRed               #D52941

Window.clearcolor = secondaryWhite
#===============================# Colors #===============================#

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def verify_credentials(self):
        if self.ids["login"].text == "" and self.ids["passw"].text == "":
            self.manager.current = "main"
            Window.maximize()
   

class MainScreen(Screen):
    pass

class AmbulatoraisZurnals(Screen):
    pass

class WindowManager(ScreenManager):
    primaryWhiteKV = ListProperty(colorConfig.primaryWhite)         #FFFFFF
    secondaryWhiteKV = ListProperty(colorConfig.secondaryWhite)     #EEEEF3
    transparentGrayKV = ListProperty(colorConfig.transparentGray)

    lightGrayKV = ListProperty(colorConfig.lightGray)               #C3C6D6
    primaryGrayKV = ListProperty(colorConfig.primaryGray)           #4B4D58
    primaryBlackKV = ListProperty(colorConfig.primaryBlack)         #212227
    secondaryBlackKV = ListProperty(colorConfig.secondaryBlack)

    primaryAccentKV = ListProperty(colorConfig.primaryAccent)       #D864D9
    accentGreenKV = ListProperty(colorConfig.accentGreen)           #62C370
    accentRedKV = ListProperty(colorConfig.accentRed)               #D52941

with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT * FROM skolenu_saraksts ORDER BY klase, klases_burts, vards_uzvards
    """)
    skoleni = cur.fetchall()

class IerakstiPopup(Popup):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.size_hint = (None,None)
        self.size = (800,400)
        self.title =f'{self.id}'
        #box = RoundedBox()
        #self.content(box)

class RoundedBox(BoxLayout):
    def __init__(self, box_color, corner_radius, image_source='', **kwargs):
        super().__init__(**kwargs) 
        self.box_color = box_color
        self.corner_radius = corner_radius
        with self.canvas.before:
            Color(rgba=self.box_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius= self.corner_radius, source= image_source, allow_stretch=False, keep_ratio=True)
            
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
            cur = con.execute(f"""SELECT * FROM ambulatorais_zurnals WHERE skolena_id = {id} ORDER BY date(datums, 'DD.MM.YY') ASC, time(laiks, 'HH:mm') ASC""")
            ieraksti = cur.fetchall()
            self.spacing = 5
            self.padding = 5
            for i in ieraksti:
                box = RoundedBox(orientation='horizontal', size_hint_y=None, height=230, box_color=primaryWhite, corner_radius=[10,])
                
                if i[8] == 'nav':
                    trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=accentGreen, corner_radius=[10,0,0,10])
                elif i[8] == 'ir':
                    trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=accentRed, corner_radius=[10,0,0,10])
                box.add_widget(trauma_box)
                
                main_content_box = BoxLayout(orientation='vertical',padding=(10,10,10,5))
                
                name_boxx = BoxLayout(size_hint_y=None, height=40)
                
                
                name = Label(text=f'{i[4]} {i[5]}', halign='left', valign='middle', padding=(5,5), text_size=(None, None),font_size=25,color=primaryBlack)
                name.bind(size=self.on_button_size)
                iesatijumi = Button(size_hint=(None,None),size=(60,60),color= primaryGray,
                                    background_normal = "..\\images\\editUp.png",
                                    background_down = "..\\images\\editDown.png",
                                    background_color = primaryGray)
                
                iesatijumi.bind(on_release=partial(self.set_variable,i))
                
                name_boxx.add_widget(name)
                name_boxx.add_widget(iesatijumi)
                main_content_box.add_widget(name_boxx)
                
                content_box = BoxLayout(orientation='horizontal',spacing=10,padding=10)
                si_un_pa_box = RoundedBox(orientation='vertical', box_color=secondaryWhite, corner_radius=[5,])
                
                content_simptomi = Label(text=f'{i[6]}',size_hint=(1,None), height=35, halign='left', valign='middle', padding=(5,5), text_size=(None, None),color=(primaryBlack))
                content_simptomi.bind(size=self.on_button_size)
                
                content_palidz = Label(text=f'{i[7]}', halign='left', valign='top', padding=(5,5), text_size=(None, None),color=(primaryBlack))
                content_palidz.bind(size=self.on_button_size)
                
                si_un_pa_box.add_widget(content_simptomi)
                si_un_pa_box.add_widget(content_palidz)
                content_box.add_widget(si_un_pa_box)
                
                piezimes_layout = RoundedBox(orientation='vertical', box_color=secondaryWhite, corner_radius=[5,])
                piezimes_box = Label(text=f'{i[9]}',size_hint=(0.4,1), halign='left', valign='top', padding=(5,5), text_size=(None, None),color=primaryBlack)
                piezimes_box.bind(size=self.on_button_size)
                
                piezimes_layout.add_widget(piezimes_box)
                content_box.add_widget(piezimes_layout)
                
                main_content_box.add_widget(content_box)
                
                time_box = Label(text=f'{i[3]} • {i[2]}',size_hint_y=None, height=20, halign='right', valign='middle', padding=(5,5), text_size=(None, None),color=primaryBlack)
                time_box.bind(size=self.on_button_size)
                
                main_content_box.add_widget(time_box)
                
                box.add_widget(main_content_box)
                
                self.add_widget(box)
            
    def on_button_size(self, instance, size):
        instance.text_size = size    
    
    def set_variable(self,id,button_object):
        IerakstiPopup(id=id).open()
                
class IzveidotIerakstu(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_press(self):
        popup_layout = BoxLayout()
        popup_button = Button(text='Close')
        popup_layout.add_widget(popup_button)
        popup = Popup(title='Ieraksta izveide', content=popup_layout, size_hint=(None, None), size=(600, 400),background="", separator_color=primaryAccent, title_color=primaryBlack)
        popup_button.bind(on_press=popup.dismiss)
        popup.open()
        
class Profile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def update(self,id):
        self.clear_widgets()
        
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM skolenu_saraksts WHERE skolena_id = {id}""")
            skolnieks = cur.fetchone()
     
            self.orientation = 'vertical'

            box = RoundedBox(box_color=primaryWhite ,corner_radius=[0,], orientation = 'vertical', image_source='..\\images\\background.png')

            name = Label(text=f'[b]{skolnieks[3]} {skolnieks[1]}.{skolnieks[2]}[/b]', size_hint_y = None, height= 120,  halign='center', valign='middle', padding=(5,5), text_size=(None, None), font_size=40, markup=True, color=primaryWhite)
            name.bind(size=self.on_button_size)

            main_content_box = BoxLayout(orientation='vertical')

            user_data = BoxLayout(orientation='horizontal',size_hint_y=None, height=150)

            nosaukumi = Label(text='Personas kods:\nDzimšanas dati:\nTelefona nummurs:\nMed. Karte:\nHroniskās slimības', halign='left', valign='top', padding=(10,10), text_size=(None, None), font_size=20, color=secondaryWhite)
            nosaukumi.bind(size=self.on_button_size)

            dati = Label(text=f'{skolnieks[4]}\n{skolnieks[5]}\n{skolnieks[6]}\n{skolnieks[7]}\n{skolnieks[8]}', height=150,halign='right', valign='top', padding=(10,10), text_size=(None, None), font_size=20, color=secondaryWhite)
            dati.bind(size=self.on_button_size)

            user_data.add_widget(nosaukumi)
            user_data.add_widget(dati)

            main_content_box.add_widget(user_data)

            piezimes_box = BoxLayout(orientation='vertical',padding=10)

            p_nosaukums = Label(text='Piezimes:',size_hint_y=None, height=40, halign='left', valign='top',padding=(10,10), text_size=(None, None), font_size=20, color=secondaryWhite)
            p_nosaukums.bind(size=self.on_button_size)

            piezimes = RoundedBox(box_color=transparentGray,corner_radius=[10,],padding=10)
            piezimes_text = Label(text=f'{skolnieks[9]}',text_size=(None, None), font_size=20,halign='left', valign='top',color=primaryWhite)
            piezimes_text.bind(size=self.on_button_size)
            
            piezimes.add_widget(piezimes_text)

            piezimes_box.add_widget(p_nosaukums)
            piezimes_box.add_widget(piezimes)

            main_content_box.add_widget(piezimes_box)

            tool_box = BoxLayout(orientation='horizontal',size_hint_y=None,height=80)
            filler = Label()
            tool_box.add_widget(filler)
            eddit_button = Button(color=lightGray,size_hint=(None,None),size=(60, 60),
                                background_normal = "..\\images\\userUp.png",
                                background_down = "..\\images\\userDown.png",
                                background_color = lightGray
                                )
            
            tool_box.add_widget(eddit_button)
            
            main_content_box.add_widget(tool_box)

            box.add_widget(name)
            box.add_widget(main_content_box)

            self.add_widget(box)
        
    def on_button_size(self, instance, size):
        instance.text_size = size
        
class SkoleniSearch(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.background_normal = "..\\images\\searchUp.png"
        self.background_down = "..\\images\\searchDown.png"
        self.background_color = primaryGray

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
                        color= primaryBlack,#Text color
                        background_normal=""
                        )
                self.add_widget(button)
                            
    def set_variable(self,id,button_object): # Metode, kura atbild par to lai informācija par skolēnu nomainās uz ekrāna
        #Window.toggle_fullscreen()
        #=========================================================================================================# Skolena info
        self.parent.parent.parent.parent.parent.ids.profile.update(id)
        #=========================================================================================================#

        #=========================================================================================================# Ierakstu info
        self.parent.parent.parent.parent.parent.ids.ieraksti.update(id)
        #=========================================================================================================#
          
kv = Builder.load_file("main.kv")


class MedSistēma(App):
    def build(self):
        Window.size = (400, 300)
        return kv

if __name__ == "__main__":
    MedSistēma().run()