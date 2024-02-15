import platform

from pypi_monitor.pypi_client import windows_client
from pypi_monitor.pypi_client import linux_client


class Client():
    def __init__(self, main_window):
        # determine if on windows or linux and start appropriate data client
        self.os = platform.system()
        self.main_window = main_window

        if self.os == "Linux":
            self.data_client = linux_client.DataClient(self.main_window)
        elif self.os == "Windows":
            self.data_client = windows_client.DataClient(self.main_window)
