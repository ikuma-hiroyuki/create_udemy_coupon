import pandas
import datetime
import pandas as pd
import random
import string

coupen_file = "coupen_code.csv"
past_codes_file = "past_codes.csv"

coupen_code_len = 10
letters = string.ascii_uppercase + string.digits + '.' + '_' + '-'


def create_random_code(length: int) -> str:
    randdom_letters = ''.join(random.choices(letters, k=length))
    with open(past_codes_file, "r") as read_file:
        past_codes_list = [past_code.replace("\n", "") for past_code in read_file.readlines()]

    while randdom_letters in past_codes_list:
        randdom_letters = ''.join(random.choices(letters, k=length))

    with open(past_codes_file, "a") as file:
        file.writelines(f"{randdom_letters}\n")

    return randdom_letters


coupon_list = pd.read_csv(coupen_file)
with open(coupen_file, "w") as new_file:
    new_file.write(",".join(coupon_list.columns.values) + "\n")
    for course in coupon_list.values:
        issuing_date = datetime.datetime.strptime(course[3], "%Y-%m-%d") + datetime.timedelta(days=30)
        new_file.write(f"{course[0]},"
                       f"{course[1]},"
                       f"{create_random_code(coupen_code_len)},"
                       f"{issuing_date},"
                       f"{course[4]},"
                       f"{course[5]}" + "\n")
