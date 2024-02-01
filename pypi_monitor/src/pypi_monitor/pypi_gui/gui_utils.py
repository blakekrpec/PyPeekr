from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


#Set the background color for the main window
def set_main_background_color(main_window, color):
    #convert hex to QColor
    q_color = QColor(color)

    # Set the background color for main window, settings page, and button
    main_window.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_button.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.view_settings_page.displays_dialog.setStyleSheet(f'background-color: {q_color.name()};')
    main_window.settings_controller.settings_dialog.file_settings_page.ip_dialog.setStyleSheet(f'background-color: {q_color.name()};')

    #call pane manager to also update pane colors 
    main_window.pane_manager.update_panes()

#class that creates appropriate number of panes, sizes them, and then keeps panes, and all relevant lists up to date 
    #update_panes() is the only function of this class that should be called externally, it will call all other functions 
class PaneManager:
    def __init__(self, main_window):
        #define main window, and call update_panes() on startup
        self.main_window = main_window
        self.update_panes()

    #function in charge of listening to main.window.settings and keeping panes and panes_list up to date 
    def create_pane_lists(self):
        #empty previous panes_status list
        self.panes_status = {}
        #update panes_status list according to current settings 
        if self.main_window.settings["displays"]["CPU"]["enabled"] == True:
            self.panes_status["CPU"] = True
        else:
            self.panes_status["CPU"] = False   
 
        if self.main_window.settings["displays"]["GPU"]["enabled"] == True:
            self.panes_status["GPU"] = True
        else:
            self.panes_status["GPU"] = False

    #function that creates a simple pane with correct title
    def create_pane(self, title):
        #create the pane for "title" and store in panes list, store layout so we can access it later to add widgets, and set the layout
        self.panes[title] = QWidget(self.main_window)

        #Spawn a PaneController for this new pane, and store it in panes_controllers list
        self.panes_controllers[title] = PaneController(title, self.panes[title], self.main_window)

        #define pane color
        color = self.main_window.settings["displays"][title]["color"]

        #define pane stylesheet and apply
        settings = "background-color: "+color+"; margin:2px; border:0px solid rgb(0, 0, 0); border-radius:20px;"
        self.panes[title].setStyleSheet(settings)

    #function that recursively calls create pane the necessary amount of times (to create correct number of panes)
    def create_panes(self):
        #loop over all pane statuses
        for i in self.panes_status:
            #if pane is enabled 
            if self.panes_status[i] == True:
                #create relevant panes, and add them to the central widget layout with title
                self.create_pane(i)
                self.main_window.layout.addWidget(self.panes[i])
    
    #function that wraps all pane management logic. It will be called when any changes need to be made by the PaneManager
    def update_panes(self):
        #clear existing variable pertaining to panes
        self.panes_controllers = {}
        self.panes = {}
        self.panes_status = {}
        self.panes_layouts = {}

        #remove all previous panes (which are QWidgets)
        while self.main_window.layout.count():
            widget_item = self.main_window.layout.takeAt(0)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        #create new list of panes and create them 
        self.create_pane_lists()
        self.create_panes()

#class that will be used once per each pane. It will be in charge of controlling which panels are displayed inside the pane 
    #update_pane_controller() should be called from outside of the class as it will call all other functions 
class PaneController(): 
    def __init__(self, title, pane_widget, main_window, parent=None):

        self.title = title
        self.main_window = main_window

        #pane_widget is the main widget created by Pane Manager, all label and data widgets will be created inside pane_widget
        self.pane_widget = pane_widget

        #define the layout of this pane widget to be vertical 
        self.layout = QVBoxLayout()
        self.pane_widget.setLayout(self.layout)
        
        #call the main update function for the PaneController
        self.update_pane_controller()

    #adds a title widget to the pane according to pane title 
    def add_pane_title(self):
        #create a QLabel widget and set its alignment to center top 
        self.label = QLabel(self.title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        #get its color from CPU color settings 
        color = self.main_window.settings["displays"][self.title]["color"]

        #define the style sheet and apply it to the label widget
        settings = "background-color: "+color+"; margin:2px; border:1px solid rgb(0, 0, 0); border-radius:10px;"
        self.label.setStyleSheet(settings)

        #make it fixed height 
        self.label.setFixedHeight(25)

        #add the label widget to pane_widgets layout
        self.layout.addWidget(self.label)
    
    def create_list_widgets(self):
        #create list of needed widgets in this pane 
        if self.title == "CPU" or self.title == "GPU":
            self.widgets_status["temp"] = self.main_window.settings["displays"][self.title]["temp"]
            self.widgets_status["util"] = self.main_window.settings["displays"][self.title]["util"]

    #function that adds widgets to the Pane, called recursively by add_widgets()
    def add_widget(self, title):
        #create the pane for "title" and store in panes list, store layout so we can access it later to add widgets, and set the layout
        self.widgets[title] = QWidget(self.pane_widget)
        self.widgets_layouts[title] = QVBoxLayout()
        self.widgets[title].setLayout(self.widgets_layouts[title])

        #define pane color
        color = self.main_window.settings["background_color"]

        #define pane stylesheet and apply
        settings = "background-color: "+color+"; margin:0px; border:1px solid rgb(0, 0, 0); border-radius:20px;"
        self.widgets[title].setStyleSheet(settings)

        #add fixed height title to each widget in the pane, and remove its borders 
        widget_title = QLabel(self.title_resolver(title))
        widget_title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        widget_title.setFixedHeight(25)#hardcoded value of 25 pixels, determined by experimentation 
        widget_title_settings = "background-color: "+color+"; margin:0px; border:1px solid rgb(0, 0, 0); border-radius:5px;"
        widget_title.setStyleSheet(widget_title_settings)
        self.widgets_layouts[title].addWidget(widget_title)

        #add a dummy number for now, later this will be client data 
        dummy_number = QLabel("55")
        dummy_number.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        dummy_number_settings = "background-color: "+color+"; margin:0px; border:1px solid rgb(0, 0, 0); font-size:75px; border-radius:20px;"
        dummy_number.setStyleSheet(dummy_number_settings)
        self.widgets_layouts[title].addWidget(dummy_number)

    #function to convert the short settings keys into full titles
    def title_resolver(self, title):
        if title == "temp":
            return "Temperature (C)"
        elif title == "util":
            return "Utilization (%)"
        else:
            return ""
    
    #function to loop over the list of widgets, and add any that are enabled
    def add_widgets(self):
        #loop over all pane statuses
        for i in self.widgets_status:
            #if widget is enabled 
            if self.widgets_status[i] == True:
                #create relevant panes, and add them to the central widget layout with title
                self.add_widget(i)
                self.layout.addWidget(self.widgets[i])
    
    #function that wraps all pane controller logic. It will be called when any changes need to be made by the PaneController
    def update_pane_controller(self):
        self.widgets = {}
        self.widgets_status = {}
        self.widgets_layouts = {}

        #remove all previous widgets added to the pane_widget
        while self.layout.count():
            widget_item = self.layout.takeAt(0)
            if widget_item.widget():
                widget_item.widget().deleteLater()
        
        #add title for entire pane
        self.add_pane_title()

        #create list of widgets to be added
        self.create_list_widgets()

        #add widgets according to current state of settings
        self.add_widgets()