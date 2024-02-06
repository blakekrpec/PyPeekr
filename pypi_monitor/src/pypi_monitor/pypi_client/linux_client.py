class LinuxClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = self.Queue(self.main_window)


class Queue():
    def __init__(self, main_window):
        dummy = 0