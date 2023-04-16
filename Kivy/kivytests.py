from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from ctypes import windll, c_int64
import random
import loremipsum

windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))

class Label(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0,0,0,1)
    
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

class Ieraksti(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        
        for m in range(20):
              
            i = (1,500,'20/12/2023','14:25','Aleksejs Šematjuks','12.a','Vēdera sāpes','Kautkādas rekomendācijas',random.choice(['nav','ir']),'Bez piezīmēm')
            
            box = RoundedBox(orientation='horizontal', size_hint_y=None, height=230, box_color=(1,1,1,1), corner_radius=[10,])
            
            if i[8] == 'nav':
                trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=(0,1,.5,1), corner_radius=[10,0,0,10])
            elif i[8] == 'ir':
                trauma_box = RoundedBox(size_hint_x=None, width=20,box_color=(1,0,.3,1), corner_radius=[10,0,0,10])
            box.add_widget(trauma_box)
            
            main_content_box = BoxLayout(orientation='vertical',padding=(10,0,10,5))
            
            name_boxx = BoxLayout(size_hint_y=None, height=40)
            
            
            name = Label(text=f'{i[4]} {i[5]}', halign='left', valign='middle', padding=(5,5), text_size=(None, None),font_size=25)
            name.bind(size=self.on_button_size)
            iesatijumi = Button(background_normal="",background_color=(0,0,0,0), text="...", color=(0,0,0,1),size_hint_x=None,width=30)
            
            name_boxx.add_widget(name)
            name_boxx.add_widget(iesatijumi)
            main_content_box.add_widget(name_boxx)
            
            content_box = BoxLayout(orientation='horizontal',spacing=10,padding=10)
            si_un_pa_box = RoundedBox(orientation='vertical', box_color=(.9,.9,.93,1), corner_radius=[5,])
            
            content_simptomi = Label(text=f'{i[6]}',size_hint=(1,None), height=35, halign='left', valign='middle', padding=(5,5), text_size=(None, None))
            content_simptomi.bind(size=self.on_button_size)
            
            content_palidz = Label(text=f'{i[7]}', halign='left', valign='top', padding=(5,5), text_size=(None, None))
            content_palidz.bind(size=self.on_button_size)
            
            si_un_pa_box.add_widget(content_simptomi)
            si_un_pa_box.add_widget(content_palidz)
            content_box.add_widget(si_un_pa_box)
            
            piezimes_layout = RoundedBox(orientation='vertical', box_color=(.9,.9,.93,1), corner_radius=[5,])
            piezimes_box = Label(text=f'{i[9]}',size_hint=(0.4,1), halign='left', valign='top', padding=(5,5), text_size=(None, None))
            piezimes_box.bind(size=self.on_button_size)
            
            piezimes_layout.add_widget(piezimes_box)
            content_box.add_widget(piezimes_layout)
            
            main_content_box.add_widget(content_box)
            
            time_box = Label(text=f'{i[3]} • {i[2]}',size_hint_y=None, height=20, halign='right', valign='middle', padding=(5,5), text_size=(None, None))
            time_box.bind(size=self.on_button_size)
            
            main_content_box.add_widget(time_box)
            
            box.add_widget(main_content_box)
            
            self.add_widget(box)
            
    def on_button_size(self, instance, size):
        instance.text_size = size           

class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create BoxLayout and add it to the scrollview
        box_layout = Ieraksti(orientation='vertical', size_hint_y=None)
        box_layout.bind(minimum_height=box_layout.setter('height'))
        self.add_widget(box_layout)


class MyApp(App):
    def build(self):
        return MyScrollView()


if __name__ == '__main__':
    MyApp().run()
