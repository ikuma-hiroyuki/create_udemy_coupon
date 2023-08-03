import datetime as dt
import hashlib
import uuid

import pytz


def convert_jst_to_pst(jst_time: dt.datetime) -> tuple[str, str]:
    """
    Converts a given datetime object from JST (Japan Standard Time) to PST (Pacific Standard Time).

    :param jst_time: A datetime object representing the time in JST.
    :return: A tuple containing the converted date in PST (YYYY-MM-DD) and the converted time in PST (HH:MM).
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


def create_unique_id():
    """
    20文字のユニークなIDを作成する

    udemyのクーポン要件は6~20文字以内
    :return: unique_code
    """

    uuid_value = uuid.uuid4()
    hash_value = hashlib.sha256(uuid_value.bytes).hexdigest()
    unique_code = hash_value[:20]
    return unique_code


if __name__ == '__main__':
    t = convert_jst_to_pst(dt.datetime.now())
    print(t)
