import os

import requests
from dotenv import load_dotenv

import coupon_pathlib as cp


def get_udemy_links():
    """
    rebrandly に登録してある Udemy のリンクを取得する。

    :return: links = {link_id: {"course_id": course_id, "slashtag": slashtag}}

    https://developers.rebrandly.com/docs/list-links
    """

    api_url = 'https://api.rebrandly.com/v1/links'
    response = requests.get(api_url, headers=headers)

    links = {}
    for link in response.json():
        if 'udemy.com' in link['destination']:
            course_id = link['destination'].split('=')[-1].split('-')[0]
            course_link = link['destination'].split('?')[0]
            links[link['id']] = {
                "course_id": course_id,
                "slashtag": link['slashtag'],
                "course_link": course_link,
            }
    return links


def update_link(link_id, destination):
    """
    rebrandly のUdemyクーポンのリンクを更新する。

    :param link_id: rebrandly のリンクID
    :param destination: 新しく発行したUdemyのクーポンリンク

    https://developers.rebrandly.com/docs/update-a-link
    """

    api_url = f'https://api.rebrandly.com/v1/links/{link_id}'
    payload = {"destination": destination, }
    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == requests.codes.ok:
        print(f"{link_id} updated successfully.")
    else:
        print(f"Error updating {link_id}.")
        print(response.text)


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('REBRANDLY_API')
    headers = {
        "apikey": api_key,
        'Content-Type': 'application/json'
    }
    new_coupons: dict = cp.get_coupon_dict()
    udemy_links: dict = get_udemy_links()

    for rebrandly_link_id, udemy_course_id in udemy_links.items():
        new_coupon = new_coupons[udemy_course_id['course_id']]
        new_destination = f"{udemy_links[rebrandly_link_id]['course_link']}?couponCode={new_coupon}"
        update_link(rebrandly_link_id, new_destination)
