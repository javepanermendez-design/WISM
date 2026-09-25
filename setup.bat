@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3.14"
    echo [WIMS] Using Python launcher.
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
        echo [WIMS] Python launcher not found; falling back to python.
    ) else (
        echo [WIMS] Error: Python 3.14 or Python was not found on this machine.
        echo [WIMS] Install Python 3.10+ and rerun setup.bat.
        exit /b 1
    )
)

if not exist ".venv" (
    echo [WIMS] Creating virtual environment...
    call %PYTHON_CMD% -m venv .venv
) else (
    echo [WIMS] Virtual environment already exists.
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo [WIMS] Starting WIMS...
python run.py
