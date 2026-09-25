# WIMS
Warehouse Inventory & Order Management System prototype for Ilocos Grocers Distribution Center.

## Quick start
- Windows: `setup.bat`
- Mac/Linux: `bash setup.sh`

This creates or reuses a local virtual environment, installs the project dependencies, and starts the app automatically. Open http://127.0.0.1:5000 when the terminal shows the app is running.

## Requirements
- Python 3.10+
- This project was built and tested on Python 3.14
- No separate database or login setup is required; the demo app uses in-memory data only

## Demo login
Use the demo warehouse account:
- Email: `admin@gmail.com`
- Password: `warehouse`

## Manual setup
If you prefer to set everything up yourself instead of using the script:

### Windows
```bat
py -3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

### Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

## Running tests
```bash
pytest
```

## Project structure
```text
wims/
  domain/          Business rules, entities, enums, and validation
  services/        Use cases for auth, dashboard, inventory, orders, and receiving
  repositories/    In-memory repository implementations
  web/             Flask routes and page handlers
templates/         Jinja templates for all pages and shared layout
static/           CSS, JS, and front-end assets
tests/            Pytest smoke and domain tests
```

## Notes
- This app stores data in memory only, so it resets when the server restarts.
- It is a design prototype for a school project and is not a production-ready warehouse system.
- The app is intentionally demo-based and does not require external services or database setup.
