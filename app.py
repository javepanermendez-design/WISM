"""Compatibility entrypoint; use run.py for the WIMS application."""
from run import app


if __name__ == "__main__":
    app.run(debug=True)
