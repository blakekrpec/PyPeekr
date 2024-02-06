import requests
import time
import threading

class WindowsClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = DataQueue(self.main_window)


class DataQueue():
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.data = {}
        self.start_request_loop()
    
    def update_request_settings(self):
        self.update_rate = int(self.main_window.settings["update_rate"])
        self.ip = self.main_window.settings["ip"]
        self.port = self.main_window.settings["port"]
        self.is_running = self.main_window.settings["is_running"]
        self.url = "http://" + self.ip + ":" + self.port + "/api/rootnode"
    
    def start_request_loop(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.data_request, daemon=True)
        self.thread.start()

    def stop_request_loop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(5) # wait for the thread to finish with a 5 second timeout

    def data_request(self):
        while self.is_running:
            self.update_request_settings()
            try:
                self.main_window.data = requests.get(self.url)
                # print(self.main_window.data.json())
            except requests.RequestException as e:
                print(f"Error: {e}")
            time.sleep(self.update_rate)
