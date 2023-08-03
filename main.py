"""
Udemyのクーポン一括作成機能用のクーポンを作成する
https://www.udemy.com/instructor/multiple-coupons-creation/
"""

import csv
import datetime

from utils import coupon_pathlib as cp, create_increment_code, create_unique_id, convert_jst_to_pst


def create_udemy_coupon(coupon_type: str, start_date: str, start_time: str):
    """
    Udemyのクーポン一括作成機能用のクーポンを作成する

    coupon_typeがcustom_priceの場合は、コースID+連番でクーポンコードを作成する
    :param coupon_type:
    :param start_date:
    :param start_time:
    :return:
    """

    # クーポンのタイプによって、クーポンコードを作成する関数を変える
    coupon_func = None
    is_custom_price = coupon_type == "custom_price"
    if is_custom_price:
        coupon_func = create_increment_code
    else:
        coupon_func = create_unique_id

    # 対象になるコースに対して、クーポンコードを作成する
    with cp.courses_file.open("r", encoding="utf-8") as f:
        reader: csv.DictReader = csv.DictReader(f)

        new_coupon_list = []
        for course in reader:
            if is_custom_price:
                coupon_code = coupon_func(course["course_id"])
            else:
                coupon_code = coupon_func()

            new_coupon_list.append(
                {
                    "course_id": course["course_id"],
                    "coupon_type": coupon_type,
                    "coupon_code": coupon_code,
                    "start_date": start_date,
                    "start_time": start_time,
                    "custom_price": "min" if is_custom_price else None,
                }
            )

    with cp.new_coupon_file.open("w", encoding="utf-8", newline="") as f2:
        fieldnames = new_coupon_list[0].keys()
        writer = csv.DictWriter(f2, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_coupon_list)

    cp.open_new_coupon_dir()


jp_start_date, jp_start_time = convert_jst_to_pst(datetime.datetime.now())
create_udemy_coupon("best_price", jp_start_date, jp_start_time)
