@echo off
echo THIS SCRIPT IS UNTESTED
echo.

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

REM Check for Python venv
where pyvenv >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Python venv is already installed.
) else (
    echo Installing Python venv...
    REM Installing Python venv
    py -m ensurepip
    py -m pip install --upgrade pip
    py -m pip install virtualenv
    echo Python venv installed successfully.
)

REM Create venv
echo Activating .pypi_monitor venv...
if exist .pypi_monitor (
    set /p user_input="The venv already exists. Do you want to override it? (y/n): "
    if /i "%user_input%"=="y" (
        rmdir /s /q .pypi_monitor
        py -m venv .pypi_monitor
    ) else (
        echo Invalid input. Please enter Y or N.
        exit /b 1
    )
) else (
    py -m venv .pypi_monitor
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