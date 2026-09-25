#!/bin/bash
set -eu

cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[WIMS] Error: Python 3 was not found on this machine."
  echo "[WIMS] Install Python 3.10+ and rerun setup.sh."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[WIMS] Creating virtual environment..."
  "$PYTHON_BIN" -m venv .venv
else
  echo "[WIMS] Virtual environment already exists."
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[WIMS] Starting WIMS..."
python run.py
