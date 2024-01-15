import requests
import json


def format_sizes(sizes, site):
    max_size_len = max(len(size) for size in sizes.keys())
    if site == "wethenew":
        formatted_sizes = f"```{'SIZE'.ljust(max_size_len)} | {'LAST SOLD'.ljust(9)} | {'LOWEST'.ljust(6)}\n{'-' * (max_size_len + 21)}\n"

    else:
        formatted_sizes = f"```{'SIZE'.ljust(max_size_len)} | {'BUY PRICE'.ljust(9)} | {'PAYOUT'.ljust(6)}\n{'-' * (max_size_len + 21)}\n"

    for size, prices in sizes.items():
        formatted_sizes += f"{size.ljust(max_size_len)} | {prices['buy_price'].ljust(9)} | {prices['payout_price'].ljust(6)}\n"

    formatted_sizes += "```"
    return formatted_sizes


def send_webhook(data, webhook, site="others"):
    data = json.loads(data)

    embed = {
        "title": data["name"],
        "description": format_sizes(data["sizes"], site),
        "color": 39423,
        "author": {
            "name": data["site"] + " Prices"
        },
        "footer": {
            "text": "SneakerScraper by viksel"
        },
        "thumbnail": {
            "url": data["image"]
        }
    }

    payload = {"embeds": [embed],
               "username": "Sneaker Scraper"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook, json=payload, headers=headers)
