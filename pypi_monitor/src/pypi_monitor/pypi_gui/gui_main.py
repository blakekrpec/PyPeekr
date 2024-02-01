import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout,  QWidget
from PyQt6.QtGui import QIcon, QColor

from pypi_monitor.pypi_gui import gui_settings
from pypi_monitor.pypi_gui import gui_utils

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #load the latest settings file 
        gui_settings.load_settings(self)

        #spawn the main window
        self.setWindowTitle('Qt GUI Example')
        self.setGeometry(100, 100, 600, 400)

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

        #call the settings updater
        self.update_settings()

    #update all necessary changes
    def update_settings(self):
        #update background colors
        gui_utils.set_main_background_color(self, self.settings["background_color"])
        self.pane_manager.update_panes()
    
    #debugging function to see current settings 
    def print_settings(self):
        print(self.settings)

#add a function to start the app so poetry can link it to a cmd line verb to run the gui
def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())    

#run the app
if __name__ == '__main__':
    run_app()