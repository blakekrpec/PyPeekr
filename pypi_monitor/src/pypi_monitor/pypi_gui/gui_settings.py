import os
import ipaddress
import yaml
from PyQt6.QtWidgets import QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QColorDialog, QTabWidget, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt

from pypi_monitor.pypi_gui import gui_utils
from pypi_monitor.pypi_gui import gui_main

#define the settings controller
class SettingsController:
    def __init__(self, parent):
        self.parent = parent
        self.settings_dialog = SettingsDialog(parent)

    #this function is called to open the QDialog settings page
    def open_settings(self):

        self.settings_dialog.exec()

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
        self.file_settings_page = FileSettingsPage(main_window, self)
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
        self.layout = QVBoxLayout(self)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)

        #add in the widgets we defined
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    #function to save current settings 
    def save_settings(self):
        #dump current global settings object into a yaml
        with open(self.main_window.settings_path, 'w') as file:
            yaml.dump(self.main_window.settings, file, default_flow_style=False)

    #functions to reset all settings to defaults 
    def reset_settings(self):
        load_settings(self.main_window, self.main_window.default_settings_path)
        self.main_window.update_settings()

#function to load settings from a yaml file
def load_settings(main_window, settings_file):
    #open passed settings if it exists and then store them into global settings object
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            main_window.settings = yaml.full_load(file)

#create a file tab on settings page
class FileSettingsPage(QWidget):
    def __init__(self, main_window, parent=None):
        super(FileSettingsPage, self).__init__(parent)

        self.main_window = main_window

        self.layout = QVBoxLayout(self)
        # Add your file settings widgets here
        self.setLayout(self.layout)

        self.ip_dialog = IPDialog(main_window)

        #button to open IPDialog
        self.ip_button = QPushButton('IP Address')
        self.ip_button.clicked.connect(self.ip_pressed)
        self.layout.addWidget(self.ip_button)
    
    #function for when the the IP Address button is pressed
    def ip_pressed(self):
        #update the current ip label in the ip dialog since it is defined once when the dialog is init above, we have to manually update it here
        self.ip_dialog.current_ip_label.setText(self.ip_dialog.make_ip_label())
        #start the dialog
        self.ip_dialog.exec()


