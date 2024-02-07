import os
from pypi_monitor import __name__
import shutil
import platform
from pathlib import Path


# create location to store settings if it doesn't exist
def create_config_dir():

    # create directory outside the project where we will store settings.
    # This will protect users IP from the git repo.

    # if windows
    if platform.platform().split('-')[0] == 'Windows':
        config_dir = str(Path.home())+"\\.config\\pypi_monitor"
        if not os.path.exists(config_dir):
            print("creating dir")
            os.makedirs(config_dir)

        # construct file path to default settings
        file_path = "..\\pypi_gui\\settings\\default_settings.yaml"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_settings = os.path.join(script_dir, file_path)

        # construct file path to where we want to save settings
        settings_file = config_dir + "\\settings.yaml"
        default_file = config_dir + "\\default_settings.yaml"

        # copy default settings twice
        # once to settings.yaml and once to default_settings.yaml
        shutil.copy(default_settings, settings_file)
        shutil.copy(default_settings, default_file)

    # else linux
    else:
        config_dir = str(Path.home())+"/.config/pypi_monitor"
        if not os.path.exists(config_dir):
            print("creating dir")
            os.makedirs(config_dir)

        # construct file path to default settings
        file_path = "../pypi_gui/settings/default_settings.yaml"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_settings = os.path.join(script_dir, file_path)

        # construct file path to where we want to save settings
        settings_file = config_dir + "/settings.yaml"
        default_file = config_dir + "/default_settings.yaml"

        # copy default settings twice
        # once to settings.yaml and once to default_settings.yaml
        shutil.copy(default_settings, settings_file)
        shutil.copy(default_settings, default_file)


if __name__ == "__main__":
    create_config_dir()
