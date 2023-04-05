from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class PopupExample(App):
    def build(self):
        layout = GridLayout(cols=1)
        button = Button(text='Click Me')
        button.bind(on_press=self.show_popup)
        layout.add_widget(button)
        return layout

    def show_popup(self, event):
        popup_layout = GridLayout(cols=1)
        popup_label = Label(text='Hello, world!')
        popup_layout.add_widget(popup_label)
        popup_button = Button(text='Close')
        popup_layout.add_widget(popup_button)
        popup = Popup(title='Popup Example', content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    PopupExample().run()
