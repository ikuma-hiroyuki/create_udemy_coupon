import platform
import subprocess
from pathlib import Path

base_path = Path(__file__).resolve().parent
origin_coupon_file = base_path / "udemy_coupon_code.csv"
courses_file = base_path / "courses.csv"
new_coupon_dir = base_path / "coupon_file"
new_coupon_file = new_coupon_dir / "coupon_code.csv"


def open_new_coupon_dir():
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", f"{new_coupon_dir}"])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", f"{new_coupon_dir}"])
