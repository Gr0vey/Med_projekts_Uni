from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

class ToggleButtonApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        toggle_button = MyToggleButton(text='Off', size_hint=(None, None), size=(100, 50))
        
        layout.add_widget(toggle_button)
        return layout

class MyToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super(MyToggleButton, self).__init__(**kwargs)
        self.bind(state=self.on_toggle)
    
    def on_toggle(self, instance, value):
        if value == 'normal':
            instance.text = 'Off'
        else:
            instance.text = 'On'

ToggleButtonApp().run()
