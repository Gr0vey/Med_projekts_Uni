from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import sqlite3 as db
import kivy
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from functools import partial
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from ctypes import windll, c_int64
import ast
from UIcolors import *
from datetime import datetime
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.spinner import Spinner
import os
import pandas as pd

windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))  # DPI scaling adjustment
Config.set('input', 'mouse', 'mouse,disable_multitouch')  # Disable multitouch
Config.set('graphics', 'custom_titlebar', '1')
Config.set('graphics', 'maxfps', '60')  # Limit FPS for performance
Config.set('graphics', 'vsync', '1')  # Enable vsync

kivy.require("2.0.0")
active_skolens = -1

#===============================# Additional functioanality #===============================#
def rgb_to_kivy(color): # Funkcija kas parveido rgb hex formata krāsu Kivy piemerotā formātā
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    a = int(color[7:9], 16) if len(color) == 9 else 255
    return (r/255, g/255, b/255, a/255)

def parse_date_time(date_str, time_str):
    # Assuming date_str is in format DD.MM.YY and time_str is in format HH:mm
    return datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %H.%M")

def max_row_length(arr_2d):
    max_length = 0
    for row in arr_2d:
        row_length = len(row)
        if row_length > max_length:
            max_length = row_length

    return max_length

def sort_data_by_date_time(data_array, date_index, time_index, reverse=True):
    return sorted(data_array, key=lambda x: parse_date_time(x[date_index], x[time_index]), reverse=reverse)
#===========================================================================================#

#===============================# Colors #===============================#
Window.clearcolor = white_c[0]
#===============================# Colors #===============================#

#===============================# Screen managment #===============================#
class MainScreen(Screen):
    pass

class AmbulatoraisZurnals(Screen):
    pass

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Disable transitions for better performance
        self.transition = NoTransition()
    
    main_c   = main_c
    red_c    = red_c
    green_c  = green_c
    blue_c   = blue_c
    yellow_c = yellow_c
    white_c  = white_c
    gray_c   = gray_c
    black_c  = black_c
    transparent = (0,0,0,0)
#===============================# Screen managment #===============================#

#===============================# Building components #===============================#
class RoundedBox(BoxLayout):
    def __init__(self, box_color=gray_c[0], corner_radius=[0,], image_source='', outline_width=0, outline_color=transparent, **kwargs):
        super().__init__(**kwargs) 
        self.box_color = box_color
        self.corner_radius = corner_radius
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.image_source = image_source
        
        with self.canvas.before:
            Color(rgba=self.box_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius= self.corner_radius, source= self.image_source, allow_stretch=False, keep_ratio=True)
            Color(rgba=self.outline_color)
            self.outline = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.corner_radius[0]), width=self.outline_width)
            
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.corner.pos = self.pos
        self.corner.size = self.size
        
        self.outline.rounded_rectangle = (self.x, self.y, self.width, self.height, self.corner_radius[0])

###
class CostumButton(Button):
    def __init__(self, button_color=white_c[0], corner_radius=[5,], image_source='', outline_width=0, outline_color=transparent, **kwargs):
        super().__init__(**kwargs)
        self.button_color = button_color
        self.corner_radius = corner_radius
        self.background_normal,self.background_down = image_source,image_source
        self.background_color = (0,0,0,0)
        self.outline_width = outline_width
        self.outline_color = outline_color
        
        
        with self.canvas.before:
            Color(rgba= self.button_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius= self.corner_radius, source= image_source, allow_stretch=False, keep_ratio=True)
            Color(rgba=self.outline_color)
            self.outline = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.corner_radius[0]), width=self.outline_width)
            
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

    def change_color(self,time):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba= self.button_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius)

    def on_press(self):
        with self.canvas.before:
            Color(rgba= [a + b for a, b in zip(self.button_color, [-0.2,-0.2,-0.2,0])])
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius)
            Clock.schedule_once(self.change_color, 0.05)
            
    def update_canvas(self, *args):
        self.corner.pos = self.pos
        self.corner.size = self.size
        self.outline.rounded_rectangle = (self.x, self.y, self.width, self.height, self.corner_radius[0])

