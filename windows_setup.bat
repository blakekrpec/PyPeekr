@echo off

setlocal

REM Check for Python 3
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python is not installed.
    echo Install Python 3 from the official page: https://www.python.org/downloads/
    echo An easy way to do this is to get the latest Python version from the Windows Store.
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do (
    set "version=%%a"
)

set "major_version=%version:~0,1%"
if %major_version% geq 3 (
    echo Python %version% is installed. Version is 3 or higher.
) else (
    echo WARNING: Python version is less than 3. Current version is %version%
    echo Please install Python 3 or higher.
    exit /b 1
)

REM Check if virtualenv is installed
pip show virtualenv > nul 2>&1
if %errorlevel% equ 0 (
    echo Virtualenv is already installed.
) else (
    echo Installing virtualenv...
    pip install virtualenv
    if %errorlevel% neq 0 (
        echo Failed to install virtualenv. Exiting.
        exit /b 1
    )
)

REM Create venv
echo Checking if a pyvenv exists, if not will create it.
if exist .pypeekr (
    choice /c yn /m "The venv already exists. Do you want to override it?"
    if errorlevel 2 (
        echo Skipping venv creation.
    ) else (
        rmdir /s /q .pypeekr
        python -m venv .pypeekr
    )
) else (
    echo Creating the pyvenv.
    python -m venv .pypeekr
)

REM Activate venv
echo Activating the pyvenv.
call .pypeekr\Scripts\activate.bat

REM Upgrade pip if necessary
for /f "tokens=2 delims== " %%V in ('pip --version ^| findstr /r /c:"^[^ ]* "') do set "pip_version=%%V"
if not "%pip_version%" geq "23.0.0" (
    echo Updating pip...
    python3 -m pip install --upgrade pip
    echo Pip updated successfully.
)

REM Install pypi_monitor with pip
echo Installing pypeekr.
pip install -e ./pypeekr

REM create the config dir 
create_config_dir

echo Setup complete.

:end
endlocal
