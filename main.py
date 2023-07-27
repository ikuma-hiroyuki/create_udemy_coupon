import csv
import datetime as dt

import coupon_pathlib as cp

COUPON_LIFESPAN = 30
ORIGIN_ISSUE_DATE = dt.datetime(2022, 9, 7)  # 一番最初にクーポンを発行した日付

with cp.courses_file.open("r", encoding="utf-8") as f:
    reader: csv.DictReader = csv.DictReader(f)
    next_issue_times = (dt.datetime.today() - ORIGIN_ISSUE_DATE).days // COUPON_LIFESPAN + 1
    start_date = (ORIGIN_ISSUE_DATE + dt.timedelta(days=COUPON_LIFESPAN * next_issue_times)).strftime("%Y-%m-%d")

    new_coupon_list = []
    for course in reader:
        new_coupon_list.append(
            {
                "course_id": course["course_id"],
                "coupon_type": "custom_price",
                "coupon_code": f"{course['course_id']}-{next_issue_times:04}",
                "start_date": start_date,
                "start_time": "0:00",
                "custom_price": "min"
            }
        )

with cp.new_coupon_file.open("w", encoding="utf-8", newline="") as f2:
    fieldnames = new_coupon_list[0].keys()
    writer = csv.DictWriter(f2, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_coupon_list)

cp.open_new_coupon_dir()
