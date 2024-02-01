import platform
from pathlib import Path

def set_settings_dirs(self):
    # self.main_window = main_window
    #if windows set paths to settings, and default_settings
    if platform.platform().split('-')[0] == 'Windows':
        config_dir = str(Path.home())+"\\.config\\pypi_monitor"
        settings_file = config_dir + "\\settings.yaml"
        default_file = config_dir + "\\default_settings.yaml" 
        self.settings_path = settings_file
        self.default_settings_path = default_file
    #else do the same on linux
    else:
        config_dir = str(Path.home())+"/.config/pypi_monitor"
        settings_file = config_dir + "/settings.yaml"
        default_file = config_dir + "/default_settings.yaml"
        self.settings_path = settings_file
        self.default_settings_path = default_file 