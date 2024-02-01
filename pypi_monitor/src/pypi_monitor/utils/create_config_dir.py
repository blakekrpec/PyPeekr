import os
from pypi_monitor import __name__
import shutil

#create location to store settings
def create_config_dir():

    #create directory outside the project where we will store settings. This will protect users IP from the git repo
    config_dir = os.getenv('HOME')+"/.config/pypi_monitor"
    if not os.path.exists(config_dir):
        print("creating dir")
        os.mkdir(config_dir)
    
    #construct file path to default settings 
    file_path = "../pypi_gui/settings/default_settings.yaml"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_settings = os.path.join(script_dir, file_path)

    #construct file path to where we want to save settings 
    settings_file = config_dir + "/settings.yaml"

    #copy default_settings into config dir as settings.yaml
    shutil.copy(default_settings, settings_file)
    
if __name__ == "__main__": 
    create_config_dir()