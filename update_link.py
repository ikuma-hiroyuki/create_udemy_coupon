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

    def get_course_id(link):
        return link['destination'].split('=')[-1].split('-')[0]

    def get_course_url(link):
        return link['destination'].split('?')[0]

    redirects = get_redirect_links()

    links = {
        link['id']: {
            "course_id": get_course_id(link),
            "slashtag": link['slashtag'],
            "course_link": get_course_url(link),
            "title": link['title'],
        }
        for link in redirects if target_title == link['title']
    }

    return links


def update_redirect_links(is_custom_price: bool):
    """
    rebrandly のUdemyクーポンのリンクを更新する。

    https://developers.rebrandly.com/docs/update-a-link
    """

    if is_custom_price:
        target_title = "UdemyCustomPrice"
    else:
        target_title = "UdemyBestPrice"

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
            print(f"Error updating {rebrandly_link_id}.\n{response.status_code} - {response.text}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("リダイレクトリンク先のURLを更新する。位置引数として best か custom を指定する。"
                                     "それぞれのタイプで rebrandly の 該当する link title のリダイレクトリンクを更新する。")
    parser.add_argument("-b", "--is_best_price", action="store_true", help="best_priceのクーポンを更新するかどうか")
    args = parser.parse_args()

    if args.is_best_price:
        price_type = "Best price"
    else:
        price_type = "Custom price"

    is_create = input(f"{price_type} でクーポンを更新しますか？(y/n): ")
    if is_create.lower() == "y":
        update_redirect_links(args.is_best_price)
