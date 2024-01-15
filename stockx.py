import requests
import json
import fake_useragent
from bs4 import BeautifulSoup as bs
from log import Log

STOCKX_FEE = 0.91


def get_shoe_url(sku):
    base_url = f"https://stockx.com/es-es/search"

    params = {
        "s":  f"+{sku}",
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8',
        'Dnt': '1',
        'Referer': 'https://stockx.com/es-es',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Gpc': '1',
        'User-Agent': agent
    }

    response = session.get(base_url, params=params, headers=headers)
    soup = bs(response.text, "html.parser")

    data = json.loads(soup.find('script', {"id": "__NEXT_DATA__"}).text)

    data2 = data["props"]["pageProps"]["req"]["appContext"]["states"]["query"][
        "value"]["queries"][4]["state"]["data"]["browse"]["results"]["edges"][0]["node"]
    shoe_name = data2["name"]
    shoe_url = data2["urlKey"]
    shoe_image = data2["media"]["thumbUrl"]

    return shoe_name, shoe_url, shoe_image


def get_stockx_json(sku):
    shoe_name, shoe_url, shoe_image = get_shoe_url(sku)

    base_url = f"https://stockx.com/es-es/{shoe_url}"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8",
        "Cache-Control": "max-age=0",
        "Dnt": "1",
        "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Brave\";v=\"120\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": agent
    }

    response = session.get(base_url, headers=headers)

    soup = bs(response.text, "html.parser")
    data = json.loads(soup.find('script', {"id": "__NEXT_DATA__"}).text)

    variants = data["props"]["pageProps"]["req"]["appContext"]["states"][
        "query"]["value"]["queries"][2]["state"]["data"]["product"]["variants"]

    stockx_json = {
        "site": "StockX",
        "name": f"{shoe_name}",
        "image": f"{shoe_image}",
        "sizes": {

        }
    }

    for variant in variants:
        try:
            lowest_ask_amount = variant["market"]["state"]["lowestAsk"]
            if lowest_ask_amount is None:
                stockx_json["sizes"][variant["sizeChart"]["baseSize"].replace(variant["sizeChart"]["baseSize"], variant["sizeChart"]["displayOptions"][4]["size"]).replace("EU ", "")] = {
                    "buy_price": "OOS",
                    "payout_price": str(round(variant["market"]["state"]["highestBid"]["amount"] * STOCKX_FEE * 0.97 - 8, 2))
                }
            else:
                stockx_json["sizes"][variant["sizeChart"]["baseSize"].replace(variant["sizeChart"]["baseSize"], variant["sizeChart"]["displayOptions"][4]["size"]).replace("EU ", "")] = {
                    "buy_price": str(lowest_ask_amount["amount"]),
                    "payout_price": str(round(variant["market"]["state"]["highestBid"]["amount"] * STOCKX_FEE * 0.97 - 8, 2))
                }
        except:
            stockx_json["sizes"][variant["sizeChart"]["baseSize"].replace(variant["sizeChart"]["baseSize"], variant["sizeChart"]["displayOptions"][4]["size"]).replace("EU ", "")] = {
                "buy_price": "OOS",
                "payout_price": "OOS"
            }

    return json.dumps(stockx_json, indent=4)

ua = fake_useragent.UserAgent()
agent = ua.random
session = requests.Session()
