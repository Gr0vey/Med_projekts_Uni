import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.title = 'Popup'
        self.size_hint = (0.8, 0.4)

        layout = BoxLayout(orientation='vertical')
        self.text_inputs = []

        for i in range(3):
            text_input = TextInput()
            self.text_inputs.append(text_input)
            layout.add_widget(text_input)

        toggle_button = Button(text='IR', background_normal='', background_down='')
        toggle_button.bind(on_release=self.on_toggle_button_release)
        layout.add_widget(toggle_button)

        button = Button(text='Print', on_release=self.print_values)
        layout.add_widget(button)

        self.content = layout
        self.selected_mode = 'IR'

    def on_toggle_button_release(self, instance):
        if instance.text == 'IR':
            instance.text = 'NAV'
            self.selected_mode = 'NAV'
        else:
            instance.text = 'IR'
            self.selected_mode = 'IR'

    def print_values(self, instance):
        print('Mode:', self.selected_mode)
        for text_input in self.text_inputs:
            print(text_input.text)

class MyApp(App):
    def build(self):
        button = Button(text='Open Popup', on_release=self.open_popup)
        return button

    def open_popup(self, instance):
        popup = MyPopup()
        popup.open()

if __name__ == '__main__':
    MyApp().run()
