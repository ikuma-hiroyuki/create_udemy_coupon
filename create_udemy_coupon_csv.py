import datetime as dt

import coupon_pathlib as cp

coupen_lifespan = 30

if __name__ == "__main__":
    issue_times: int = int(input("Please enter the number of issues.\n"))
    with open(cp.origin_coupen_file, "r") as origin_file:
        header: str = origin_file.readline()
        origin_file.__next__()
        coupon_lines: list[str] = origin_file.readlines()

    with open(cp.new_coupon_file, "w") as new_file:
        new_file.write(header)
        for line in coupon_lines:
            cells = line.split(",")
            course_id: str = cells[0]
            new_coupon_code: str = f"{course_id}-{issue_times:04}"
            origin_issue_date: dt = dt.datetime.strptime(cells[3], "%Y-%m-%d")
            new_issue_date: dt = origin_issue_date + dt.timedelta(days=coupen_lifespan * issue_times)

            new_file.write(f"{course_id},"
                           f"{cells[1]},"
                           f"{new_coupon_code},"
                           f"{new_issue_date},"
                           f"{cells[4]},"
                           f"{cells[5]}")

    cp.open_new_coupon_dir()
