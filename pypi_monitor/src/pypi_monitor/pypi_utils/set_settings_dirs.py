import platform
from pathlib import Path

def set_settings_dirs(self):
    #if windows set paths to settings, and default_settings
    if platform.platform().split('-')[0] == 'Windows':
        config_dir = str(Path.home())+"\\.config\\pypi_monitor"
        settings_file = config_dir + "\\settings.yaml"
        default_file = config_dir + "\\default_settings.yaml" 
        self.settings_path = settings_file
        self.default_settings_path = default_file
    #elif do the same on linux
    elif platform.platform().split('-')[0] == 'Linux':
        config_dir = str(Path.home())+"/.config/pypi_monitor"
        settings_file = config_dir + "/settings.yaml"
        default_file = config_dir + "/default_settings.yaml"
        self.settings_path = settings_file
        self.default_settings_path = default_file 
    #modify the above blocks into a new elif as needed... you brave crusader
    else:
        print("OS not supported. Supported OSs are Windows and Linux.")