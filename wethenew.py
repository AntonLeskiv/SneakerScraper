import requests
import json
import fake_useragent
from pypasser import reCaptchaV3
from log import Log

success = False


def get_wethenew_id(sku, wethenew_token):
    base_url = "https://api-sell.wethenew.com/products"

    params = {
        "keywordSearch": f"{sku}",
        "take": '50'
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-ES,es;q=0.5",
        "Authorization": f"Bearer {wethenew_token}",
        "Dnt": "1",
        "Origin": "https://sell.wethenew.com",
        "Pragma": "no-cache",
        "Referer": "https://sell.wethenew.com/",
        "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Brave\";v=\"120\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Gpc": "1",
        "User-Agent": agent,
        "X-Xss-Protection": "1;mode=block"
    }

    response = session.get(base_url, params=params, headers=headers)
    data = response.json()
    shoe_id = data["results"][0]["id"]

    return shoe_id


def login(wethenew_token):
    try:
        headers = {
            'authority': 'api-sell.wethenew.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-ES,es;q=0.9',
            'authorization': f'Bearer {wethenew_token}',
            'dnt': '1',
            'origin': 'https://sell.wethenew.com',
            'pragma': 'no-cache',
            'referer': 'https://sell.wethenew.com/',
            'sec-ch-ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            "User-Agent": agent,
            'x-xss-protection': '1;mode=block',
        }

        response = session.get(
            'https://api-sell.wethenew.com/sellers/me', headers=headers)

        data = response.json()
        name = data['firstname']
        Log.PrintSuccess("WeTheNew", f"Login Successful {name}!")
        success = True

    except Exception:
        Log.PrintError("WeTheNew", "Login Unsuccessful")
        success = False

    return success


def pypasser_recaptcha_v3():
    try:
        recaptcha_response = reCaptchaV3(
            "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LeJBSAdAAAAACyoWxmCY7q5G-_6GnKBdpF4raee&co=aHR0cHM6Ly9zZWxsLndldGhlbmV3LmNvbTo0NDM.&hl=en&v=vpEprwpCoBMgy-fvZET0Mz6L&size=invisible&cb=oirqcocfxlm4")
        Log.PrintSuccess("Captcha", "Successfully passed captcha")
        return recaptcha_response

    except Exception as e:
        Log.PrintError("Pypasser", f"Error: {e}")


def get_wtn_token(wethenew_email, wethenew_password):

    try:
        recaptcha_token = pypasser_recaptcha_v3()

        response = session.get('https://sell.wethenew.com/api/auth/csrf')
        data = response.json()
        csrfToken = data['csrfToken']

        # time.sleep(0.5)
        data = {
            'redirect': 'false',
            'email': wethenew_email,
            'password': wethenew_password,
            'recaptchaToken': recaptcha_token,
            'pushToken': 'undefined',
            'os': 'undefined',
            'osVersion': 'undefined',
            'csrfToken': f'{csrfToken}',
            'callbackUrl': 'https://sell.wethenew.com/login',
            'json': 'true'
        }

        headers = {
            "content-type": "application/json",
            "user-agent": agent
        }
        response = session.post(
            'https://sell.wethenew.com/api/auth/callback/credentials', headers=headers, json=data)

        # time.sleep(0.5)

        headers = {
            "User-Agent": agent
        }

        response = session.get(
            'https://sell.wethenew.com/api/auth/session', headers=headers)
        data = response.json()
        wethenew_token = data["user"]["accessToken"]
        wethenew_refresh_token = data["user"]["refreshToken"]
        next_auth_token = response.cookies['__Secure-next-auth.session-token']

        Log.PrintSuccess(
            "WeTheNew", "Successfully Refreshed Session!")
        return wethenew_token, wethenew_refresh_token, next_auth_token

    except Exception as e:
        Log.PrintError("WeTheNew", f"Error getting wtn tokens: {e}")


def check_session():
    global success
    if success:
        return success
    else:
        success = False
        return success


def get_wethenew_json(sku, wethenew_email, wethenew_password, wethenew_token):
    global success
    # success = check_session()
    success = login(wethenew_token)

    while not success:
        Log.PrintWarning("WeTheNew", "Refreshing session...")
        wethenew_token, wethenew_refresh_token, next_auth_token = get_wtn_token(
            wethenew_email, wethenew_password)
        success = login(wethenew_token)

    try:
        shoe_id = get_wethenew_id(sku, wethenew_token)

        base_url = f"https://sell.wethenew.com/_next/data/rOVyOjeL_YLpm5TCntap1/en/listing/product/{shoe_id}.json"

        params = {
            "id": f"{shoe_id}"
        }

        headers = {
            'Content-Type': "application/json",
            "User-Agent": agent
        }

        response = session.get(base_url, params=params, headers=headers)
        data = response.json()

        shoe_name = data["pageProps"]["initialData"]["name"]
        shoe_image = data["pageProps"]["initialData"]["image"]
        variants = data["pageProps"]["initialData"]["variants"]

        wethenew_json = {
            "site": "Wethenew",
            "name": f"{shoe_name}",
            "image": f"{shoe_image}",
            "sizes": {

            }
        }

        for variant in variants:
            variant_id = variant["id"]
            variant_size = variant["size"].replace(" EU", "")

            headers = {
                'authorization': f'Bearer {wethenew_token}',
                "User-Agent": agent,
            }

            response = session.get(
                f"https://api-sell.wethenew.com/listings/details?variantId={variant_id}", headers=headers)
            lowest_price = response.json()["lowestPrice"]
            lastsold_price = response.json()["lastSoldPrice"]

            wethenew_json["sizes"][variant_size] = {
                "buy_price": f"{lastsold_price}",
                "payout_price": f"{lowest_price}"
            }

        return json.dumps(wethenew_json, indent=4)

    except:
        Log.PrintError("WeTheNew", "SKU not available")


ua = fake_useragent.UserAgent()
agent = ua.random
session = requests.Session()
