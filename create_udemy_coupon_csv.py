import datetime
import re

import open_dir

origin_coupen_file = "csv_files/udemy_coupon_code.csv"
coupen_file = "coupon_code.csv"
coupen_lifespan = 30

if __name__ == "__main__":
    issue_times: int = int(input("Please enter the number of issues.\n"))
    with open(origin_coupen_file, "r") as origin_file:
        header: str = origin_file.readline()
        origin_file.__next__()
        coupon_lines = origin_file.readlines()

        with open(coupen_file, "w") as new_file:
            new_file.write(header)
            for line in coupon_lines:
                cells = line.split(",")
                issuing_date: datetime = \
                    datetime.datetime.strptime(cells[3], "%Y-%m-%d") \
                    + datetime.timedelta(days=coupen_lifespan * issue_times)
                past_code: str = cells[2]
                new_issue_times: int = int(re.search(r"\d{4}$", past_code).group()) + issue_times
                course_id: str = cells[0]
                new_code: str = f"{course_id}-{new_issue_times:04}"

                new_file.write(f"{course_id},"
                               f"{cells[1]},"
                               f"{new_code},"
                               f"{issuing_date},"
                               f"{cells[4]},"
                               f"{cells[5]}")

        open_dir.open_csv_dir()
