import requests
import time
import threading
from PyQt6.QtCore import QObject, pyqtSignal


# main data client class
class DataClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = DataQueue(self.main_window)


# queue for grabbing incoming data
class DataQueue(QObject):

    # this signal will call the update panes function in pane manager
    # cannot call function directly from the threaded while loop below
    updatePaneSignal = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        # init loop and start it
        self.main_window = main_window
        # init list with 0s to avoid crashes if server isn't reached
        # other indices under CPU/GPu etc will be added later dynamically
        self.main_window.data = {
         "CPU": {
                "name": "",
                "temp": 0,
                "min_temp": 0,
                "max_temp": 0,
                "avg_temp": 0,
                "util": 0,
                "min_util": 0,
                "max_util": 0,
                "avg_util": 0
            },
         "GPU": {
                "name": "",
                "temp": 0,
                "min_temp": 0,
                "max_temp": 0,
                "avg_temp": 0,
                "util": 0,
                "min_util": 0,
                "max_util": 0,
                "avg_util": 0
            }
        }

        self.last_n_datums = {}

        # start on init
        self.is_running = True
        self.update_request_settings()
        self.start_request_loop()

    # function that will update params for the https request
    # should be called anytime a IPDialog settings change was made
    def update_request_settings(self):
        # update to new settings and reconstruct the url for the get request
        self.update_rate = int(self.main_window.settings["update_rate"])
        self.ip = self.main_window.settings["ip"]
        self.port = self.main_window.settings["port"]
        self.url = "http://" + self.ip + ":" + self.port + "/data"

    # handle pause requests from the pause button
    def handle_pause_resume(self, action):
        if action == "pause":
            self.stop_request_loop()
        elif action == "resume":
            self.start_request_loop()

    # function that will reset the stat values (min/max/avg)
    def handle_data_reset(self):
        self.last_n_datums = {}

    # function that starts the client data queue in a thread
    def start_request_loop(self):
        self.is_running = True
        # daemon thread so thread dies when the script that started it dies
        # in this case the script that starts it is (gui_main.py)
        self.thread = threading.Thread(target=self.data_request, daemon=True)
        self.thread.start()

    # function that stops the client data queue thread, shouldn't need ever
    def stop_request_loop(self):
        self.is_running = False
        if self.thread:
            # kill the thread
            self.thread.join()

    # main loop that will send out the https requests to cather data
    def data_request(self):
        while self.is_running:
            try:
                # get data from request and pass to data dumper
                # response = requests.get(self.url, timeout=2)
                # self.data_dumper(response)

                # can't call pane manager until it spawns
                # if self.main_window.pane_manager_spawned:
                self.updatePaneSignal.emit()

            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(self.update_rate)

    # def data_dumper(self):
        # handle data here
