import psutil
import GPUtil


# class to get CPU info on Linux
class LinuxCPUData():
    def __init__(self) -> None:
        self.cpu_data = {}
        self.cpu_name = None
        self.cpu_temp = None
        self.cpu_utilzn = None
        self.update_cpu_data()

    # main update fxm that calls all others
    def update_cpu_data(self):
        self.get_cpu_name()
        self.get_cpu_temp()
        self.get_cpu_utilzn()
        self.cpu_data["name"] = self.cpu_name
        self.cpu_data["temp"] = self.cpu_temp
        self.cpu_data["utilzn"] = self.cpu_utilzn

    # get cpu name
    def get_cpu_name(self):
        cpu_name = None
        # open file on to get cpu name and parse it
        with open('/proc/cpuinfo', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    if line.rstrip('\n').startswith('model name'):
                        cpu_name = line.rstrip('\n').split(':')[1].strip()
                        self.cpu_name = cpu_name
                        break

    # get cpu temp using psutil module
    def get_cpu_temp(self):
        cpu_temp = None
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                cpu_temp = temps['coretemp'][0].current
        self.cpu_temp = cpu_temp

    #get cpu utilzation with psutil
    def get_cpu_utilzn(self):
        cpu_utilization = psutil.cpu_percent(interval=None)
        self.cpu_utilzn = cpu_utilization


# class to get GPU info on Linux
class LinuxGPUData():
    def __init__(self) -> None:
        self.gpu_data = {}
        self.gpu_names = []
        self.gpu_temp = None
        self.gpu_utilzn = None
        self.update_gpu_data()

    # single fxn that gets all nvidia gpu info 
    # can handle multiple gpus
    def update_gpu_data(self):
        gpus = {}

        nvidia_gpus = GPUtil.getGPUs()
        for gpu in nvidia_gpus:
            info = {
                'name': gpu.name,
                'temperature': gpu.temperature,
                'utilzn': gpu.load * 100
            }
            gpus.update(info)

        self.gpu_data = gpus


# main server that calls data from all components
class LinuxDataServer():
    def __init__(self) -> None:
        self.server_data = {}
        self.cpu_data_obj = LinuxCPUData()
        self.server_cpu_data = None
        self.gpu_data_obj = LinuxGPUData()
        self.server_gpu_data = None
        self.update_linux_data_server()

    # fxn to update all values, will be called during http request
    def update_linux_data_server(self):
        self.cpu_data_obj.update_cpu_data()
        self.server_data["CPU"] = self.cpu_data_obj.cpu_data
        self.server_data["GPU"] = self.gpu_data_obj.gpu_data
