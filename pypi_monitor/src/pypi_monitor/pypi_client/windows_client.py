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

        self.sensor_url = "http://" + self.ip + ":" + \
            self.port + "/Sensor"

        self.cpu_temp_params = dict(id="/intelcpu/0/temperature/26",
                                    action="Get")
        self.cpu_util_params = dict(id="/intelcpu/0/load/1",
                                    action="Get")
        self.gpu_temp_params = dict(id="/gpu-nvidia/0/temperature/0",
                                    action="Get")
        self.gpu_util_params = dict(id="/gpu-nvidia/0/load/0",
                                    action="Get")

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
                # get data from requests and pass to data dumper
                cpu_temp_response = requests.get(self.sensor_url,
                                                 params=self.cpu_temp_params,
                                                 timeout=2)

                cpu_util_response = requests.get(self.sensor_url,
                                                 params=self.cpu_util_params,
                                                 timeout=2)
                gpu_temp_response = requests.get(self.sensor_url,
                                                 params=self.gpu_temp_params,
                                                 timeout=2)

                gpu_util_response = requests.get(self.sensor_url,
                                                 params=self.gpu_util_params,
                                                 timeout=2)

                data_requests = {
                    "CPU": {"temp": cpu_temp_response,
                            "util": cpu_util_response},
                    "GPU": {"temp": gpu_temp_response,
                            "util": gpu_util_response}
                }
                self.data_dumper(data_requests)

                # can't call pane manager until it spawns
                # if self.main_window.pane_manager_spawned:
                self.updatePaneSignal.emit()

            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(self.update_rate)

    # dump organize the requests into dicts
    def data_dumper(self, data_requests):
        # grab the data from requests, and store in a dict
        cpu_dict = {"CPU": {
            "temp": data_requests["CPU"]["temp"].json()["value"],
            "util": data_requests["CPU"]["util"].json()["value"]
        }}

        # grab the data from requests, and store in a dict
        gpu_dict = {"GPU": {
            "temp": data_requests["GPU"]["temp"].json()["value"],
            "util": data_requests["GPU"]["util"].json()["value"]
        }}

        # call the function below to maintain stats
        self.data_update_handler("CPU", "temp", cpu_dict)
        self.data_update_handler("CPU", "util", cpu_dict)
        self.data_update_handler("GPU", "temp", gpu_dict)
        self.data_update_handler("GPU", "util", gpu_dict)

# handles the updating of min, max, and averages on update
    def data_update_handler(self, title, key, data):
        # grab main data of [key]
        self.main_window.data[title][key] = data[title][key]

        # create other stat keys
        min_key = "min_" + key
        max_key = "max_" + key
        avg_key = "avg_" + key

        # the requests have min and max values in them, but by maintaining
        # min and max within pypi_monitor min and max can be reset in the gui
        # without sending a reset request to LibreHardwareMonitor

        # if title or key are missing from last_n_datums add them
        if title not in self.last_n_datums:
            self.last_n_datums[title] = {}
        if key not in self.last_n_datums[title]:
            self.last_n_datums[title][key] = []

        # if first time, init last_n_dataum to current vals and append
        if len(self.last_n_datums[title][key]) == 0:

            self.main_window.data[title][min_key] = \
                self.main_window.data[title][key]

            self.main_window.data[title][max_key] = \
                self.main_window.data[title][key]

            self.main_window.data[title][avg_key] = \
                self.main_window.data[title][key]

            self.last_n_datums[title][key].append(
                self.main_window.data[title][key])

        # if not yet 10 datums, append and keep going
        if len(self.last_n_datums[title][key]) < 10:
            self.last_n_datums[title][key].append(
                self.main_window.data[title][key])

        # if 10 datums update avg
        else:
            # remove oldest datum
            self.last_n_datums[title][key].pop(0)
            # add newest datum
            self.last_n_datums[title][key].append(
                self.main_window.data[title][key])

        # update avg
        self.main_window.data[title][avg_key] = \
            round(sum(self.last_n_datums[title][key]) /
                  len(self.last_n_datums[title][key]), 1)
        # update min if needed
        if self.main_window.data[title][key] < \
           self.main_window.data[title][min_key]:
            self.main_window.data[title][min_key] = \
                self.main_window.data[title][key]
        # update max if needed
        if self.main_window.data[title][key] > \
           self.main_window.data[title][max_key]:
            self.main_window.data[title][max_key] = \
                self.main_window.data[title][key]