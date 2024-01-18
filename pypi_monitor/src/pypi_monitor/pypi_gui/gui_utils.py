#pane manager class
    #this class needs to take in settings.yaml and construct the appropriate number of panes in the appropriate location 
        #not sure if hooking the panes into a visualizer class here makes sense yet or not
#visualizer class
    #this class will take in the client data and update the display as needed
    #first we will just print the number, but then later we can move on ot more advanced options

import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QColorDialog, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QColor

#Set the background color for the main window
def set_main_background_color(main_window, color):

    #convert hex to QColor
    q_color = QColor(color)

    # Set the background color for main window, settings, and button
    main_window.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_button.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.setStyleSheet(f'background-color: {q_color.name()};')