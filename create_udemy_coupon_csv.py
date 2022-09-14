import datetime as dt

import coupon_pathlib as cp

COUPEN_LIFESPAN = 30


def get_issue_date(csv_line: str) -> dt:
    line_cells = csv_line.split(",")
    return dt.datetime.strptime(line_cells[3], "%Y-%m-%d")


if __name__ == "__main__":
    with open(cp.origin_coupen_file, "r") as origin_file:
        header: str = origin_file.readline()
        origin_file.__next__()
        origin_coupon_lines: list[str] = origin_file.readlines()
        origin_issue_date: dt = get_issue_date(origin_coupon_lines[0])
        new_issue_times: int = (dt.datetime.today() - origin_issue_date).days // COUPEN_LIFESPAN + 1
        new_issue_date: dt = origin_issue_date + dt.timedelta(days=COUPEN_LIFESPAN * new_issue_times)

    with open(cp.new_coupon_file, "w") as new_file:
        new_file.write(header)
        for line_string in origin_coupon_lines:
            cells = line_string.split(",")
            course_id: str = cells[0]
            new_coupon_code: str = f"{course_id}-{new_issue_times:04}"

            new_file.write(f"{course_id},"
                           f"{cells[1]},"
                           f"{new_coupon_code},"
                           f"{new_issue_date},"
                           f"{cells[4]},"
                           f"{cells[5]}")

    cp.open_new_coupon_dir()
