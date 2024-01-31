class LinuxClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.cpu_queue = self.LinuxCPUQueue(self.main_window)
        self.gpu_queue = self.LinuxGPUQueue(self.main_window)

class LinuxCPUQueue():
    def __init__(self, main_window):
        dummy = 0

class LinuxGPUQueue():
    def __init__(self, main_window):
        dummy =0