class CostumToggleButton(BoxLayout):
    def __init__(self, normal_color=gray_c[0], down_color=red_c[2], corner_radius=[0], image_source='', state='normal', text='', **kwargs):
        super().__init__(**kwargs)
        self.normal_color = normal_color
        self.down_color = down_color
        
        self.state = state
        
        self.corner_radius = corner_radius
        self.image_source = image_source
        
        self.toggle_button = ToggleButton(text=text, size_hint=(1, 1),background_color=transparent,state=state)
        self.toggle_button.bind(on_press=self.on_toggle)

        with self.canvas.before:
            if self.state == 'normal' : self.color_instruction = Color(rgba=self.normal_color)
            else:                       self.color_instruction = Color(rgba=self.down_color)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius,
                                        source=self.image_source, allow_stretch=False, keep_ratio=True)

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.add_widget(self.toggle_button)

    def on_toggle(self, instance):
        if instance.state == 'down':
            instance.text = 'Ir'
            self.color_instruction.rgba = self.down_color
        else:
            instance.text = 'Nav'
            self.color_instruction.rgba = self.normal_color
        self.update_canvas()

    def update_canvas(self, *args):
        self.corner.pos = self.pos
        self.corner.size = self.size          

#=====================================================================================#

#===============================# Popups #===============================#
class File_display(Popup):
    def __init__(self, records, **kwargs):
        super().__init__(**kwargs)
        self.records = records
        
        self.size_hint = (None,None)
        self.size = (1000,600)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        
        self.main_box = BoxLayout(orientation = 'vertical')
        self.content = self.main_box
        
        self.main_box.add_widget(Label(text='Kolonnu izvēle:',size_hint=(None,None),size=(200,40)))
        
        top_row = BoxLayout(orientation = 'horizontal',size_hint_y=None, height=40)
        for i in range(max_row_length(self.records)):
            drop_button = Spinner(text='-izvēlēties kolonnu-',
                                  values=['Klase',
                                          'Vārds Uzvārds',
                                          'Personas kods',
                                          'Telefona nummurs',
                                          'Dzimšanas datums'])
                
            top_row.add_widget(drop_button)
        self.main_box.add_widget(top_row)
        
        self.main_box.add_widget(Label(text='Datu priekšskats:',size_hint=(None,None),size=(200,40)))
        
        bottom_row = BoxLayout(orientation = 'vertical')
        
        if len(self.records)<5:
            show_count = len(self.records)
        else:
            show_count = 5
            
        for i in range(show_count):
            temp_layout = BoxLayout(orientation = 'horizontal')
            for j in range(max_row_length(self.records)):
                temp_layout.add_widget(Label(text=f'{self.records[i][j]}'))
            bottom_row.add_widget(temp_layout)
        self.main_box.add_widget(bottom_row)
        
        commit = Button(text='Commit',size_hint=(None,None),size=(200,40),
                        on_release=self.dismiss)
        self.main_box.add_widget(commit)
        
