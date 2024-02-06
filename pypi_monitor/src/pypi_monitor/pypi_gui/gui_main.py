import sys
import os
from datetime import datetime
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout,  QWidget
from PyQt6.QtGui import QIcon, QResizeEvent
from PyQt6.QtCore import Qt, QTimer

from pypi_monitor.pypi_gui import gui_settings
from pypi_monitor.pypi_gui import gui_utils
from pypi_monitor.pypi_client import client
from pypi_monitor.pypi_utils import set_settings_dirs

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #set all settings dirs based on OS
        set_settings_dirs.set_settings_dirs(self)

        #load the latest settings file 
        gui_settings.load_settings(self, self.settings_path)

        #start the client
        self.client = client.Client(self)

        #spawn the main window
        self.setWindowTitle('pypi_monitor')
        self.setGeometry(100, 100, 600, 400)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint) # this will make the window frameless

        #define central widget, and give it an QHBoxLayout with the top 25 rows being empty so we don't overlap settings button
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0,14,0,0)

        #get the script's directory and construct the relative path to the gear icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'imgs/gear.png')  # Use the transparent gear icon

        #create settings button 
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(icon_path))
        self.settings_button.setGeometry(1, 1, 15, 15)

        #setup settings controller and connect it to the button 
        self.settings_controller = gui_settings.SettingsController(self)
        self.settings_button.clicked.connect(self.settings_controller.open_settings)

        #setup the pane manager 
        self.pane_manager = gui_utils.PaneManager(self)


        #__init__ complete, allow the resizeEvent to run (which it will do when allowed to)
        time.sleep(3) #sleep just to debug and make sure everything inits before resizeEvent is allowed to run
        self.resize_update_flag = True

    #update all necessary changes
    def update_settings(self):
        gui_utils.set_main_background_color(self, self.settings["background_color"]) #background color
        self.pane_manager.update_panes() #panes
        self.client.data_client.queue.update_request_settings() #http request settings 
        self.settings_controller.settings_dialog.file_settings_page.update_rate_slider() #update rate

    #resizeEvent, but it users a flag to make sure we don't call update_settings() more than once every 0.5 seconds (resizeEvent happens many times very fast)
    def resizeEvent(self, event):
        if self.resize_update_flag:
            print("resizing and updating")
            self.resize_update_flag = False
            self.update_settings()
            QTimer.singleShot(500, lambda: setattr(self, "resize_update_flag", True))#do not set resize_update_flag back to false until 0.5 seconds has passed 
        super().resizeEvent(event)


    #debugging function to see current settings 
    def print_settings(self):

        print(self.settings)

#add a function to start the app so poetry can link it to a cmd line verb to run the gui
def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()#showMaximized() will make the window full screen
    sys.exit(app.exec())    

#run the app
if __name__ == '__main__':
    run_app()