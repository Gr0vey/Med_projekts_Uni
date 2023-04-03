from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class ButtonBoxLayout(BoxLayout):
    def __init__(self, content_box, **kwargs):
        super(ButtonBoxLayout, self).__init__(**kwargs)
        self.content_box = content_box
        # Create the buttons
        self.button1 = Button(text="Button 1", on_press=self.on_button1_press)
        self.button2 = Button(text="Button 2", on_press=self.on_button2_press)
        self.button3 = Button(text="Button 3", on_press=self.on_button3_press)
        # Add the buttons to the layout
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.add_widget(self.button3)

    def on_button1_press(self, instance):
        self.content_box.clear_widgets()
        self.content_box.add_widget(Label(text="Button 1 pressed"))

    def on_button2_press(self, instance):
        self.content_box.clear_widgets()
        self.content_box.add_widget(Label(text="Button 2 pressed"))

    def on_button3_press(self, instance):
        self.content_box.clear_widgets()
        self.content_box.add_widget(Label(text="Button 3 pressed"))

class ContentBoxLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        # Create the layouts
        content_layout = ContentBoxLayout()
        button_layout = ButtonBoxLayout(content_box=content_layout)
        # Add the layouts to the app
        root = BoxLayout(orientation='horizontal')
        root.add_widget(button_layout)
        root.add_widget(content_layout)
        return root

if __name__ == '__main__':
    MyApp().run()
