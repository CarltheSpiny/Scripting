@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on your system.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Install required Python libraries using requirements.txt
if exist requirements.txt (
    echo Installing required Python libraries...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, skipping library installation.
)

:: Run the Python script
echo Running your Python script...
python reserve_room.py

pause
