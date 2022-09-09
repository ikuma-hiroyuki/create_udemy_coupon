import platform
import subprocess
from pathlib import Path

dir_path = Path(__file__).resolve().parent


def open_dir():
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", f"{dir_path}"])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", f"{dir_path}"])
