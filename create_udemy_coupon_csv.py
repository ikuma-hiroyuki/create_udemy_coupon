import datetime
import re

import pandas as pd

import open_dir

origin_coupen_file = "csv_files/udemy_coupon_code.csv"
coupen_file = "coupon_code.csv"
coupen_lifespan = 30

if __name__ == "__main__":
    issue_times: int = int(input("Please enter the number of issues.\n"))
    coupon_list = pd.read_csv(origin_coupen_file)
    with open(coupen_file, "w") as new_file:
        new_file.write(",".join(coupon_list.columns.values) + "\n")
        for course in coupon_list.values:
            issuing_date: datetime = datetime.datetime.strptime(course[3], "%Y-%m-%d") \
                                     + datetime.timedelta(days=coupen_lifespan * issue_times)
            past_code: str = course[2]
            new_issue_times: int = int(re.search(r"\d{4}$", past_code).group()) + issue_times
            course_id: str = course[0]
            new_code: str = f"{course_id}-{new_issue_times:04}"

            new_file.write(f"{course_id},"
                           f"{course[1]},"
                           f"{new_code},"
                           f"{issuing_date},"
                           f"{course[4]},"
                           f"{course[5]}" + "\n")

    open_dir.open_csv_dir()
