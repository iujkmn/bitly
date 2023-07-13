import requests
import argparse
from urllib.parse import urlparse
import os
from dotenv import load_dotenv


def shorten_link(token, link):
    headers = {"Authorization": f"Bearer {token}"}
    url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {"long_url": link}
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, link):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary",
        headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(link, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{link}",
                            headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(
        description='Создаёт битлинк,считает количесто нажатий на битлинк'
    )
    parser.add_argument('url', help='Ваша ссылка')
    args = parser.parse_args()
    load_dotenv()
    token = os.environ["BITLY_TOKEN"]
    link = args.url
    parsed_link = urlparse(link)
    shared_link = f"{parsed_link.netloc}{parsed_link.path}"
    try:
        if is_bitlink(shared_link, token):
            print(count_clicks(token, shared_link))
        else:
            print(shorten_link(token, link))
    except requests.exceptions.HTTPError:
        print("Ошибка")


if __name__ == "__main__":
    main()
