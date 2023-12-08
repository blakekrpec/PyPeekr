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

Launch OpenHardwareMonitor and make the following changes to settings: TODO



### Client 
The client is a Qt GUI written in python intended to run on a RaspberryPi. However, being in python, portability to other OS shouldn't be too painful. 

The client lives in the pypi_monitor pip package. The setup.sh script included will create a python virtual environment for you, and install pypi_monitor in it.

Run the setup
```
./setup.sh
```
Source the python virtual environment
```
source .pypi_monitor/bin/activate
```
Start the client GUI
```
client
```


