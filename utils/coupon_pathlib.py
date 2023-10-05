import csv
import platform
import subprocess
from pathlib import Path

base_path = Path(__file__).resolve().parent
resources_dir = Path(__file__).resolve().parent.parent / "resources"

origin_coupon_file = base_path / "udemy_coupon_code.csv"
courses_file = resources_dir / "courses.csv"
new_coupon_dir = base_path.parent / "coupon_file"
new_coupon_file = new_coupon_dir / "coupon_code.csv"


def open_new_coupon_dir():
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", f"{new_coupon_dir}"])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", f"{new_coupon_dir}"])


def get_coupon_dict():
    """
    発行したクーポンコードを取得する。

    :return: coupon_dict = {course_id: coupon_code}
    """

    coupon_dict = {}
    with new_coupon_file.open("r", encoding="utf-8") as f:
        reader: csv.DictReader = csv.DictReader(f)
        for row in reader:
            coupon_dict[row["course_id"]] = row["coupon_code"]
    return coupon_dict


if __name__ == '__main__':
    print(courses_file)
