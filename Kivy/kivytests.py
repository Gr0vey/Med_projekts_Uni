import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 1, 0, 1)
            self.corner = RoundedRectangle(pos=self.pos, size=self.size, radius=[10,])
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

    def update_canvas(self, *args):
        self.corner.pos = self.pos
        self.corner.size = self.size

class RoundedBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10
        for i in range(5):
            button = RoundedButton(text=f"Button {i}",background_normal="",background_color=(0,0,0,0))
            self.add_widget(button)

class MyApp(App):
    def build(self):
        return RoundedBoxLayout()

if __name__ == "__main__":
    MyApp().run()

