
#intent here is to pass in the "settings" object that is loaded out of the yaml and then just 

#class File Settings Page

    #insert current pick color logic 

    #insert a displays button that enables the users to check select from the displays 

        # for each enabled display, add toggles for temp and % util

#class ViewSettingsPage

#class SettingsDialog

    #def save_settings

    #def load_settings 

    #def reset_settings 

#class SettingsController

from pypi_monitor.pypi_gui import gui_utils

import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QColorDialog, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QSize, Qt

from pypi_monitor.pypi_gui import gui_main

class FileSettingsPage(QWidget):
    def __init__(self, parent=None):
        super(FileSettingsPage, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Add your file settings widgets here
        self.setLayout(self.layout)

class ViewSettingsPage(QWidget):
    def __init__(self, main_window, parent=None):
        super(ViewSettingsPage, self).__init__(parent)
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add the "Pick Color" button to the View tab
        self.color_button = QPushButton('Pick Color')
        self.color_button.clicked.connect(self.pick_color)
        self.layout.addWidget(self.color_button)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.settings["background_color"] = color.name() #get hex color code
            gui_utils.set_main_background_color(self.main_window, color) #set main window color

class SettingsController:
    def __init__(self, parent):
        self.parent = parent
        self.settings_dialog = SettingsDialog(parent)

    def open_settings(self):
        self.settings_dialog.exec_()

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

        # Create the "Save" button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        # Create the "Reset" button
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_settings)

        # Create the main layout for the dialog
        layout = QVBoxLayout(self)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)

        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    #save current settings 
    def save_settings(self):
        #write self.settings into the yaml 
        file_path="settings/settings.yaml"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, file_path)
        with open(settings_file, 'w') as file:
            print("trying to yaml dump")
            print(self.main_window.settings)
            yaml.dump(self.main_window.settings, file, default_flow_style=False)

    #reset all settings to defaults 
    def reset_settings(self):
        self.load_settings('settings/default_settings.yaml')
        self.main_window.update_settings()

    #load settings from a yaml file
    def load_settings(self, file_path='settings/settings.yaml'):
        # Load settings from the specified file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, file_path)
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                self.main_window.settings = yaml.full_load(file)


