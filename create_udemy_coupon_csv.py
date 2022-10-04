import csv
import datetime as dt

import coupon_pathlib as cp

COUPEN_LIFESPAN = 30


def get_new_items(start_date: dt) -> (str, str):
    origin_issue_date: dt = dt.datetime.strptime(start_date, "%Y-%m-%d")
    next_issue_times: int = (dt.datetime.today() - origin_issue_date).days // COUPEN_LIFESPAN + 1
    next_issue_date: dt = origin_issue_date + dt.timedelta(days=COUPEN_LIFESPAN * next_issue_times)
    return f"{row['course_id']}-{next_issue_times:04}", next_issue_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    with open(cp.origin_coupen_file, "r", encoding="utf-8", newline="") as origin_file:
        reader = csv.DictReader(origin_file)

        with open(cp.new_coupon_file, "w", encoding="utf-8", newline="") as new_file:
            writer = csv.DictWriter(new_file, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                new_coupon_code, new_issue_date = get_new_items(row["start_date"])
                row["start_date"] = new_issue_date
                row["coupon_code"] = new_coupon_code
                writer.writerow(row)

    cp.open_new_coupon_dir()
