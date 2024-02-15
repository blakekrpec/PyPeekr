import sys
import os
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QPushButton, QHBoxLayout, QWidget)
from PyQt6.QtGui import QIcon

from pypi_monitor.pypi_gui import gui_settings
from pypi_monitor.pypi_gui import gui_utils
from pypi_monitor.pypi_client import client
from pypi_monitor.pypi_utils import set_settings_dirs


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # save the time when the gui was started
        self.start_time = datetime.now()

        # set all settings dirs based on OS
        set_settings_dirs.set_settings_dirs(self)

        # load the latest settings file
        gui_settings.load_settings(self, self.settings_path)

        # start the client
        # client signal to update pane manager will be connected later
        self.client = client.Client(self)

        # spawn the main window
        self.setWindowTitle('pypi_monitor')
        self.setGeometry(100, 100, 600, 400)

        # this will make the window frameless
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # define central widget, and give it an QHBoxLayout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QHBoxLayout(central_widget)
        # set the top 14 rows empty so we don't overlap settings button
        self.layout.setContentsMargins(0, 14, 0, 0)

        # get the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # construct the relative path to the gear icon
        icon_path = os.path.join(script_dir, 'imgs/gear.png')

        # create settings button
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(icon_path))
        self.settings_button.setGeometry(1, 1, 15, 15)

        # setup settings controller and connect it to the button
        self.settings_controller = gui_settings.SettingsController(self)
        self.settings_button.clicked.connect(
            self.settings_controller.open_settings)

        # setup the pane manager
        self.pane_manager = gui_utils.PaneManager(self)

        # connect client signal now that pane manager is spawned
        self.client.data_client.queue.updatePaneSignal.connect(
            self.pane_manager.update_panes)

        # update settings
        self.update_settings()

    # update all necessary changes
    def update_settings(self):
        # update main color (which also calls update_panes())
        gui_utils.set_main_background_color(
            self, self.settings["background_color"])
        # http request settings
        self.client.data_client.queue.update_request_settings()
        # update rate
        self.settings_controller.settings_dialog. \
            file_settings_page.update_rate_slider()

    # resizeEvent, but only after gui has been up for 0.5 seconds
        # (fixes race condition with update_settings() in __init__)
    def resizeEvent(self, event):
        # make sure the gui has been up for 0.5 seconds
        if (datetime.now() - self.start_time) > timedelta(seconds=0.5):
            self.update_settings()
        super().resizeEvent(event)

    # debugging function to see current settings :
    def print_settings(self):
        print(self.settings)


# add a function to start (so poetry can call this)
def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()  # showMaximized() will make the window full screen
    sys.exit(app.exec())


# run the app
if __name__ == '__main__':
    run_app()
