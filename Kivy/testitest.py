from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        # Add a placeholder widget that expands and pushes the button to the right
        self.add_widget(Widget())

        # Create a button and add it to the box layout
        button = Button(text='Right Button', size_hint=(None, None), size=(100, 50))
        self.add_widget(button)


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
