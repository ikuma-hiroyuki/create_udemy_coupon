"""
Udemyのクーポン一括作成機能用のクーポンを作成する
https://www.udemy.com/instructor/multiple-coupons-creation/
"""
import argparse
import csv
import datetime

from utils import coupon_pathlib as cp, create_increment_code, create_unique_id, convert_jst_to_pst


def create_udemy_coupon(is_custom_price: bool, start_date: str, start_time: str):
    """
    Udemyのクーポン一括作成機能用のクーポンを作成する

    coupon_typeがcustom_priceの場合は、コースID+連番でクーポンコードを作成する
    :param is_custom_price: custom_priceにするかどうか。Trueの場合はcustom_priceにし、Falseの場合はbest_priceにする
    :param start_date: 開始日(日本時間)
    :param start_time: 開始時刻(日本時間)
    """

    start_date_time = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    jp_start_date, jp_start_time = convert_jst_to_pst(start_date_time)

    # クーポンのタイプによって、クーポンコードを作成する関数を変える
    if is_custom_price:
        coupon_type = "custom_price"
        coupon_func = create_increment_code
    else:
        coupon_type = "best_price"
        coupon_func = create_unique_id

    # 対象になるコースに対して、クーポンコードを作成する
    with cp.courses_file.open("r", encoding="utf-8") as f:
        reader: csv.DictReader = csv.DictReader(f)

        new_coupon_list = []
        for course in reader:
            coupon_code = coupon_func(course["course_id"])

            new_coupon_list.append(
                {
                    "course_id": course["course_id"],
                    "coupon_type": coupon_type,
                    "coupon_code": coupon_code,
                    "start_date": jp_start_date,
                    "start_time": jp_start_time,
                    "custom_price": "min" if is_custom_price else None,
                }
            )

    with cp.new_coupon_file.open("w", encoding="utf-8", newline="") as f2:
        fieldnames = new_coupon_list[0].keys()
        writer = csv.DictWriter(f2, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_coupon_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Udemyのクーポン一括作成機能用のクーポンを作成する")
    parser.add_argument('price_type', type=str, help='best or custom')
    parser.add_argument('start_date', type=str, help='YYYY-MM-DD')
    parser.add_argument('start_time', type=str, help='HH:MM')
    parser.add_argument("-i", "--is_custom_price", action="store_true", help="custom_priceのクーポンを作成するかどうか")
    args = parser.parse_args()

    create_udemy_coupon(args.is_custom_price, args.start_date, args.start_time)
