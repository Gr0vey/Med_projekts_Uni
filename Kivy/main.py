from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.properties import StringProperty

klases =['a','b','c','d']

class WidgetEx(GridLayout):
    my_text = StringProperty("Button has not been clicked")
    x = 0
    def buttonPress(self,):
        self.x = self.x + 1
        print('Button has been clicked')
        self.my_text = "Button has been clicked {} times".format(self.x)

class List(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0,12):
            for j in klases:
                self.add_widget(Button(
                    text='{}.{}'.format(i+1,j),
                    size_hint=(1,None),
                    size=(dp(20),dp(20))
                    ))
    
                
class BoxlayoutEx(BoxLayout):
    pass
class Aplikacija(App):
    pass


Aplikacija().run()