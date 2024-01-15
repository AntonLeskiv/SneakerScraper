import discord
import threading
from discord.ext import commands
from json_handler import load_discord_token, load_webhook, load_sneakit_credentials, load_wethenew_credentials, CONFIG
from webhooks import send_webhook
from sneakit import get_sneakit_json
from hypeboost import get_hypeboost_json
from stockx import get_stockx_json
from klekt import get_klekt_json
from wethenew import get_wethenew_json
from log import Log

sneakit_email, sneakit_password = load_sneakit_credentials(CONFIG)
wethenew_email, wethenew_password, wethenew_token = load_wethenew_credentials(
    CONFIG)
webhook = load_webhook(CONFIG)
discord_token = load_discord_token(CONFIG)


def run_klekt(sku):
    Log.PrintWarning("Klekt", f"Scrapping {sku} on Klekt")
    klekt_json = get_klekt_json(sku)
    send_webhook(klekt_json, webhook)
    Log.PrintSuccess("Klekt", f"Klekt {sku} webhook sent")


def run_hypeboost(sku):
    Log.PrintWarning("Hypeboost", f"Scrapping {sku} on Hypeboost")
    hypeboost_json = get_hypeboost_json(sku)
    send_webhook(hypeboost_json, webhook)
    Log.PrintSuccess("Hypeboost", f"Hypeboost {sku} webhook sent")


def run_sneakit(sku):
    Log.PrintWarning("Sneakit", f"Scrapping {sku} on Sneakit")
    sneakit_json = get_sneakit_json(sku, sneakit_email, sneakit_password)
    send_webhook(sneakit_json, webhook)
    Log.PrintSuccess("Sneakit", f"Sneakit {sku} webhook sent")


def run_stockx(sku):
    Log.PrintWarning("StockX", f"Scrapping {sku} on StockX")
    stockx_json = get_stockx_json(sku)
    send_webhook(stockx_json, webhook)
    Log.PrintSuccess("StockX", f"StockX {sku} webhook sent")
    # TODO


def run_wethenew(sku):
    Log.PrintWarning("WeTheNew", f"Scrapping {sku} on WeTheNew")
    wethenew_json = get_wethenew_json(
        sku, wethenew_email, wethenew_password, wethenew_token)
    send_webhook(wethenew_json, webhook, "wethenew")
    Log.PrintSuccess("WeTheNew", f"WeTheNew {sku} webhook sent")
    # TODO


def thread_handler(function, *args):
    thread = threading.Thread(target=function, args=(args))
    thread.start()


def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # COMANDOS DEL BOT DE DISCORD
    @bot.event
    async def on_ready():
        Log.PrintSuccess("Bot", f'Connected as {bot.user.name}')

    @bot.command()
    async def k(ctx, sku):  # Klekt
        thread_handler(run_klekt, sku)

    @bot.command()
    async def sx(ctx, sku):  # Stockx
        thread_handler(run_stockx, sku)

    @bot.command()
    async def w(ctx, sku):  # WeTheNew
        thread_handler(run_wethenew, sku)

    @bot.command()
    async def h(ctx, sku):  # Hypeboost
        thread_handler(run_hypeboost, sku)

    @bot.command()
    async def s(ctx, sku):  # Sneakit
        thread_handler(run_sneakit, sku)

    @bot.command()
    async def all(ctx, sku):  # All sites
        thread_handler(run_klekt, sku)
        thread_handler(run_hypeboost, sku)
        thread_handler(run_sneakit, sku)
        thread_handler(run_wethenew, sku)
        thread_handler(run_stockx, sku)

    bot.run(f'{discord_token}')
