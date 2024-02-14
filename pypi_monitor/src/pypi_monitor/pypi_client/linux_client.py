import requests
import time
import threading
from collections import defaultdict


# main data client class
class DataClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = DataQueue(self.main_window)


# queue for grabbing incoming data
class DataQueue():
    def __init__(self, main_window):
        # init loop and start it
        self.main_window = main_window
        # init list to be at least two layers deep
        # other indices under CPU/GPu etc will be added later dynamically
        self.main_window.data = {
         "CPU": {
                "name": ""
            },
         "GPU": {
                "name": ""
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
            self.is_running = False
            self.stop_request_loop()
        else:
            self.is_running = True
            self.start_request_loop()

    # function that will reset the stat values (min/max/avg)
    def handle_data_reset(self):
        self.last_n_datums = {}

    # function that starts the client data queue in a thread
    def start_request_loop(self):
        # self.is_running = True
        # daemon thread so thread dies when the script that started it dies
        # in this case the script that starts it is (gui_main.py)
        self.thread = threading.Thread(target=self.data_request, daemon=True)
        self.thread.start()

    # function that stops the client data queue thread, shouldn't need ever
    def stop_request_loop(self):
        # self.is_running = False
        if self.thread:
            # kill the thread
            self.thread.join(0)

    # main loop that will send out the https requests to cather data
    def data_request(self):
        while True:
            try:
                # get data from request and pass to data dumper
                response = requests.get(self.url, timeout=2)
                self.data_dumper(response)
            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(self.update_rate)

    # function to dump the requests data out into json, then into dicts
    def data_dumper(self, response):
        self.main_window.data["CPU"]["name"] = response.json()["CPU"]["name"]
        self.main_window.data["GPU"]["name"] = response.json()["GPU"]["name"]

        self.update_handler("CPU", "temp", response)
        self.update_handler("CPU", "util", response)
        self.update_handler("GPU", "temp", response)
        self.update_handler("GPU", "util", response)

        print("main data")
        print(self.main_window.data)

    # handles the updating of min, max, and averages on update
    def update_handler(self, title, key, response):

        self.main_window.data[title][key] = response.json()[title][key]
        min_key = "min_" + key
        max_key = "max_" + key
        avg_key = "avg_" + key

        if title not in self.last_n_datums:
            self.last_n_datums[title] = {}

        if key not in self.last_n_datums[title]:
            self.last_n_datums[title][key] = []

        if len(self.last_n_datums[title][key]) == 0:
            self.main_window.data[title][min_key] = self.main_window.data[title][key]
            self.main_window.data[title][max_key] = self.main_window.data[title][key]
            self.main_window.data[title][avg_key] = self.main_window.data[title][key]
            self.last_n_datums[title][key].append(self.main_window.data[title][key])

        if len(self.last_n_datums[title][key]) < 10:
            self.last_n_datums[title][key].append(self.main_window.data[title][key])
        else:
            self.last_n_datums[title][key].pop(0)
            self.last_n_datums[title][key].append(self.main_window.data[title][key])
            self.main_window.data[title][avg_key] = round(sum(self.last_n_datums[title][key]) / len(self.last_n_datums[title][key]), 1)

        if self.main_window.data[title][key] < self.main_window.data[title][min_key]:
            self.main_window.data[title][min_key] = self.main_window.data[title][key]
        if self.main_window.data[title][key] > self.main_window.data[title][max_key]:
            self.main_window.data[title][max_key] = self.main_window.data[title][key]