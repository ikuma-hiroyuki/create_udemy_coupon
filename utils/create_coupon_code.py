"""
https://www.udemy.com/instructor/multiple-coupons-creation/
クーポンコードは6文字以上、20字以内でなければなりません。
使用できる文字と記号は、英数字（A-Z、0-9）、ピリオド（「.」）、ダッシュ（「-」）、アンダースコア（「_」）のみです。
"""

import datetime as dt
import hashlib
import uuid

import pytz


def convert_jst_to_pst(jst_time: dt.datetime) -> tuple[str, str]:
    """
    指定された日時を JST (日本標準時) から PST (太平洋標準時) に変換する

    :param jst_time: JST の時刻を表す datetime オブジェクト
    :return: PST (YYYY-MM-DD) に変換された日付と PST (HH:MM) に変換された時刻のタプル
    """

    pst = pytz.timezone('America/Los_Angeles')
    us_time = jst_time.astimezone(pst)
    us_date = us_time.strftime('%Y-%m-%d')
    us_time = us_time.strftime('%H:%M')
    return us_date, us_time


def create_increment_code(course_id: str) -> str:
    """
    連番になっているクーポンコードを作成する
    :return: 連番になっているクーポンコード
    """

    coupon_lifespan = 30
    origin_issue_date = dt.datetime(2022, 9, 7)  # 一番最初にクーポンを発行した日付
    next_issue_times = (dt.datetime.today() - origin_issue_date).days // coupon_lifespan + 1
    return f"{course_id}-{next_issue_times:04}"


def create_unique_id(course_id: str):
    """
    ユニークなIDを作成する

    Udemyのクーポン要件は6~20文字以内。コースIDは7文字。クーポンはコースID + -(ハイフン) + IDの形式で作成する。
    コースIDを含めるのはリダイレクトリンクURLがコースIDを含んでいるため。
    :return: unique_code
    """

    uuid_value = uuid.uuid4()
    hash_value = hashlib.sha256(uuid_value.bytes).hexdigest()
    unique_code = hash_value[:12].upper()
    return f"{course_id}-{unique_code}"[:20]
