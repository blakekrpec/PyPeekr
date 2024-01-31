class WindowsClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.cpu_queue = self.WindowsCPUQueue(self.main_window)
        self.gpu_queue = self.WindowsGPUQueue(self.main_window)

class WindowsCPUQueue():
    def __init__(self, main_window):
        dummy = 0

class WindowsGPUQueue():
    def __init__(self, main_window):
        dummy =0