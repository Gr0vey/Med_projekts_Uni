from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

class DropdownSpinnerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text="Select an option:")
        layout.add_widget(label)

        spinner = Spinner(
            text='Option 1',  # Default text to display
            values=('Option 1', 'Option 2', 'Option 3'),  # List of options
            size_hint=(None, None),
            size=(200, 44)
        )

        # Bind the on_text event to a callback function
        spinner.bind(on_text=self.on_spinner_select)

        layout.add_widget(spinner)

        return layout

    def on_spinner_select(self, instance, text):
        print(f"Selected option: {text}")

if __name__ == '__main__':
    DropdownSpinnerApp().run()
