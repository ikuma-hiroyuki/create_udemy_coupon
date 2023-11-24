"""
Udemyのクーポン一括作成機能用のクーポンを作成する
https://www.udemy.com/instructor/multiple-coupons-creation/
"""

import argparse
import csv
import datetime

from update_link import update_redirect_links
from utils import (
    coupon_pathlib as cp,
    create_increment_code,
    create_unique_id,
    convert_jst_to_pst,
    update_promotion_template_and_copy_to_clipboard
)


def add_arguments():
    parser = argparse.ArgumentParser("Udemyのクーポン一括作成機能用のクーポンを作成する")
    parser.add_argument("-c", "--is_custom_price", action="store_true", help="custom_priceのクーポンを作成するかどうか")
    parser.add_argument('-d', '--start_date', type=str, help='YYYY-MM-DD (日本時間。省略すると当日)')
    parser.add_argument('-t', '--start_time', type=str, help='HH:MM (日本時間。省略すると現在時刻)')
    return parser.parse_args()


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

    print(f"クーポンコードを作成しました。{cp.new_coupon_file} を確認してください。")


if __name__ == '__main__':
    args = add_arguments()

    if args.is_custom_price:
        price_type = "Custom price"
    else:
        price_type = "Best price"

    if args.start_date is None:
        args.start_date = datetime.date.today().strftime("%Y-%m-%d")
    if args.start_time is None:
        args.start_time = datetime.datetime.now().strftime("%H:%M")

    is_create = input(f"{price_type} でクーポンを作成しますか？(y/n): ")
    if is_create == "y":
        create_udemy_coupon(args.is_custom_price, args.start_date, args.start_time)
        if not args.is_custom_price:
            update_promotion_template_and_copy_to_clipboard()

        if args.is_custom_price:
            is_update = input("リダイレクトリンク先のURLを更新しますか？(y/n): ")
            if is_update == "y":
                update_redirect_links(is_best_price=False)
