import webbrowser
from pathlib import Path

dir_path = Path(__file__).resolve().parent


def open_csv_dir():
    webbrowser.open(f"{dir_path}")
