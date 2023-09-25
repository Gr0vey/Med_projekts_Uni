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
from kivy.uix.screenmanager import ScreenManager, Screen
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.spinner import Spinner
import os
import pandas as pd

def max_row_length(arr_2d):
    max_length = 0
    for row in arr_2d:
        row_length = len(row)
        if row_length > max_length:
            max_length = row_length

    return max_length

class File_display(Popup):
    def __init__(self, records, **kwargs):
        super().__init__(**kwargs)
        self.records = records
        
        self.size_hint = (None,None)
        self.size = (800,400)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        
        self.main_box = BoxLayout(orientation = 'vertical')
        self.content = self.main_box
        
        self.main_box.add_widget(Label(text='Kolonnu izvēle:',size_hint=(None,None),size=(200,20)))
        
        top_row = BoxLayout(orientation = 'horizontal',size_hint_y=None, height=20)
        for i in range(max_row_length(self.records)):
            drop_button = Spinner(text='-izvēlēties kolonnu-',
                                  values=['Klase',
                                          'Vārds Uzvārds',
                                          'Personas kods',
                                          'Telefona nummurs',
                                          'Dzimšanas datums'])
                
            top_row.add_widget(drop_button)
        self.main_box.add_widget(top_row)
        
        self.main_box.add_widget(Label(text='Datu priekšskats:',size_hint=(None,None),size=(200,20)))
        
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
        
        commit = Button(text='Commit',size_hint=(None,None),size=(100,20),
                        on_release=self.dismiss)
        self.main_box.add_widget(commit)
        
class Choose_file(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint = (None,None)
        self.size = (600,400)
        self.title =''
        self.title_size='0sp'
        self.separator_height=0
        self.main_box = BoxLayout(orientation = 'vertical')
        self.content = self.main_box
        
        self.file_view = FileChooserListView(path = os.path.expanduser("~"),
                                            filters=['*.xlsx', '*.csv'])
        self.main_box.add_widget(self.file_view)
        
        choice_button = Button(text='open',size_hint = (None,None), size = (100,20))
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
                    
class StarterApp(App):
    def build(self):
        # Create the main layout
        Window.size = (1000, 500) 
        layout = FloatLayout()
        
        button = Button(text="Click me!", size_hint=(None, None), size=(200,50), pos=(500-100, 250-25))
        button.bind(on_press=self.on_button_click)
        
        layout.add_widget(button)
        
        return layout
    
    def on_button_click(self, instance):
        Choose_file().open()
    
if __name__ == '__main__':
    StarterApp().run()
