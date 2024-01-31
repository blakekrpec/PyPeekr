import platform

from pypi_monitor.pypi_client import windows_client
from pypi_monitor.pypi_client import linux_client

class Client():
    def __init__(self, main_window):
        #determine if on windows or linux
        self.os = platform.system()
        self.main_window = main_window

        if self.os == "Linux":
            self.main_window.client = linux_client.LinuxClient(self.main_window)
        elif self.os =="Windows":
            self.main_window.client = windows_client.WindowsClient(self.main_window)
