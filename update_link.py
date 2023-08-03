import argparse
import os

import requests
from dotenv import load_dotenv

import utils.coupon_pathlib as cp

load_dotenv()
api_key = os.getenv('REBRANDLY_API')
headers = {
    "apikey": api_key,
    'Content-Type': 'application/json'
}


def get_redirect_links() -> list:
    """
    rebrandly に登録してあるリダイレクトリンクを取得する。
    :return: リダイレクトリンク一覧
    """
    api_url = 'https://api.rebrandly.com/v1/links'
    response = requests.get(api_url, headers=headers)
    return response.json()


def get_udemy_links(target_title) -> dict:
    """
    Udemyのクーポン一括作成機能用のリダイレクトリンクを整形して返す。

    :return: Udemyのクーポン一括作成機能用のリダイレクトリンク辞書

    https://developers.rebrandly.com/docs/list-links
    """

    redirects = get_redirect_links()

    links = {
        link['id']: {
            "course_id": link['destination'].split('=')[-1].split('-')[0],
            "slashtag": link['slashtag'],
            "course_link": link['destination'].split('?')[0],
            "title": link['title'],
        }
        for link in redirects if target_title == link['title']
    }

    return links


def update_redirect_links(target_title):
    """
    rebrandly のUdemyクーポンのリンクを更新する。

    https://developers.rebrandly.com/docs/update-a-link
    """

    new_coupons: dict = cp.get_coupon_dict()
    udemy_links: dict = get_udemy_links(target_title)

    for rebrandly_link_id, udemy_course_id in udemy_links.items():
        new_coupon = new_coupons[udemy_course_id['course_id']]
        new_destination = f"{udemy_links[rebrandly_link_id]['course_link']}?couponCode={new_coupon}"

        api_url = f'https://api.rebrandly.com/v1/links/{rebrandly_link_id}'
        payload = {"destination": new_destination, "title": target_title}
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == requests.codes.ok:
            print(f"{udemy_links[rebrandly_link_id]['slashtag']} updated successfully.")
        else:
            print(f"Error updating {rebrandly_link_id}.")
            print(response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("リダイレクトリンク先のURLを更新する。位置引数として best か custom を指定する。")
    parser.add_argument('price_type', type=str, help='best or custom')

    args = parser.parse_args()

    target_title = ""
    if args.price_type.lower() == "best":
        target_title = "UdemyBestPrice"
    elif args.price_type.lower() == "custom":
        target_title = "UdemyCustomPrice"

    update_redirect_links(target_title)
