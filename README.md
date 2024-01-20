# pypi_monitor
Tools to use a raspberry + display as a computer stat monitoring scree. 

The project is designed to have a server that hosts the computer stats over a local network. A client then grabs this data and presents it in a GUI on. 

Clone the project
```
git clone git@github.com:blakekrpec/pypi_monitor.git
```

### Server
[OpenHardwareMonitor](https://github.com/hexagon-oss/openhardwaremonitor) project as the server on Windows to host the pc information over the web. Future work aims to implement a Linux server as well, although this will likely be a custom implementation that mimics the data structure hosted by OpenHardwareMonitor.

To install OpenHardwareMonitor, grab the latest release [here](https://github.com/hexagon-oss/openhardwaremonitor/releases). Then follow the setup guide to complete installation. 

Launch OpenHardwareMonitor and make the following changes to settings:

    Enable run on startup
    Enable web server
    Enable remote access for the web server

### Client 
The client will be written in python and will listen for data from server, and send it to the gui to be displayed. 

### GUI
The gui is written in python with Qt. It spawns a client to listen to data from server, and displays it in the gui.

The gui, and client live in the pypi_monitor pip package. The linux_setup.sh script included will create a python virtual environment for you, and install pypi_monitor in it.

Run the setup
```
./linux_setup.sh
```
Source the python virtual environment
```
source .pypi_monitor/bin/activate
```
Start the client GUI
```
gui
```

On Windows Setup:

create venv
```
python -m venv .pypi_monitor
```
source venv
```
.\pypi_monitor\Scripts\activate
```
install pypi_monitor 
```
pip install -e .\pypi_monitor
```
run code 
```
gui
```

Current design:

- Client will be a RasPi on the LAN with a systemctl service to run the gui on startup.

- Server
    - On Linux, we will need to write our own server, or get the OpenHardwareMonitor.exe to run on Linux.
    - On Windows, the OpenHardwareMonitor REST API will be used. We should consider adding an abstraction layer that takes info from OpenHardwareMonitor and then makes it more portable, currently there is a ton of info and really we may only want CPU and GPU. 



- Done: 
    - Files separated for readability 
    - Settings functionality done (save and reset)
    - Settings button added to open settings dialog
    - Settings dialog has file and view tabs 
    - View tab added pick color ability 
    - View tab added displays button for displays dialog
    - Displays dialog done, has cpu and gpu tab
    - CPU and GPU tabs fleshed out, and now update the global settings in memory when interacted with.  
    - Added "gui" command with poetry to run the gui easily

- Next:
    - Create the pane manager. Will read from global settings and then spawn the number of panes with correct color, and temp util selections. 
    - Remove the enable button from cpu and gpu pages, but keep the enabled value in settings. It should work where if temp or util is selected for CPU or GPU, then the enabled value in settings is true, if none are selected then set enabled value to false in settings. This will mean we only have to check one value in settings to see if any cpu values are selected, but will remove the enabled button since it is kind of redundant.
