import json
import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
from log import Log

logged = False


def get_sneakit_url(session, sku):
    base_url = "https://sneakit.com/es/shop"

    headers = {
        "authority": "sneakit.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.5",
        "Dnt": "1",
        "Referer": "https://sneakit.com/es",
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

    params = {
        "search": f"{sku}"
    }

    response = session.get(base_url, params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    data = json.loads(soup.find_all(
        'script', type='application/ld+json')[2].text)
    shoe_url = data["itemListElement"][0]["item"]["url"]

    return shoe_url


def get_sneakit_id(session, sku):
    headers = {
        "User-Agent": agent
    }

    response = session.get(
        f"https://sell.sneakit.com/search/products/{sku}", headers=headers)
    data = json.loads(response.text)
    sneakit_id = data["data"][0]["id"]
    return sneakit_id


def sneakit_login(session, sku, sneakit_email, sneakit_password):
    Log.PrintWarning("Sneakit", "Logging into Sneakit account...")

    headers = {
        "authority": "sell.sneakit.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cache-Control": "max-age=0",
        "Dnt": "1",
        "Referer": "https://sell.sneakit.com/edit",
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

    response = session.get("https://sell.sneakit.com/login", headers=headers)
    sneakit_token = (bs(response.text, "html.parser")).find_all(
        "meta", {"name": "csrf-token"})[0]["content"]

    headers = {
        "authority": "sell.sneakit.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cache-Control": "max-age=0",
        "Content-Length": "99",
        "Content-Type": "application/x-www-form-urlencoded",
        "Dnt": "1",
        "Origin": "https://sell.sneakit.com",
        "Referer": "https://sell.sneakit.com/login",
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

    payload = {
        "_token": f"{sneakit_token}",
        "email": f"{sneakit_email}",
        "password": f"{sneakit_password}"
    }

    response = session.post(
        "https://sell.sneakit.com/login", data=payload, headers=headers)

    if "Logout" in response.text:
        Log.PrintSuccess("Sneakit", "Sneakit Login was successful")
        global logged
        logged = True
        return logged

    else:
        Log.PrintError("Sneakit", "Sneakit Login was unsuccessful")
        Log.PrintError("Sneakit", "Check your credentials")
        return logged


def check_session():
    global logged
    if logged:
        return logged
    else:
        logged = False
        return logged


def get_sneakit_json(sku, sneakit_email, sneakit_password):

    global logged
    logged = check_session()

    while not logged:
        logged = sneakit_login(session, sku, sneakit_email, sneakit_password)

    shoe_url = get_sneakit_url(session, sku)

    headers = {
        "authority": "sneakit.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.5",
        "Dnt": "1",
        "Referer": "https://sneakit.com/es/shop?search=DD1391-100",
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

    response = session.get(shoe_url, headers=headers)
    soup = bs(response.text, 'html.parser')
    data = json.loads(soup.find_all(
        'script', type='application/ld+json')[2].text)

    sneakit_id = get_sneakit_id(session, sku)

    response2 = session.get(
        f"https://sell.sneakit.com/search/product-with-history/{sneakit_id}", headers=headers)
    data2 = json.loads(response2.text)

    all_sizes = data["offers"]["offers"]
    all_sizes2 = data2["sizesPrices"]

    shoe_name = data["name"]
    shoe_image = data["image"]

    sneakit_dict = {
        "site": "Sneakit",
        "name": f"{shoe_name}",
        "image": f"{shoe_image}",
        "sizes": {

        }
    }

    for i in range(len(all_sizes2)):
        size = all_sizes[i]["description"].replace("Talla: ", "").replace(
            " ½", ".5").replace(".66", " ⅔").replace(".33", " ⅓").strip()
        try:
            buy_price = int(all_sizes[i]["price"])
            payout_price = int(all_sizes2[i]["price"])
        except:
            buy_price, payout_price = "OOS", "OOS"

        sneakit_dict["sizes"][f"{size}"] = {
            "buy_price": f"{buy_price}",
            "payout_price": f"{payout_price}"
        }

    return json.dumps(sneakit_dict, indent=4)

ua = fake_useragent.UserAgent()
agent = ua.random
session = requests.Session()
