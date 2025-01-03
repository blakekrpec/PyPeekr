#! /bin/bash
CODENAME=$(sed -n -e '/DISTRIB_CODENAME/ s/.*\= *//p' /etc/lsb-release)

#weird step needed for qt6 to run on 22.04
sudo apt install libxcb-cursor0

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
echo "activating .pypeekr venv"
if [ -d .pypeekr ]; then
    # Directory exists
    read -p "The venv already exists. Do you want to override it? (y/n): " user_input
    if [ "$user_input" == "Y" ] || [ "$user_input" == "y" ]; then
        rm -rf .pypeekr
        python3 -m venv .pypeekr
    # elif [ "$user_input" == "N" || "$user_input" == "n"]; then   
    else
        echo "Invalid input. Please enter Y or N."
        exit
    fi
else
    python3 -m venv .pypeekr
fi

#activate the venv
source .pypeekr/bin/activate

#upgrade pip is out of date (less than 23.0.0)
current_version=$(pip --version | awk '{print $2}')
if [[ "$(printf '%s\n' "20.0.0" "$current_version" | sort -V | head -n1)" != "23.0.0" ]]; then 
    echo "Updating pip"
    pip install --upgrade pip
fi 

#install pypeekr with pip
pip install -e ./pypeekr

#create the config dir 
create_config_dir
