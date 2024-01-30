#pane manager class
    #this class needs to take in settings.yaml and construct the appropriate number of panes in the appropriate location 
        #not sure if hooking the panes into a visualizer class here makes sense yet or not
#visualizer class
    #this class will take in the client data and update the display as needed
    #first we will just print the number, but then later we can move on ot more advanced options

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
import time


#Set the background color for the main window
def set_main_background_color(main_window, color):

    #convert hex to QColor
    q_color = QColor(color)

    # Set the background color for main window, settings page, and button
    main_window.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_button.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.view_settings_page.displays_dialog.setStyleSheet(f'background-color: {q_color.name()};')

#creates appropriate number of panes, sizes them, and then keeps panes, and panes_list up to date 
class PaneManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.panes = {}
        self.panes_controllers = {}
        self.create_pane_lists()

    #function in charge of listening to main.window.settings and keeping panes and panes_list up to date 
    def create_pane_lists(self):
        self.panes_status = {}
        if self.main_window.settings["displays"]["CPU"]["enabled"] == True:
            self.panes_status["CPU"] = True
        else:
            self.panes_status["CPU"] = False   
 
        if self.main_window.settings["displays"]["GPU"]["enabled"] == True:
            self.panes_status["GPU"] = True
        else:
            self.panes_status["CPU"] = False


    #function that creates a simple pane with correct title
    def create_pane(self, title, j):

        self.panes[title] = QWidget(self.main_window)
        self.panes_controllers[title] = PaneController(self.panes[title], self.main_window)

        #doing weird spacing w j for now to see two panes
        self.panes[title].setGeometry(50+j, 0, 200, 200)

        #panes are clear rn, need to set color
        color = self.main_window.settings["displays"]["CPU"]["color"]
        settings = "background-color: "+color+"; margin:5px; border:1px solid rgb(0, 0, 0);  "
        self.panes[title].setStyleSheet(settings)


    #function that recursively calls create pane the necessary amount of times (to create correct number of panes)
    def create_panes(self):
        for i in self.panes_status:
            j=0
            if self.panes_status[i] == True:
                if i == "CPU":
                    j = 200
                self.create_pane(i,j)
                self.main_window.layout.addWidget(self.panes[i])
    
    #function that wraps all pane control logic. It will be called when any changes to panes need to be made
    def update_panes(self):

        #clear existing panes
        self.panes_controllers = {}
        self.pane = {}
        self.panes_status = {}
        print("clear start")
        for i in reversed(range(self.main_window.layout.count())): 
            # print(self.main_window.layout.itemAt(i).widget())
            self.main_window.layout.itemAt(i).widget().setParent(None)
        print("clear end")
        print("num widgets after clear: " + str(self.main_window.layout.count()))
        self.create_pane_lists()
        self.create_panes()
        print(self.panes_status)
        print(self.panes)
        print("num widgets after create_panes(): " + str(self.main_window.layout.count()))


#class that will be used once per each pane. It will be in charge of controlling which panels are displayed inside the pane 
class PaneController:
    def __init__(self, widget, main_window):
        self.widget = widget
        self.main_window = main_window
    
    def test(self):
        dummy = 0

 