class Choose_file(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint = (None,None)
        self.size = (1000,600)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        self.main_box = BoxLayout(orientation = 'vertical')
        self.content = self.main_box
        
        self.file_view = FileChooserListView(path = os.path.expanduser("~"),
                                            filters=['*.xlsx', '*.csv'])
        self.main_box.add_widget(self.file_view)
        
        choice_button = Button(text='open',size_hint = (None,None), size = (100,40))
        choice_button.bind(on_press=self.select_file)
        self.main_box.add_widget(choice_button)
        
    def select_file(self, instance):
        selected_file = self.file_view.selection
        if selected_file:
            file_path = selected_file[0]
            
            if file_path.lower().endswith(".xlsx"): # ================= # .xlsx files
                try:
                    data = pd.read_excel(file_path).values.tolist()
                    print(data)
                    File_display(data).open()
                    
                except Exception as e:
                    print(f"Failed to read XLSX file: {str(e)}")
                
                self.dismiss()
                
            elif file_path.lower().endswith(".csv"): # ================= # .csv files
                try:
                    data = pd.read_csv(file_path)
                    print("This is a CSV file turned into a 2D array:")
                    print(data)
                except Exception as e:
                    print(f"Failed to read CSV file: {str(e)}")
                    
class IerakstiPopup(Popup):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.size_hint = (None,None)
        self.size = (1200,800)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        self.background_color = (0,0,0,0)
        
        box = RoundedBox(box_color = white_c[0], corner_radius = [10,], orientation='vertical')
        
        top_panel = RoundedBox(orientation='horizontal',
                                padding=20,
                                spacing=20,
                                size_hint_y=None,
                                height=90,
                                corner_radius=[10,10,0,0],
                                box_color=black_c[0])
        
        name = Label(text=f'[b]{id[4]} {id[5]}[/b]',color=white_c[0],
                     font_size=30,
                     markup=True,
                     valign='center')
        name.bind(size=self.on_button_size)
        
        discard_button = CostumButton(text='//',
                                      color=white_c[0],
                                      button_color=red_c[2],
                                      corner_radius=[10,],
                                      size_hint_x=None,
                                      width=50,
                                      on_release=self.delete_record)
        
        top_panel.add_widget(name)
        top_panel.add_widget(discard_button)
        
        main_panel = BoxLayout(orientation='horizontal',
                               padding=20,
                               spacing=30)
        
        #====== Sgnietā palīdzība un Simptomi ====#
        content1 = BoxLayout(orientation='vertical',spacing=10)
        
        simptomi_label = Label(text='Simptomi:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        simptomi_label.bind(size=self.on_button_size)
        
        simptomi_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        simptomi = TextInput(text=f'{id[6]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        
        sniegta_p_label = Label(text='Sniegtā Palīdzība:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        sniegta_p_label.bind(size=self.on_button_size)
        
        sniegta_p_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        sniegta_p = TextInput(text=f'{id[7]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        
        content1.add_widget(simptomi_label)
        simptomi_holder.add_widget(simptomi)
        content1.add_widget(simptomi_holder)
        
        content1.add_widget(sniegta_p_label)
        sniegta_p_holder.add_widget(sniegta_p)
        content1.add_widget(sniegta_p_holder)
        
        main_panel.add_widget(content1)
        #=========================================#
        
        #====== Piezīmes un pārējie parametri ====#
        content2 = BoxLayout(orientation='vertical',spacing=20)
        
        piezimes_content = BoxLayout(orientation='vertical',spacing=10)
        
        piezimes_label = Label(text='Piezīmes:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        piezimes_label.bind(size=self.on_button_size)
        
        piezimes_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        piezimes = TextInput(text=f'{id[9]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        piezimes_holder.add_widget(piezimes)
        
        piezimes_content.add_widget(piezimes_label)
        piezimes_content.add_widget(piezimes_holder)
        
        trauma_time = BoxLayout(orientation='horizontal',spacing=20, size_hint_y=None, height=160)
        
        trauma_boxx = BoxLayout(orientation='horizontal')
        trauma_label = Label (text='Trauma',color=black_c[1])
        
        if self.id[8] == 'Ir':
            trauma_toggle = CostumToggleButton(text='Ir',state='down',corner_radius=[10,])
        else:
            trauma_toggle = CostumToggleButton(text='Nav',state='normal',corner_radius=[10,])
        
        trauma_boxx.add_widget(trauma_label)
        trauma_boxx.add_widget(trauma_toggle)
        
        time_date = BoxLayout(orientation='vertical',spacing=10)
        
        time_label = Label(text='Laiks:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        time_label.bind(size=self.on_button_size)
        
        time_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        time = TextInput(text=f'{id[3]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent,
                            multiline=False)
        time_holder.add_widget(time)
        
        time_date.add_widget(time_label)
        time_date.add_widget(time_holder)
        
        
        date_label = Label(text='Laiks:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        date_label.bind(size=self.on_button_size)
        
        date_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        date = TextInput(text=f'{id[2]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent,
                            multiline=False)
        date_holder.add_widget(date)
        
        time_date.add_widget(date_label)
        time_date.add_widget(date_holder)
        
        trauma_time.add_widget(trauma_boxx)
        trauma_time.add_widget(time_date)
        
        content2.add_widget(piezimes_content)
        content2.add_widget(trauma_time)
        main_panel.add_widget(content2)

        self.inputs = [simptomi, sniegta_p, piezimes, time, date, trauma_toggle.toggle_button]
              
        action_panel = BoxLayout(orientation='horizontal',
                                 padding=20,
                                 spacing=20,
                                 size_hint=(None,None),
                                 height=90,
                                 width=500,
                                 pos_hint={"right": 1})
        
        cancel_button = CostumButton(background_color = (0,0,0,0),
                                      color= black_c[1],
                                      background_normal="",
                                      text='Atcelt',
                                      corner_radius=[10,],
                                      button_color=white_c[0],
                                      outline_color=gray_c[1],
                                      outline_width=0,
                                      on_release=self.dismiss)

        save_button = CostumButton(background_color = (0,0,0,0),
                                      color= white_c[0],
                                      background_normal="",
                                      text='Saglabāt',
                                      corner_radius=[10,],
                                      button_color=main_c[2],
                                      on_release=self.save_record)
        
        action_panel.add_widget(cancel_button)
        action_panel.add_widget(save_button)
        
        box.add_widget(top_panel)
        box.add_widget(main_panel)
        box.add_widget(action_panel)
        
        self.content = box
        
    def on_button_size(self, instance, size):
        instance.text_size = size
    
    def delete_record(self, instance):
        with db.connect('datubaze.db') as con:
            con.execute(f"""DELETE FROM ambulatorais_zurnals WHERE ieraksta_id = {self.id[0]}""")
            
        App.get_running_app().root.get_screen('main').ids.ieraksti.update(self.id[1]) # Iegūst saraksta metodi un izmanto
        
        Clock.schedule_once(lambda dt: self.dismiss(), 0.1) # Taimeris kurš aizver logu
        
    def save_record(self, instance):
        output = []
        for i in self.inputs:
            output.append(i.text)
        #['Simptomi', 'Sniegtā palīdzība', 'Bez piezīmēm', '11:03', '19.4.2023', 'Nav']
        with db.connect('datubaze.db') as con:
            query = """UPDATE ambulatorais_zurnals SET 
            datums = ?, 
            laiks = ?,
            simptomi = ?,
            sniegta_palidz = ?,
            trauma = ?,
            ipasa_piezimes = ?
            WHERE ieraksta_id = ?"""

            values = (output[4], output[3], output[0], output[1], output[5], output[2], self.id[0])

            con.execute(query, values)  

        App.get_running_app().root.get_screen('main').ids.ieraksti.update(self.id[1]) # Iegūst saraksta metodi un izmanto
        
        Clock.schedule_once(lambda dt: self.dismiss(), 0.1) # Taimeris kurš aizver logu
        
class ProfilePopup(Popup):
    def __init__(self,skolens, **kwargs):
        super().__init__(**kwargs)
        self.skolens = skolens
        self.size_hint = (None,None)
        self.size = (800,800)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        self.background_color = (0,0,0,0)
        
        # (6, 1, 'a', 'Adele Strautmane', '050215-24644', '06.04.2015', '+37125329484', 'nav', '-', '-', 1) skolens example
        
        box = RoundedBox(box_color = white_c[0], corner_radius = [10,], orientation='vertical')
        
        #============================================#
        top_panel = RoundedBox(orientation='horizontal',
                                padding=20,
                                spacing=20,
                                size_hint_y=None,
                                height=90,
                                corner_radius=[10,10,0,0],
                                box_color=black_c[0])
        
        name = Label(text=f'[b]{skolens[3]} {skolens[1]}.{skolens[2]}[/b]',color=white_c[0],
                    font_size=30,
                    markup=True,
                    valign='center')
        name.bind(size=self.on_button_size)
        
        discard_button = CostumButton(text='Arhivēt skolēnu',
                                    color=white_c[0],
                                    button_color=red_c[2],
                                    corner_radius=[10,],
                                    size_hint_x=None,
                                    width=160,
                                    on_release=self.archive
                                    )
        
        top_panel.add_widget(name)
        top_panel.add_widget(discard_button)
        box.add_widget(top_panel)
        #============================================#
        
        #============================================#
        main_content_box = BoxLayout(orientation='vertical',spacing=10,padding=20)
        
        tabs = BoxLayout(orientation='horizontal',spacing=20)
        tab1 = BoxLayout(orientation='vertical',spacing=10)
        tab2 = BoxLayout(orientation='vertical',spacing=10)
        #===========================================================#
        pk_label = Label(text='Personas kods:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        pk_label.bind(size=self.on_button_size)
        
        pk_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2],
                            size_hint_y=None,
                            height=50)
        pk = TextInput(text=f'{skolens[4]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        pk_holder.add_widget(pk)
        tab1.add_widget(pk_label)
        tab1.add_widget(pk_holder)
        #===========================================================#
        dz_dati_label = Label(text='Dzimšanas dati:',   
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        dz_dati_label.bind(size=self.on_button_size)
        
        dz_dati_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2],
                            size_hint_y=None,
                            height=50)
        dz_dati = TextInput(text=f'{skolens[5]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        dz_dati_holder.add_widget(dz_dati)
        tab1.add_widget(dz_dati_label)
        tab1.add_widget(dz_dati_holder)
        #===========================================================#
        tel_label = Label(text='Telefona nummurs:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        tel_label.bind(size=self.on_button_size)
        
        tel_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2],
                            size_hint_y=None,
                            height=50)
        tel = TextInput(text=f'{skolens[6]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        tel_holder.add_widget(tel)
        tab1.add_widget(tel_label)
        tab1.add_widget(tel_holder)
        
        tabs.add_widget(tab1)
        #===========================================================#
        med_label = Label(text='Med. Karte:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        med_label.bind(size=self.on_button_size)
        
        med_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        med = TextInput(text=f'{skolens[7]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        med_holder.add_widget(med)
        tab2.add_widget(med_label)
        tab2.add_widget(med_holder)
        #===========================================================#
        hs_label = Label(text='Hroniskās slimības:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        hs_label.bind(size=self.on_button_size)
        
        hs_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
        hs = TextInput(text=f'{skolens[8]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        hs_holder.add_widget(hs)
        tab2.add_widget(hs_label)
        tab2.add_widget(hs_holder)
        
        tabs.add_widget(tab2)
        
        main_content_box.add_widget(tabs)
        #===========================================================#
        piezimes_label = Label(text='Piezīmes:',
                            color=gray_c[2],
                            size_hint_y=None,
                            height=20)
        piezimes_label.bind(size=self.on_button_size)
        
        piezimes_holder = RoundedBox(box_color= white_c[1], 
                            corner_radius=[10,],
                            outline_width = 0.5,
                            outline_color = white_c[2])
                            
        piezimes = TextInput(text=f'{skolens[9]}',
                            font_size= 20,
                            padding=(10,), 
                            background_color = transparent)
        piezimes_holder.add_widget(piezimes)
        main_content_box.add_widget(piezimes_label)
        main_content_box.add_widget(piezimes_holder)
        #===========================================================#
        box.add_widget(main_content_box)
        #============================================#
        
        #============================================#
        action_panel = BoxLayout(orientation='horizontal',
                                padding=20,
                                spacing=20,
                                size_hint=(None,None),
                                height=90,
                                width=500,
                                pos_hint={"right": 1})

        cancel_button = CostumButton(background_color = (0,0,0,0),
                                    color= black_c[1],
                                    background_normal="",
                                    text='Atcelt',
                                    corner_radius=[10,],
                                    button_color=white_c[0],
                                    outline_color=gray_c[1],
                                    outline_width=0,
                                    on_release=self.dismiss)

        save_button = CostumButton(background_color = (0,0,0,0),
                                    color= white_c[0],
                                    background_normal="",
                                    text='Saglabāt',
                                    corner_radius=[10,],
                                    button_color=main_c[2],
                                    on_release=self.save_profile)

        action_panel.add_widget(cancel_button)
        action_panel.add_widget(save_button)
        box.add_widget(action_panel)
        #============================================#
        
        self.add_widget(box)
        
    def archive(self,instance):
        pass
            
    def save_profile(self,instance):
        pass
    
    def on_button_size(self, instance, size):
        instance.text_size = size
#========================================================================#


#===============================# Login Screen #===============================#
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        
    def verify_credentials(self):
        if self.ids["login"].text == "" and self.ids["passw"].text == "":
            self.manager.current = "main"
            Window.maximize()

class LoginScreenCotent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 30
        self.spacing = 10
        
        title = Label(text='[b]Med sistēma', font_size=40, color=black_c[1], text_size=(None, None,), halign='center', valign='center',
                        size_hint_y=None, height = 100,
                        markup=True)
        title.bind(size=self.on_button_size)
        self.add_widget(title)
        
        liet_label = Label(text='Lietotājvārds:', color=gray_c[2], text_size=(None, None),
                            size_hint_y=None, height = 20)
        liet_label.bind(size=self.on_button_size)
        self.add_widget(liet_label)
        
        liet_input_holder = RoundedBox(box_color= white_c[1], corner_radius=[10,], size_hint_y=None, height = 50,
                                outline_width = 0.5,
                                outline_color = white_c[2])
        liet_input = TextInput(font_size= 20,padding=(10,), multiline=False,
                                size_hint_y=None, height = 50,
                                background_color = transparent)
        
        liet_input.bind(size=self.on_button_size)
        liet_input_holder.add_widget(liet_input)
        self.add_widget(liet_input_holder)
        
        parole_label = Label(text='Parole:', color=gray_c[2], text_size=(None, None),
                                size_hint_y=None, height = 20)
        parole_label.bind(size=self.on_button_size)
        self.add_widget(parole_label)
        
        parole_input_holder = RoundedBox(box_color=white_c[1], corner_radius=[10,], size_hint_y=None, height = 50,
                                outline_width = 0.5,
                                outline_color =white_c[2])
        parole_input = TextInput(font_size= 10,padding=(10,18,10,15), multiline=False,
                                size_hint_y=None, height = 50, password=True, password_mask= '\u25CF', font_name="DejaVuSans.ttf",
                                background_color = transparent)
        
        parole_input.bind(size=self.on_button_size)
        parole_input_holder.add_widget(parole_input)
        self.add_widget(parole_input_holder)
        
        separator = Label(size_hint_y=None, height = 20)
        self.add_widget(separator)
        
        peslegt_butt = CostumButton(text='Pieslegties', color=rgb_to_kivy('#ffffff'),  text_size=(None, None,), halign='center', valign='center',
                                size_hint_y=None, height = 50,
                                corner_radius=[10,],
                                button_color=rgb_to_kivy('#BE17E8'),
                                on_release=self.verify_credentials)
        
        peslegt_butt.bind(size=self.on_button_size)
        self.add_widget(peslegt_butt)

        self.inputs = [liet_input, parole_input]
        
    def on_button_size(self, instance, size):
        instance.text_size = size
        
    def verify_credentials(self,instance):
        
        if self.inputs[0].text == "" and self.inputs[1].text == "":
            self.parent.manager.current = "main"
            Window.maximize()
        
#==============================================================================#

#===============================# Main Screen #===============================#
class IerakstsAction(BoxLayout):
    global active_skolens
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Widget())
        create_button = CostumButton(text='Izveidot ierakstu',
                                    button_color=main_c[2],
                                    corner_radius=[10,],
                                    color=white_c[0],
                                    on_release = self.create,
                                    size_hint_x= None,
                                    width = 200,
                                    pos_hint = {'right': 1})
        
        self.add_widget(create_button)
        
    def create(self,instance):
        if active_skolens == -1: pass
        else:
            with db.connect('datubaze.db') as con:
                cur = con.execute(f"""SELECT * FROM skolenu_saraksts WHERE skolena_id = {active_skolens}""")
                skolnieks = cur.fetchone()
            CreateIerakstsPopup(skolnieks).open()
    
class CreateIerakstsPopup(IerakstiPopup):#klase jauna ieraksta izveidei
    def __init__(self, user, **kwargs):
        self.user = user
        user_layout = ['',
                       user[0], 
                       datetime.now().strftime("%d.%m.%y"), 
                       datetime.now().strftime("%H.%M"),
                       user[3],
                       f'{user[1]}.{user[2]}',
                       '',#snimptomi
                       '',#sniegta_palidz
                       'Nav',#trauma
                       ''#piezimes
                       ]
        super().__init__(id=user_layout, **kwargs)
        
    def save_record(self, instance):
        output = []
        for i in self.inputs:
            output.append(i.text) 
            
        with db.connect('datubaze.db') as con:
            query = """
                    INSERT INTO ambulatorais_zurnals 
                    (skolena_id, vards_uzvards, klase, datums, laiks, simptomi, sniegta_palidz, trauma, ipasa_piezimes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            data = (self.user[0], self.user[3], f'{self.user[1]}.{self.user[2]}', output[4], output[3], output[0], output[1], output[5], output[2])
            con.execute(query, data)
            
        App.get_running_app().root.get_screen('main').ids.ieraksti.update(self.id[1]) # Iegūst saraksta metodi un izmanto
        
        Clock.schedule_once(lambda dt: self.dismiss(), 0.1) # Taimeris kurš aizver logu
    
    def delete_record(self,instance):
        self.dismiss()
        
class Ieraksti(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'vertical'

    def update(self,id):
        self.clear_widgets()
        with db.connect('datubaze.db') as con:
            cur = con.execute(f"""SELECT * FROM ambulatorais_zurnals WHERE skolena_id = {id} ORDER BY date(datums) ASC, time(laiks) ASC""")
            
            ieraksti = cur.fetchall()
            ieraksti = sort_data_by_date_time(ieraksti, date_index=2, time_index=3)
            
            self.spacing = 1
            self.padding = 2
            for i in ieraksti:
                box = RoundedBox(orientation='horizontal', size_hint_y=None, height=230, box_color=white_c[0], corner_radius=[5,])
                
                #i[8] = trauma
                
                main_content_box = BoxLayout(orientation='vertical',padding=(10,10,10,5))
                
                name_boxx = BoxLayout(size_hint_y=None, height=40)
                
                
                name = Label(text=f'{i[4]} {i[5]}', halign='left', valign='middle', padding=(5,5), text_size=(None, None),font_size=25,color= black_c[1])
                name.bind(size=self.on_button_size)
                iesatijumi = Button(size_hint=(None,None),size=(60,60),color= gray_c[2],
                                    background_normal = "..\\images\\editUp.png",
                                    background_down = "..\\images\\editDown.png",
                                    background_color = gray_c[2])
                
                iesatijumi.bind(on_release=partial(self.set_variable,i))
                
                name_boxx.add_widget(name)
                name_boxx.add_widget(iesatijumi)
                main_content_box.add_widget(name_boxx)
                
                content_box = BoxLayout(orientation='horizontal',spacing=10,padding=10)
                si_un_pa_box = RoundedBox(orientation='vertical', box_color=white_c[1], corner_radius=[5,])
                
                content_simptomi = Label(text=f'{i[6]}',size_hint=(1,None), height=35, halign='left', valign='middle', padding=(5,5), text_size=(None, None),color=(black_c[1]))
                content_simptomi.bind(size=self.on_button_size)
                
                content_palidz = Label(text=f'{i[7]}', halign='left', valign='top', padding=(5,5), text_size=(None, None),color=(black_c[1]))
                content_palidz.bind(size=self.on_button_size)
                
                si_un_pa_box.add_widget(content_simptomi)
                si_un_pa_box.add_widget(content_palidz)
                content_box.add_widget(si_un_pa_box)
                
                piezimes_layout = RoundedBox(orientation='vertical', box_color=white_c[1], corner_radius=[5,])
                piezimes_box = Label(text=f'{i[9]}',size_hint=(1,1), halign='left', valign='top', padding=(5,5), text_size=(None, None),color=black_c[1])
                piezimes_box.bind(size=self.on_button_size)
                
                piezimes_layout.add_widget(piezimes_box)
                content_box.add_widget(piezimes_layout)
                
                trauma = BoxLayout(orientation='vertical',size_hint_x=None,width=100,spacing=10)
                
                if i[8] == 'Nav':
                    trauma_label = Label(text='Trauma',size_hint_y=None, height=20, halign='center', valign='middle', text_size=(None, None),color=gray_c[1])
                    trauma_label.bind(size=self.on_button_size)
                    trauma_holder = RoundedBox(orientation='vertical',box_color=white_c[1],corner_radius=[5,],padding=10)
                    trauma_icon = Image(source="..\\images\\traumaFalse.png",color=gray_c[0],keep_ratio=True)
                    trauma_holder.add_widget(trauma_label)
                    trauma_holder.add_widget(trauma_icon)
                else:
                    trauma_label = Label(text='[b]Trauma',size_hint_y=None, height=20, halign='center', valign='middle', text_size=(None, None),color=red_c[2],markup=True)
                    trauma_label.bind(size=self.on_button_size)
                    trauma_holder = RoundedBox(orientation='vertical',box_color=red_c[4],corner_radius=[5,],padding=10)
                    trauma_icon = Image(source="..\\images\\traumaTrue.png",color=red_c[2],keep_ratio=True)
                    trauma_holder.add_widget(trauma_label)
                    trauma_holder.add_widget(trauma_icon)
                    
                #trauma.add_widget(trauma_label)
                trauma.add_widget(trauma_holder)
                
                content_box.add_widget(trauma)
                
                main_content_box.add_widget(content_box)
                
                time_box = Label(text=f'{i[3]} • {i[2]}',size_hint_y=None, height=20, halign='right', valign='middle', padding=(5,5), text_size=(None, None),color=black_c[1])
                time_box.bind(size=self.on_button_size)
                
                main_content_box.add_widget(time_box)
                
                box.add_widget(main_content_box)
                
                self.add_widget(box)
            
    def on_button_size(self, instance, size):
        instance.text_size = size    
    
    def set_variable(self,id,button_object):
        IerakstiPopup(id=id).open()
        
class Options_button(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '...' 
        self.values = ['Import file']  
        self.size_hint = (None,None)
        self.size = (200,50)
        self.bind(text=self.on_spinner_select)
        
    def on_spinner_select(self, instance, text):
        self.text = '...'
        if text == 'Import file':
            self.import_file()
        else: print('went wrong')

    def import_file(self):
        Choose_file().open()
        
class IzveidotIerakstu(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_press(self):
        popup_layout = BoxLayout()
        popup_button = Button(text='Close')
        popup_layout.add_widget(popup_button)
        popup = Popup(title='', content=popup_layout, size_hint=(None, None), size=(600, 400),background="",title_size='0sp',separator_height=0)
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

            self.skolnieks = skolnieks
            
            self.orientation = 'vertical'

            box = RoundedBox(box_color=white_c[0] ,corner_radius=[0,], orientation = 'vertical', image_source='..\\images\\background.png')

            name = Label(text=f'[b]{skolnieks[3]} {skolnieks[1]}.{skolnieks[2]}[/b]', size_hint_y = None, height= 120,  halign='center', valign='middle', padding=(5,5), text_size=(None, None), font_size=40, markup=True, color=white_c[0])
            name.bind(size=self.on_button_size)

            main_content_box = BoxLayout(orientation='vertical')

            user_data = BoxLayout(orientation='horizontal',size_hint_y=None, height=150)

            nosaukumi = Label(text='Personas kods:\nDzimšanas dati:\nTelefona nummurs:\nMed. Karte:\nHroniskās slimības', halign='left', valign='top', padding=(10,10), text_size=(None, None), font_size=20, color=white_c[1])
            nosaukumi.bind(size=self.on_button_size)

            dati = Label(text=f'{skolnieks[4]}\n{skolnieks[5]}\n{skolnieks[6]}\n{skolnieks[7]}\n{skolnieks[8]}', height=150,halign='right', valign='top', padding=(10,10), text_size=(None, None), font_size=20, color=white_c[1])
            dati.bind(size=self.on_button_size)

            user_data.add_widget(nosaukumi)
            user_data.add_widget(dati)

            main_content_box.add_widget(user_data)

            piezimes_box = BoxLayout(orientation='vertical',padding=10)

            p_nosaukums = Label(text='Piezimes:',size_hint_y=None, height=40, halign='left', valign='top',padding=(10,10), text_size=(None, None), font_size=20, color=white_c[1])
            p_nosaukums.bind(size=self.on_button_size)

            piezimes = RoundedBox(box_color=rgb_to_kivy('#00000020'),corner_radius=[10,],padding=10)
            piezimes_text = Label(text=f'{skolnieks[9]}',text_size=(None, None), font_size=20,halign='left', valign='top',color=white_c[0])
            piezimes_text.bind(size=self.on_button_size)
            
            piezimes.add_widget(piezimes_text)

            piezimes_box.add_widget(p_nosaukums)
            piezimes_box.add_widget(piezimes)

            main_content_box.add_widget(piezimes_box)

            tool_box = BoxLayout(orientation='horizontal',size_hint_y=None,height=80)
            filler = Label()
            tool_box.add_widget(filler)
            eddit_button = Button(color=gray_c[2],size_hint=(None,None),size=(60, 60),
                                background_normal = "..\\images\\userUp.png",
                                background_down = "..\\images\\userDown.png",
                                background_color = gray_c[2],
                                on_release=self.open_popup
                                )
            
            tool_box.add_widget(eddit_button)
            
            main_content_box.add_widget(tool_box)

            box.add_widget(name)
            box.add_widget(main_content_box)

            self.add_widget(box)
            
    def open_popup(self,instance):
        ProfilePopup(skolens=self.skolnieks).open()
        
    def on_button_size(self, instance, size):
        instance.text_size = size
        
class SkoleniSearch(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 10
        search_input = TextInput(font_size= 20,padding=(10,12,10,10), multiline=False,
                                size_hint_y=None, height = 50,
                                background_color = transparent,
                                foreground_color  = white_c[0],
                                on_text_validate=self.search,
                                hint_text='Meklēt skolēnu',
                                hint_text_color=gray_c[0])
        
        search_button = Button( background_normal = "..\\images\\searchUp.png",
                                background_down = "..\\images\\searchDown.png",
                                background_color = white_c[0],
                                size_hint=(None,None),
                                size=(50,50),
                                on_release=self.search)
        
        box = RoundedBox(corner_radius=[10,],box_color=gray_c[2],size_hint_y=None,height=50)
        
        box.add_widget(search_input)
        box.add_widget(search_button)
        self.add_widget(box)
        
        self.input = search_input
        
    def search(self,instance):
        search_term = self.input.text
        with db.connect('datubaze.db') as con:
            cur = con.execute("""SELECT * FROM skolenu_saraksts WHERE vards_uzvards LIKE ? OR pk LIKE ? ORDER BY klase, klases_burts, vards_uzvards""", ('%' + search_term + '%', '%' + search_term + '%'))
            saraksts = cur.fetchall()
            App.get_running_app().root.get_screen('main').ids.list.update(saraksts)
        
class List(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with db.connect('datubaze.db') as con:
            cur = con.execute("""SELECT * FROM skolenu_saraksts ORDER BY klase, klases_burts, vards_uzvards
            """)
            skoleni = cur.fetchall()
        self.update(skoleni)
                
    def update(self,saraksts):
        self.clear_widgets()
        self.spacing = 1
        self.padding = 1
        for i in saraksts:
            if i[10] == 1:#Parbaude vai skolnieks ir arhivēts
                button = CostumButton(
                        text=f'{i[1]}.{i[2]} - {i[3]}',
                        text_size= (200,None),    
                        halign= 'left',
                        valign= 'bottom',
                        size_hint=(1,None),
                        size=(dp(20),dp(50)),
                        on_press=  partial(self.set_variable,i[0]),
                        background_color = (0,0,0,0),#Color of the button
                        color= white_c[0],#Text color
                        background_normal="",
                        button_color=black_c[0],
                        corner_radius=[0,]
                        )
                self.add_widget(button)

    def set_variable(self,id,button_object): # Metode, kura atbild par to lai informācija par skolēnu nomainās uz ekrāna
        #Window.toggle_fullscreen()
        #=========================================================================================================# Skolena info
        self.parent.parent.parent.parent.parent.ids.profile.update(id)
        #=========================================================================================================#
        global active_skolens 
        active_skolens = id
        #=========================================================================================================# Ierakstu info
        self.parent.parent.parent.parent.parent.ids.ieraksti.update(id)
        #=========================================================================================================#

kv = Builder.load_file("main.kv")

class MedSistēma(App):
    def build(self):
        Window.size_hint = (None, None)
        Window.size = (400, 440)
        #title = RoundedBox(box_color=black_c[1],corner_radius=[10,])
        #Window.custom_titlebar = True
        #Window.set_custom_titlebar(title)
        return kv

if __name__ == "__main__":
    
    MedSistēma().run()