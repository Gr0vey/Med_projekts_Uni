from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Original Text'
    
    def change_label(self, new_text):
        self.text = new_text

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mylabel = MyLabel()
        self.add_widget(self.mylabel)

def update_label(a):
    mylabel.change_label(str(a))

class MyApp(App):
    def build(self):
        global mylabel
        mylayout = MyBoxLayout()
        mylabel = mylayout.mylabel
        return mylayout
    
for i in range (10):
    update_label(i)
    input()

if __name__ == '__main__':
    MyApp().run()
