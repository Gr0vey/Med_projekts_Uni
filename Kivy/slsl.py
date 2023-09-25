from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import os

class FileViewerPopupContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Get the user's home directory and set it as the default path
        user_home = os.path.expanduser("~")

        # Create a custom filter for allowed file extensions
        self.file_chooser = FileChooserListView(path=user_home, filters=['*.xlsx', '*.csv'])
        self.add_widget(self.file_chooser)

        self.select_button = Button(text="Select File")
        self.select_button.bind(on_press=self.select_file)
        self.add_widget(self.select_button)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def select_file(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            file_path = selected_file[0]
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.result_label.text = file_contents
