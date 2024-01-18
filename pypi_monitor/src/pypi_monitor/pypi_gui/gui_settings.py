import os
import yaml
from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QColorDialog, QTabWidget, QWidget

from pypi_monitor.pypi_gui import gui_utils

#create a file tab on settings page
class FileSettingsPage(QWidget):
    def __init__(self, parent=None):
        super(FileSettingsPage, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Add your file settings widgets here
        self.setLayout(self.layout)

#create a views tab on settings page
class ViewSettingsPage(QWidget):
    def __init__(self, main_window, parent=None):
        super(ViewSettingsPage, self).__init__(parent)
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add the "Pick Color" button to the View tab and hook into pick_color()
        self.color_button = QPushButton('Pick Color')
        self.color_button.clicked.connect(self.pick_color)
        self.layout.addWidget(self.color_button)

    #use the built in Qt color selector 
    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.settings["background_color"] = color.name() #get hex color code
            gui_utils.set_main_background_color(self.main_window, color) #set main window color

#define the settings controller
class SettingsController:
    def __init__(self, parent):
        self.parent = parent
        self.settings_dialog = SettingsDialog(parent)

    def open_settings(self):
        self.settings_dialog.exec_()

#define the settings dialog as a QDialog 
class SettingsDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 400, 300)
        self.main_window = main_window

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create and add pages to the tab widget
        self.file_settings_page = FileSettingsPage(self)
        self.view_settings_page = ViewSettingsPage(main_window, self)  # Pass main_window to ViewSettingsPage
        self.tab_widget.addTab(self.file_settings_page, 'File')
        self.tab_widget.addTab(self.view_settings_page, 'View')

        # Create the "Save" button and hook into save_resettings()
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        # Create the "Reset" button and hook into reset_settings()
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_settings)

        # Create the main layout for the settings QDialog
        layout = QVBoxLayout(self)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)

        #add in the widgets we defined
        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    #function to save current settings 
    def save_settings(self):
        #write self.settings into the yaml 
        file_path="settings/settings.yaml"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, file_path)
        with open(settings_file, 'w') as file:
            yaml.dump(self.main_window.settings, file, default_flow_style=False)

    #functions to reset all settings to defaults 
    def reset_settings(self):
        self.load_settings('settings/default_settings.yaml')
        self.main_window.update_settings()

    #function to load settings from a yaml file
    def load_settings(self, file_path='settings/settings.yaml'):
        # Load settings from the specified file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, file_path)
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                self.main_window.settings = yaml.full_load(file)


