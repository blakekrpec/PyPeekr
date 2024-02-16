@echo off

setlocal

REM Check for Python 3
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Python 3 is already installed.
) else (
    echo Installing Python 3...
    REM Installing Python 3 using Chocolatey
    choco install python3
    echo Python 3 installed successfully.
)

REM Check if virtualenv is installed
python -c "import virtualenv" 2>nul
if %errorlevel% neq 0 (
    echo Installing virtualenv...
    pip install virtualenv
    if %errorlevel% neq 0 (
        echo Failed to install virtualenv. Exiting.
        exit /b 1
    )
    echo Virtualenv installed successfully.
) else (
    echo Virtualenv is already installed.
)

REM Create venv
echo Activating .pypi_monitor venv...
if exist .pypi_monitor (
    choice /c yn /m "The venv already exists. Do you want to override it?"
    if errorlevel 2 (
        echo Skipping venv creation.
    ) else (
        rmdir /s /q .pypi_monitor
        python -m venv .pypi_monitor
    )
) else (
    python -m venv .pypi_monitor
)

REM Activate venv
call .pypi_monitor\Scripts\activate.bat

REM Upgrade pip if necessary
for /f "tokens=2 delims== " %%V in ('pip --version ^| findstr /r /c:"^[^ ]* "') do set "pip_version=%%V"
if not "%pip_version%" geq "23.0.0" (
    echo Updating pip...
    python -m pip install --upgrade pip
    echo Pip updated successfully.
)

REM Install pypi_monitor with pip
pip install -e ./pypi_monitor

REM create the config dir 
create_config_dir

:end
endlocal
