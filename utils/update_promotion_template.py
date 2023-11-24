import csv
from pathlib import Path

import pyperclip


def update_promotion_template_and_copy_to_clipboard():
    """
    プロモーション用のメールテンプレートを更新し、クリップボードにコピーする
    """

    resources = Path(__file__).parent.parent / "resources"
    coupons_csv = Path(__file__).parent.parent / "coupon_file" / "coupon_code.csv"
    courses_csv = resources / "courses.csv"
    template_txt = resources / "mail_template.txt"

    coupon_dict = {}
    with courses_csv.open(mode="r", encoding="utf-8") as courses, coupons_csv.open(mode="r",
                                                                                   encoding="utf-8") as coupons:
        csv_reader: csv.DictReader = csv.DictReader(courses)
        coupon_reader: csv.DictReader = csv.DictReader(coupons)
        for row in zip(csv_reader, coupon_reader):
            coupon_dict[f'{row[0]["course_id"]}-name'] = row[0]["course_name"]
            coupon_dict[f'{row[0]["course_id"]}-code'] = row[1]["coupon_code"]

    with template_txt.open(mode="r", encoding="utf-8") as template:
        mail_template = template.read()

    mail = mail_template.format(**coupon_dict)
    pyperclip.copy(mail)
    print(mail)
    print("\nメールテンプレートを更新し、クリップボードにコピーしました。")
    print("VSCodeでMarkDownファイルを作成、貼り付けてプレビューをコピペして利用してください。")


if __name__ == "__main__":
    update_promotion_template_and_copy_to_clipboard()
