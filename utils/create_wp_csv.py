"""Wordpressでリダイレクト先を更新するためのCSVを作成する"""

import csv
import os
import re

from dotenv import load_dotenv

import coupon_pathlib as cp

load_dotenv()

domain = os.getenv("DOMAIN")


def create_wp_csv():
    """Wordpressでリダイレクト先を更新するためのCSVを作成する

    mail_template.txtからコースIDとUdemyのURLの対応を取得し、
    coupon_code.csvのクーポンコードと組み合わせてredirect.csvを作成する
    """

    # mail_template.txtからコースIDとUdemyのURLの対応を取得
    mail_template_path = cp.resources_dir / "mail_template.txt"
    course_url_mapping = {}

    with open(mail_template_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # {course_id-code}とUdemyのURLのパターンを検索
        # パターン: https://www.udemy.com/course/コース名/?couponCode={course_id-code}
        pattern = r'https://www\.udemy\.com/course/([^?]+)/\?couponCode=\{(\d+)-code\}'
        matches = re.findall(pattern, content)

        for course_name, course_id in matches:
            course_url_mapping[course_id] = f"https://www.udemy.com/course/{course_name}/"

    # coupon_code.csvからクーポンコードを取得
    coupon_dict = cp.get_coupon_dict()

    # redirect.csvを作成
    redirect_csv_path = cp.new_coupon_dir / "redirect.csv"

    with open(redirect_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        for course_id, coupon_code in coupon_dict.items():
            if course_id in course_url_mapping:
                source = f"https://{domain}/course-{course_id}/"
                udemy_url = course_url_mapping[course_id]
                url = f"{udemy_url}?couponCode={coupon_code}"

                writer.writerow([source, url, "url", "redirect"])

    upload_url = "wp-admin/tools.php?page=redirection.php&sub=io"
    print(
        f"redirect.csvを作成しました。{redirect_csv_path} を https://{domain}/{upload_url} にアップロードしてください。")


if __name__ == '__main__':
    create_wp_csv()
