@echo off

REM Navigate to your project directory
cd /d "E:\Jarvis-v13"

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run your Python script
python main.py

REM Optional: Deactivate the virtual environment after the script finishes
call deactivate
