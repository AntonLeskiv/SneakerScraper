import json
import requests
import fake_useragent
from bs4 import BeautifulSoup as bs


def get_hypeboost_url(sku):
    headers = {
        'authority': 'hypeboost.com',
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Dnt': '1',
        'Referer': 'https://hypeboost.com/es',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Gpc': '1',
        'User-Agent': agent,
        'X-Requested-With': 'XMLHttpRequest'
    }

    params = {
        'keyword': f'{sku}'
    }

    response = session.get(
        "https://hypeboost.com/es/search/shop", params=params, headers=headers)
    shoe_url = (bs(response.text, "html.parser")).find("a")["href"]

    return shoe_url


def get_hypeboost_json(sku):
    shoe_url = get_hypeboost_url(sku)

    headers = {
        'authority': 'hypeboost.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Dnt': '1',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-Gpc': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': agent
    }

    response = session.get(shoe_url, headers=headers)
    soup = bs(response.text, "html.parser")
    all_sizes = soup.find_all("div", class_="size")

    shoe_name = soup.find("h1").text.strip()
    shoe_image = soup.find('div', {"class": "item"}).find("img")["src"]

    hypeboost_dict = {
        "site": "Hypeboost",
        "name": f"{shoe_name}",
        "image": f"{shoe_image}",
        "sizes": {

        }
    }
    for size_div in all_sizes:
        size = size_div.find("div", class_="label").text.replace(" ½", ".5")
        try:
            buy_price = int(size_div.find("span", class_="").text.replace(
                ".", "").replace(" €", ""))
            payout_price = round((buy_price * 0.915 - 15), 2)
        except:
            buy_price, payout_price = "OOS", "OOS"

        hypeboost_dict["sizes"][f"{size}"] = {
            "buy_price": f"{buy_price}",
            "payout_price": f"{payout_price}"
        }

    return json.dumps(hypeboost_dict, indent=4)

ua = fake_useragent.UserAgent()
agent = ua.random
session = requests.Session()
