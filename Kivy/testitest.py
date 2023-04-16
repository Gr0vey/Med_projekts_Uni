from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class MyBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        
        # Set orientation to vertical
        self.orientation = 'vertical'
        
        # Create 5 buttons with height 80 and text aligned to bottom left corner
        for i in range(5):
            btn = Button(text='Button {}'.format(i+1), size_hint_y=None, height=80,
                         halign='left', valign='bottom', text_size=(None, None),
                         padding=(10, 5, 10, 5))
            btn.bind(width=self.on_button_width)
            self.add_widget(btn)

    def on_button_width(self, instance, width):
        # Set the text_size of the button to match the button's width
        instance.text_size = (width, None)


class MyApp(App):

    def build(self):
        # Set window size
        Window.size = (400, 400)
        
        # Create and return instance of MyBoxLayout
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
