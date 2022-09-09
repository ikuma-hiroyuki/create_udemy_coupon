import webbrowser
from pathlib import Path

dir_path = Path(__file__).resolve().parent


def open():
    webbrowser.open(f"{dir_path}")
