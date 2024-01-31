import platform

class Client():
    def __init__(self, main_window):
        #determine if on windows or linux
        self.os = platform.system()
        self.main_window = main_window

        if self.os == "Linux":
            self.main_window.client = LinuxClient()
        elif self.os =="Windows":
            self.main_window.client = WindowsClient()

class WindowsClient():
    def __init__(self, main_window):
        self.main_window = main_window
        dummy = 0

class LinuxClient():
    def __init__(self, main_window):
        self.main_window = main_window
        dummy = 0