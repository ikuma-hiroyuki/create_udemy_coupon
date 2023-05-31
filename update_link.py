import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'Authorization': f'Bearer {os.getenv("BITLY_TOKEN")}',
    'Content-Type': 'application/json',
}


def print_links():
    api_url = 'https://api-ssl.bitly.com/v4/groups/'
    response = requests.get(f'{api_url}{os.getenv("GROUP_GUID")}/bitlinks', headers=HEADERS)
    print(json.dumps(response.json(), indent=4))


def update_long_url(bit_id, new_url):
    """
    リンク先のURLを更新する

    URL更新は Starterプラン以上で可能
    :param bit_id: bit.lyのID
    :param new_url: 新しいURL
    :return:
    """
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
    data = {
        'long_url': new_url,
        'title': 'New Title2'
    }
    response = requests.patch(f'{api_url}{bit_id}', headers=HEADERS,
                              data=json.dumps(data))
    print(json.dumps(response.json(), indent=4))


if __name__ == '__main__':
    bitly_id = 'bit.ly/3OI6SC1'  # テスト用
    new_long_url = 'https://www.udemy.com/course/vba4-ux1/?referralCode=3A9D44378B6F82D2F3EF'  # テスト用
    update_long_url(bitly_id, new_long_url)
