import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QColorDialog, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QColor

from pypi_monitor.pypi_gui import gui_settings
from pypi_monitor.pypi_gui import gui_utils
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #spawn window
        self.setWindowTitle('Qt GUI Example')
        self.setGeometry(100, 100, 600, 400)

        #get the script's directory and construct the relative path to the gear icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'imgs/gear.png')  # Use the transparent gear icon

        #create settings button 
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(icon_path))
        self.settings_button.setGeometry(10, 10, 15, 15)

        #setup settings controller and connect it to the button 
        self.settings_controller = gui_settings.SettingsController(self)
        self.settings_button.clicked.connect(self.settings_controller.open_settings)

        #initial load and update of settings 
        self.settings_controller.settings_dialog.load_settings()
        self.update_settings()

    #update all necessary changes
    def update_settings(self):
        
        #update background colors
        gui_utils.set_main_background_color(self, self.settings["background_color"])

#run the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())