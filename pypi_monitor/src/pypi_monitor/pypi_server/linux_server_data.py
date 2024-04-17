import psutil
import GPUtil


# class to get CPU info on Linux
class LinuxCPUData():
    def __init__(self) -> None:
        self.cpu_data = {}
        self.cpu_name = None
        self.cpu_temp = None
        self.cpu_util = None
        self.update_cpu_data()

    # main update fxn that calls all others
    def update_cpu_data(self):
        self.get_cpu_name()
        self.get_cpu_temp()
        self.get_cpu_util()
        self.cpu_data["name"] = self.cpu_name
        self.cpu_data["temp"] = self.cpu_temp
        self.cpu_data["util"] = self.cpu_util

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
            # intel cpus have coretemp
            if 'coretemp' in temps:
                # grab the temp reported by intel cpu (1st element)
                cpu_temp = temps['coretemp'][0].current
            # amd cpus have k10temp
            elif 'k10temp' in temps:
                # grab the temp reported by amd cpu (2nd element)
                # amd k10temp = {Tctl, Tdie, Tccd1}
                # Tdie (2nd element) is what is desired
                cpu_temp = temps['k10temp'][1].current
            self.cpu_temp = cpu_temp

    # get cpu utilzation with psutil
    # returns avg cpu util acorss all cores
    def get_cpu_util(self):
        if hasattr(psutil, "cpu_percent"):
            cpu_utilization = psutil.cpu_percent(interval=None)
            self.cpu_util = cpu_utilization


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

        # find any nvidia gpus
        nvidia_gpus = GPUtil.getGPUs()
        if nvidia_gpus:
            for gpu in nvidia_gpus:
                info = {
                    'name': gpu.name,
                    'temp': gpu.temperature,
                    'util': gpu.load * 100
                }
                gpus.update(info)

        # elif no nvidia gpus find amd gpus
        else:
            info = {
                    'name': "",
                    'temp': 0,
                    'util': 0
                }
            gpus.update(info)

        self.gpu_data = gpus

# class to get RAM info on Linux
class LinuxRAMData():
    def __init__(self) -> None:
        self.ram_data = {}
        self.ram_name = None
        self.ram_usage = None
        self.ram_util = None
        self.update_ram_data()

    # main update fxn that calls all others
    def update_ram_data(self):
        self.get_ram_usage()
        self.get_ram_util()
        self.ram_data["name"] = "RAM"
        self.ram_data["usage"] = self.ram_usage
        self.ram_data["util"] = self.ram_util

    # get ram usage using psutil module
    def get_ram_usage(self):
        usage_bytes = None
        usage_gb = None
        if hasattr(psutil, "virtual_memory"):
            usage_bytes = psutil.virtual_memory().used
            usage_gb = round(usage_bytes / (1024 * 1024 * 1024), 2)
            self.ram_usage = usage_gb

    # get ram utilization with psutil
    def get_ram_util(self):
        if hasattr(psutil, "virtual_memory"):
            ram_utilization = psutil.virtual_memory().percent
            self.ram_util = ram_utilization

# class to serve as the main data server
class LinuxDataServer():
    def __init__(self) -> None:
        self.server_data = {}
        self.cpu_data_obj = LinuxCPUData()
        self.server_cpu_data = None
        self.gpu_data_obj = LinuxGPUData()
        self.server_gpu_data = None
        self.ram_data_obj = LinuxRAMData()
        self.server_ram_data = None
        self.last_n_samples = {}
        self.update_linux_data_server()

    # function to update all values, will be called during HTTP request
    def update_linux_data_server(self):
        self.cpu_data_obj.update_cpu_data()
        self.gpu_data_obj.update_gpu_data()
        self.ram_data_obj.update_ram_data()
        self.server_data["CPU"] = self.cpu_data_obj.cpu_data
        self.server_data["GPU"] = self.gpu_data_obj.gpu_data
        self.server_data["RAM"] = self.ram_data_obj.ram_data