#Dialog that will show the current IP, and allow user to change to a new one
class IPDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super(IPDialog, self).__init__(parent)
        self.setWindowTitle('IP Address')
        self.setGeometry(200, 200, 250, 130)
        self.main_window = main_window

        #create layout
        self.layout = QVBoxLayout(self)

        #show the current IP address in settings 
        self.current_ip_label = QLabel(self.make_ip_label())
        self.layout.addWidget(self.current_ip_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        #add option for the user to change the ip in settings 
        self.change_ip = QLineEdit("Change IP Here...")
        self.layout.addWidget(self.change_ip)

        #button to save the new ip 
        self.save_ip_button = QPushButton('Save IP Address', self)
        self.save_ip_button.clicked.connect(self.save_ip)
        self.layout.addWidget(self.save_ip_button)
    
    #simple function that will grab the current ip and make a string to it
    def make_ip_label(self):
        label = "Current IP Address: " + self.main_window.settings["ip"]
        return label

    #function for when the save ip button is pressed
    def save_ip(self):
        #make sure the user didn't hit save ip without entering anything 
        if self.change_ip.text() != "Change IP Here...":
            #check that the ip is valid
            if self.check_ip(self.change_ip.text()):
                #create update message that we will later show user
                msg_string = "IP address updated from " + self.main_window.settings["ip"] + " to " + self.change_ip.text() + "."

                #update the new IP entered in settings and update label to show now current ip
                self.main_window.settings["ip"]=self.change_ip.text()
                self.current_ip_label.setText(self.make_ip_label())

                #give success message
                success_msg = QMessageBox(self)
                success_msg.setIcon(QMessageBox.Icon.Information)
                success_msg.setText("IP Address Updated")
                success_msg.setWindowTitle("IP Address")
                success_msg.setInformativeText(msg_string)
                success_msg.exec()

                #update the QLineEdit with prompt again
                self.change_ip.setText("Change IP Here...")

            #warn user if the ip is not valid and reset prompt
            else:
                error_msg = QMessageBox(self)
                error_msg.setIcon(QMessageBox.Icon.Warning)
                error_msg.setText("Invalid IP Address")
                error_msg.setInformativeText("The entered address is not a valid IPv4 address.")
                error_msg.setWindowTitle("Error")
                error_msg.exec()
                self.change_ip.setText("Change IP Here...")

    #check if user provided ip is valid
    def check_ip(self, ip):
        #split the ip and make sure it has 4 parts
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        
        #check that each part is an int, and 0<int<255
        for part in parts:
            if not isinstance(int(part), int):
                return False
            elif int(part) < 0 or int(part) > 255:
                return False
            else:
                return True
                
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

        #init dialog for displays options
        self.displays_dialog = DisplaysDialog(main_window)

        #add displays button 
        self.displays_button = QPushButton('Displays')
        self.displays_button.clicked.connect(self.displays_dialog.exec)
        self.layout.addWidget(self.displays_button)

    #use the built in Qt color selector 
    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.settings["background_color"] = color.name() #get hex color code
            gui_utils.set_main_background_color(self.main_window, color) #set main window color

#the dialog ot run when the displays page is opened
class DisplaysDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super(DisplaysDialog, self).__init__(parent)
        self.setWindowTitle('Displays')
        self.setGeometry(200, 200, 400, 300)
        self.main_window = main_window

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create and add pages to the tab widget
        self.cpu_page = CPUPage(main_window, self)
        self.gpu_page = GPUPage(main_window, self)
        self.tab_widget.addTab(self.cpu_page, 'CPU')
        self.tab_widget.addTab(self.gpu_page, 'GPU')

        self.layout = QVBoxLayout(self)
        #add in the widgets we defined
        self.layout.addWidget(self.tab_widget)

#create a CPU tab in displays page
class CPUPage(QWidget):
    def __init__(self, main_window, parent=None):

        super(CPUPage, self).__init__(parent)
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        #create button to change color of cpu pannel
        self.cpu_color_button = QPushButton("CPU Panel Color", self)
        self.cpu_color_button.setCheckable(False)
        self.cpu_color_button.clicked.connect(lambda: self.cpu_color()) #link button to color picker fxn
        self.layout.addWidget(self.cpu_color_button)

        #create button to enable CPU stats 
        if main_window.settings["displays"]["CPU"]["enabled"]:
            self.cpu_enable_button = QPushButton("Disable CPU Stats", self)
        else:
            self.cpu_enable_button = QPushButton("Enable CPU Stats", self)          
        self.cpu_enable_button.setCheckable(True)
        self.cpu_enable_button.setChecked(main_window.settings["displays"]["CPU"]["enabled"])  #set cpu to enabled or disabled based on settings.yaml
        self.cpu_enable_button.clicked.connect(lambda: self.cpu_button_logic(self.cpu_enable_button)) #link to cpu button fxn
        self.layout.addWidget(self.cpu_enable_button)

        #create button to enable CPU temp stats
        self.cpu_temp_button = QPushButton("CPU Temp", self)
        self.cpu_temp_button.setCheckable(True)
        self.cpu_temp_button.setChecked(main_window.settings["displays"]["CPU"]["temp"]) #set cpu temp to enabled or disabled based on settings.yaml
        self.cpu_temp_button.clicked.connect(lambda: self.cpu_button_logic(self.cpu_temp_button)) #link to cpu button fxn
        self.layout.addWidget(self.cpu_temp_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        #create button to enable CPU util stats
        self.cpu_util_button = QPushButton("CPU Util %", self)
        self.cpu_util_button.setCheckable(True)
        self.cpu_util_button.setChecked(main_window.settings["displays"]["CPU"]["util"]) #set cpu util to enabled or disabled based on settings.yaml
        self.cpu_util_button.clicked.connect(lambda: self.cpu_button_logic(self.cpu_util_button))#link to cpu button fxn
        self.layout.addWidget(self.cpu_util_button, alignment=Qt.AlignmentFlag.AlignHCenter)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cpu_temp_button.setFixedWidth(self.cpu_enable_button.width() // 2)
        self.cpu_util_button.setFixedWidth(self.cpu_enable_button.width() // 2)
    
    #use the built in Qt color selector 
    def cpu_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.settings["displays"]["CPU"]["color"] = color.name() #get hex color code and store in global settings
        #call the settings updater
        self.main_window.update_settings() 

    #fxn to control the logic behind all cpu buttons 
    def cpu_button_logic(self, button):
        #if the user clicked enable button
        if button == self.cpu_enable_button:
            #if it was clicked to true/on
            if button.isChecked():
                #set temp and stat buttons to true, and update settings to show all cpu settings are now true
                self.cpu_temp_button.setChecked(True)
                self.main_window.settings["displays"]["CPU"]["temp"] = True
                self.cpu_util_button.setChecked(True)
                self.main_window.settings["displays"]["CPU"]["util"] = True
                self.main_window.settings["displays"]["CPU"]["enabled"] = True
                self.cpu_enable_button.setText("Disable CPU Stats")
            #if it was clicked to false/off
            else:
                #set temp and stat buttons to false, and update settings to show all cpu settings are now false
                self.cpu_temp_button.setChecked(False)
                self.main_window.settings["displays"]["CPU"]["temp"] = False
                self.cpu_util_button.setChecked(False)
                self.main_window.settings["displays"]["CPU"]["util"] = False
                self.main_window.settings["displays"]["CPU"]["enabled"] = False
                self.cpu_enable_button.setText("Enable CPU Stats")

        #if the cpu temp button was pressed
        if button == self.cpu_temp_button:
            #if cpu is currently enabled 
            if self.main_window.settings["displays"]["CPU"]["enabled"] == True:
                #if button was clicked to true/on
                if button.isChecked():
                    #update settings
                    self.main_window.settings["displays"]["CPU"]["temp"] = True
                #if button was clicked to false/off
                else:
                    #update settings
                    self.main_window.settings["displays"]["CPU"]["temp"] = False
            #if cpu is not enabled, ignore request to change state of temp and force it to false
            else:
                self.cpu_temp_button.setChecked(False)

        #if the cpu temp button was pressed
        if button == self.cpu_util_button:
            #if cpu is currently enabled 
            if self.main_window.settings["displays"]["CPU"]["enabled"] == True:
                #if button was clicked to true/on
                if button.isChecked():
                    #update settings
                    self.main_window.settings["displays"]["CPU"]["util"] = True
                #if button was clicked to false/off
                else:
                    #update settings 
                    self.main_window.settings["displays"]["CPU"]["util"] = False
            #if cpu is not enabled, ignore request to change state of util and force it to false
            else:
                self.cpu_util_button.setChecked(False)

        #if both temp and util are disabled, then set cpu enabled to false in settings, and set the button to false
        if self.main_window.settings["displays"]["CPU"]["temp"] == False and self.main_window.settings["displays"]["CPU"]["util"] == False:
            self.main_window.settings["displays"]["CPU"]["enabled"] = False
            self.cpu_enable_button.setChecked(False)

        #call the main settings updater
        self.main_window.update_settings()               

#create a GPU tab in displays page
class GPUPage(QWidget):
    def __init__(self, main_window, parent=None):

        super(GPUPage, self).__init__(parent)
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        #create button to change color of gpu pannel
        self.gpu_color_button = QPushButton("GPU Panel Color", self)
        self.gpu_color_button.setCheckable(False)
        self.gpu_color_button.clicked.connect(lambda: self.gpu_color()) #link button to color picker fxn
        self.layout.addWidget(self.gpu_color_button)

        #create button to enable GPU stats 
        if main_window.settings["displays"]["GPU"]["enabled"]:
            self.gpu_enable_button = QPushButton("Disable GPU Stats", self)
        else:
            self.gpu_enable_button = QPushButton("Enable GPU Stats", self)  
        self.gpu_enable_button.setCheckable(True)
        self.gpu_enable_button.setChecked(main_window.settings["displays"]["GPU"]["enabled"])  #set gpu to enabled or disabled based on settings.yaml
        self.gpu_enable_button.clicked.connect(lambda: self.gpu_button_logic(self.gpu_enable_button)) #link to gpu button fxn
        self.layout.addWidget(self.gpu_enable_button)

        #create button to enable GPU temp stats
        self.gpu_temp_button = QPushButton("GPU Temp", self)
        self.gpu_temp_button.setCheckable(True)
        self.gpu_temp_button.setChecked(main_window.settings["displays"]["GPU"]["temp"]) #set gpu temp to enabled or disabled based on settings.yaml
        self.gpu_temp_button.clicked.connect(lambda: self.gpu_button_logic(self.gpu_temp_button)) #link to gpu button fxn
        self.layout.addWidget(self.gpu_temp_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        #create button to enable GPU util stats
        self.gpu_util_button = QPushButton("GPU Util %", self)
        self.gpu_util_button.setCheckable(True)
        self.gpu_util_button.setChecked(main_window.settings["displays"]["GPU"]["util"]) #set gpu util to enabled or disabled based on settings.yaml
        self.gpu_util_button.clicked.connect(lambda: self.gpu_button_logic(self.gpu_util_button))#link to gpu button fxn
        self.layout.addWidget(self.gpu_util_button, alignment=Qt.AlignmentFlag.AlignHCenter)

    #anytime the displays window is changes, update the temp and util buttons to be half as wide an enable
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gpu_temp_button.setFixedWidth(self.gpu_enable_button.width() // 2)
        self.gpu_util_button.setFixedWidth(self.gpu_enable_button.width() // 2)
    
    #use the built in Qt color selector 
    def gpu_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.settings["displays"]["GPU"]["color"] = color.name() #get hex color code and store in global settings
        #call the settings updater
        self.main_window.update_settings() 

    #fxn to control the logic behind all gpu buttons 
    def gpu_button_logic(self, button):
        #if the user clicked enable button
        if button == self.gpu_enable_button:
            #if it was clicked to true/on
            if button.isChecked():
                #set temp and stat buttons to true, and update settings to show all gpu settings are now true
                self.gpu_temp_button.setChecked(True)
                self.main_window.settings["displays"]["GPU"]["temp"] = True
                self.gpu_util_button.setChecked(True)
                self.main_window.settings["displays"]["GPU"]["util"] = True
                self.main_window.settings["displays"]["GPU"]["enabled"] = True
                self.gpu_enable_button.setText("Disable GPU Stats")
            #if it was clicked to false/off
            else:
                #set temp and stat buttons to false, and update settings to show all gpu settings are now false
                self.gpu_temp_button.setChecked(False)
                self.main_window.settings["displays"]["GPU"]["temp"] = False
                self.gpu_util_button.setChecked(False)
                self.main_window.settings["displays"]["GPU"]["util"] = False
                self.main_window.settings["displays"]["GPU"]["enabled"] = False
                self.gpu_enable_button.setText("Enable GPU Stats")

        #if the gpu temp button was pressed
        if button == self.gpu_temp_button:
            #if gpu is currently enabled 
            if self.main_window.settings["displays"]["GPU"]["enabled"] == True:
                #if button was clicked to true/on
                if button.isChecked():
                    #update settings
                    self.main_window.settings["displays"]["GPU"]["temp"] = True
                #if button was clicked to false/off
                else:
                    #update settings
                    self.main_window.settings["displays"]["GPU"]["temp"] = False
            #if gpu is not enabled, turn on GPU enable and temp
            else:
                self.gpu_temp_button.setChecked(False)

        #if the gpu temp button was pressed
        if button == self.gpu_util_button:
            #if gpu is currently enabled 
            if self.main_window.settings["displays"]["GPU"]["enabled"] == True:
                #if button was clicked to true/on
                if button.isChecked():
                    #update settings
                    self.main_window.settings["displays"]["GPU"]["util"] = True
                #if button was clicked to false/off
                else:
                    #update settings 
                    self.main_window.settings["displays"]["GPU"]["util"] = False
            #if gpu is not enabled, ignore request to change state of util and force it to false
            else:
                self.gpu_util_button.setChecked(False)

        #if both temp and util are disabled, then set gpu enabled to false in settings, and set the button to false
        if self.main_window.settings["displays"]["GPU"]["temp"] == False and self.main_window.settings["displays"]["GPU"]["util"] == False:
            self.main_window.settings["displays"]["GPU"]["enabled"] = False
            self.gpu_enable_button.setChecked(False)

        #call the main settings updater
        self.main_window.update_settings()     