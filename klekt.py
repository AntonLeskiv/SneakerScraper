import requests
import json
import fake_useragent
from bs4 import BeautifulSoup as bs


def us_to_eu(size_set, us_size):
    for size_mapping in size_set:
        if size_mapping['US'] == us_size:
            return size_mapping['EU']
    return None


def get_size_set(data):
    set = data["props"]["pageProps"]["productDetailsExtended"]["sizeSet"]["Attributes"]

    sizes_to_keep = ["US", "EU"]

    size_set = [
        {key: value for key, value in atributo.items() if key in sizes_to_keep} for atributo in set
    ]

    return size_set


def get_product_url(sku):
    base_url = "https://www.klekt.com/brands"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.5",
        "Dnt": "1",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": agent
    }

    params = {
        "search": f"{sku}"
    }

    response = session.get(base_url, params=params, headers=headers)

    soup = bs(response.text, "html.parser")
    data = json.loads(soup.find('script', {"id": "__NEXT_DATA__"}).text)

    # klekt_id = data["props"]["pageProps"]["plpData"]["data"]["search"]["items"][0]["productId"]
    slug = data["props"]["pageProps"]["plpData"]["data"]["search"]["items"][0]["slug"]
    shoe_url = f"https://www.klekt.com/product/{slug}"

    return shoe_url


def get_klekt_json(sku):
    shoe_url = get_product_url(sku)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.5",
        "Cache-Control": "max-age=0",
        "Dnt": "1",
        "If-None-Match": 'W/"11wvlqk5cf0az2"',
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": agent
    }

    response = session.get(shoe_url, headers=headers)

    soup = bs(response.text, "html.parser")
    data = json.loads(soup.find('script', {"id": "__NEXT_DATA__"}).text)

    sizes = data["props"]["pageProps"]["productDetailsExtended"]["variants"]
    size_set = get_size_set(data)
    shoe_name = data["props"]["pageProps"]["productDetailsExtended"]["name"]
    shoe_image = data["props"]["pageProps"]["productDetailsExtended"]["featuredAsset"]["preview"]

    klekt_json = {
        "site": "Klekt",
        "name": f"{shoe_name}",
        "image": f"{shoe_image}",
        "sizes": {

        }
    }

    for size in sizes:
        klekt_json["sizes"][size["facetValues"][0]["name"]] = {
            "buy_price": str(round(size["priceWithTax"] / 100)),
            "payout_price": str(round((size["priceWithTax"] / 100 * 0.855) - 5))
        }

    try:
        converted_sizes = {}
        for us_size, values in klekt_json['sizes'].items():
            eu_size = us_to_eu(size_set, us_size)
            if eu_size:
                converted_sizes[eu_size] = values

        sorted_sizes = dict(
            sorted(converted_sizes.items(), key=lambda x: float(x[0])))
        klekt_json["sizes"] = sorted_sizes

    except:
        pass

    return json.dumps(klekt_json, indent=4)

ua = fake_useragent.UserAgent()
agent = ua.random
session = requests.Session()
