#pane manager class
    #this class needs to take in settings.yaml and construct the appropriate number of panes in the appropriate location 
        #not sure if hooking the panes into a visualizer class here makes sense yet or not
#visualizer class
    #this class will take in the client data and update the display as needed
    #first we will just print the number, but then later we can move on ot more advanced options

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget


#Set the background color for the main window
def set_main_background_color(main_window, color):

    #convert hex to QColor
    q_color = QColor(color)

    # Set the background color for main window, settings page, and button
    main_window.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_button.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.view_settings_page.displays_dialog.setStyleSheet(f'background-color: {q_color.name()};')

class PaneManager:
    def __init__(self, parent):
        self.parent = parent
        self.main_window = parent
        self.panes = {}
        self.create_pane_lists()

    def create_pane_lists(self):
        if self.main_window.settings["displays"]["CPU"]["enabled"] == True:
            self.panes["CPU"] = True
        if self.main_window.settings["displays"]["GPU"]["enabled"] == True:
            self.panes["GPU"] = True
   