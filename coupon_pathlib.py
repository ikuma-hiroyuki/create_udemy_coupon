import platform
import subprocess
from pathlib import Path

base_path = Path(__file__).resolve().parent
origin_coupen_file = base_path / "base_files/udemy_coupon_code.csv"
new_coupon_dir = base_path / "coupon_file"
new_coupon_file = new_coupon_dir / "coupon_code.csv"


def open_new_coupon_dir():
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", f"{new_coupon_dir}"])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", f"{new_coupon_dir}"])
