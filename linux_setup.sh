#! /bin/bash
CODENAME=$(sed -n -e '/DISTRIB_CODENAME/ s/.*\= *//p' /etc/lsb-release)

#check for python3
if command -v python3 &>/dev/null; then
    echo "Python 3 is already installed."
else
    # Install Python 3
    echo "Installing Python 3..."
    sudo apt update
    sudo apt install -y python3
    echo "Python 3 installed successfully."
fi

#check for python3-venv
if dpkg -s python3-venv &>/dev/null; then
    echo "python3-venv is already installed."
else
    # Install python3-venv
    echo "Installing python3-venv..."
    sudo apt install -y python3-venv
    echo "python3-venv installed successfully."
fi

# Check if the directory .test exists
echo "activating .pypi_monitor venv"
if [ -d .pypi_monitor ]; then
    # Directory exists
    read -p "The venv already exists. Do you want to override it? (y/n): " user_input
    if [ "$user_input" == "Y" ] || [ "$user_input" == "y" ]; then
        rm -rf .pypi_monitor
        python3 -m venv .pypi_monitor
    # elif [ "$user_input" == "N" || "$user_input" == "n"]; then   
    else
        echo "Invalid input. Please enter Y or N."
        exit
    fi
else
    python3 -m venv .pypi_monitor
fi

#activate the venv
source .pypi_monitor/bin/activate

#install pypi_monitor with pip
pip install -e ./pypi_monitor