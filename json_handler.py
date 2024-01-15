import json
from log import Log

CONFIG = "config.json"


def print_json(json_file, site="others"):
    data = json.loads(json_file)
    name = data["name"]
    sizes = data["sizes"]
    if site == "wethenew":
        print(f"\n\t   {name}")
        print("\t   {:<6} | {:<8} | {:<6}".format(
            "Size", "LastSold", "Lowest"))

        for size, prices in sizes.items():
            buy_price = prices.get("buy_price", "N/A")
            payout_price = prices.get("payout_price", "N/A")
            print("\t   {:<6} | {:<8} | {:<6}".format(
                size, buy_price, payout_price))

    else:
        print(f"\n\t   {name}")
        print("\t   {:<6} | {:<6} | {:<6}".format("Size", "Buy", "Sell"))
        for size, prices in sizes.items():
            buy_price = prices.get("buy_price", "N/A")
            payout_price = prices.get("payout_price", "N/A")
            print("\t   {:<6} | {:<6} | {:<6}".format(
                size, buy_price, payout_price))


def load_discord_token(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data["discord_token"] == "":
        Log.PrintError("Config", "Input your discord token on config.json")
        exit()

    discord_token = data["discord_token"]

    return discord_token


def load_webhook(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data["webhook"] == "":
        Log.PrintError("Config", "Input your webhook on config.json")
        exit()

    webhook = data["webhook"]

    return webhook


def load_sneakit_credentials(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data["sneakit"]["email"] == "" or data["sneakit"]["password"] == "":
        Log.PrintError(
            "Config", "Input your sneakit email or password correctly on config.json")
        exit()

    sneakit_email = data["sneakit"]["email"]
    sneakit_password = data["sneakit"]["password"]

    return sneakit_email, sneakit_password


def load_wethenew_credentials(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data["wethenew"]["email"] == "" or data["wethenew"]["password"] == "":
        Log.PrintError(
            "Config", "Input your wethenew email or password correctly on config.json")
        exit()

    wethenew_email = data["wethenew"]["email"]
    wethenew_password = data["wethenew"]["password"]
    wethenew_token = data["wethenew"]["token"]

    return wethenew_email, wethenew_password, wethenew_token
