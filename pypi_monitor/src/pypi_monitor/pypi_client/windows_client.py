import requests
import time
import threading


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
        self.main_window.data = {}
        self.update_request_settings()
        self.start_request_loop()

    # function that will update params for the https request
    # should be called anytime a IPDialog settings change was made
    def update_request_settings(self):
        # update to new settings and reconstruct the url for the get request
        self.update_rate = int(self.main_window.settings["update_rate"])
        self.ip = self.main_window.settings["ip"]
        self.port = self.main_window.settings["port"]
        self.is_running = self.main_window.settings["is_running"]
        self.url = "http://" + self.ip + ":" + self.port + "/api/rootnode"

    # function that starts the client data queue in a thread
    def start_request_loop(self):
        self.is_running = True
        # daemon thread so thread dies when the script that started it dies
        # in this case the script that starts it is (gui_main.py)
        self.thread = threading.Thread(target=self.data_request, daemon=True)
        self.thread.start()

    # function that stops the client data queue thread
    def stop_request_loop(self):
        self.is_running = False
        if self.thread:
            # wait 5 seconds for thread to finish then kill it
            self.thread.join(5)

    # main loop that will send out the https requests to cather data
    def data_request(self):
        while self.is_running:
            try:
                self.main_window.data = requests.get(self.url)
                print(self.main_window.data)
                # in the future call the data_dumper function
            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(self.update_rate)

    # function to dump the requests data out into json, then into dicts
    # def data_dumper(self):
        # self.main_window.data["CPU"] = cpu data from request
        # after data is dumped and stored, call update pane_manager
            # pane manager will grab client data and display it
