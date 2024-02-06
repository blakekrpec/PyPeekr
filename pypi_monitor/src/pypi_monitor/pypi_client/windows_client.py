import requests

class WindowsClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = self.Queue(self.main_window)


class DataQueue():
    def __init__(self, main_window):
        self.main_window = main_window
        self.ip = self.main_window.settings["ip"]
        self.url = "http"+self.ip+":"+"self.port"
        self.interval = 1
        self.is_running = self.main_window.settings["is_running"]
