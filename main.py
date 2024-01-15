import threading
import os
from hypeboost import get_hypeboost_json
from sneakit import get_sneakit_json
from klekt import get_klekt_json
from stockx import get_stockx_json
from wethenew import get_wethenew_json
from json_handler import print_json, load_sneakit_credentials, load_wethenew_credentials, CONFIG
from discord_bot import run_bot
from log import Log
from colorama import Fore, Style

logo = '''
   _____                      __                  _____                                      
  / ___/ ____   ___   ____ _ / /__ ___   _____   / ___/ _____ _____ ____ _ ____   ___   _____
  \__ \ / __ \ / _ \ / __ `// //_// _ \ / ___/   \__ \ / ___// ___// __ `// __ \ / _ \ / ___/
 ___/ // / / //  __// /_/ // ,<  /  __// /      ___/ // /__ / /   / /_/ // /_/ //  __// /    
/____//_/ /_/ \___/ \__,_//_/|_| \___//_/      /____/ \___//_/    \__,_// .___/ \___//_/      by viksel
                                                                       /_/                    
'''

modules = """
\t   [1] Console Bot Scraper (cmd)
\t   [2] Discord Bot Scraper
\t   [0] Exit
"""

store_modules = """
\t   [1] ALL
\t   [2] Klekt
\t   [3] StockX 
\t   [4] Sneakit
\t   [5] WeTheNew (Coming soon)
\t   [6] Hypeboost
\t   [0] Back to main menu
"""

sneakit_email, sneakit_password = load_sneakit_credentials(CONFIG)
wethenew_email, wethenew_password, wethenew_token = load_wethenew_credentials(
    CONFIG)


def thread_handler(function, *args):
    thread = threading.Thread(target=function, args=(args))
    thread.start()


def repeat(function, sku, *args):
    while True:
        choose = str(input(
            Fore.YELLOW + "\t   Input another SKU or type [0] for main menu: " + Style.RESET_ALL))
        if choose == "0":
            break
        else:
            sku = choose
            function(sku, *args)
    choose_store_module()


def all_module(sku):
    thread_handler(wethenew_module, sku, wethenew_email,
                   wethenew_password, wethenew_token)
    thread_handler(klekt_module, sku)
    thread_handler(sneakit_module, sku, sneakit_email, sneakit_password)
    thread_handler(hypeboost_module, sku)
    thread_handler(stockx_module, sku)


def klekt_module(sku):
    Log.PrintWarning("Klekt", ":")
    klekt_json = get_klekt_json(sku)
    if not klekt_json == None:
        print_json(klekt_json + "\n")


def stockx_module(sku):
    Log.PrintWarning("StockX", ":")
    stockx_json = get_stockx_json(sku)
    if not stockx_json == None:
        print_json(stockx_json + "\n")


def sneakit_module(sku, sneakit_email, sneakit_password):
    sneakit_json = get_sneakit_json(sku, sneakit_email, sneakit_password)
    Log.PrintWarning("Sneakit", ":")
    if not sneakit_json == None:
        print_json(sneakit_json)


def wethenew_module(sku, wethenew_email, wethenew_password, wethenew_token):
    wethenew_json = get_wethenew_json(
        sku, wethenew_email, wethenew_password, wethenew_token)
    Log.PrintWarning("Wethenew", ":")
    if not wethenew_json == None:
        print_json(wethenew_json)


def hypeboost_module(sku):
    Log.PrintWarning("Hypeboost", ":")
    hypeboost_json = get_hypeboost_json(sku)
    if not hypeboost_json == None:
        print_json(hypeboost_json + "\n")


def choose_store_module():
    Log.PrintWarning("Menu", store_modules)
    store_module = int(
        input(Fore.YELLOW + "\t   Choose a store to scrap: " + Style.RESET_ALL))

    if store_module == 1:  # All
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        all_module(sku)
        repeat(all_module, sku)

    elif store_module == 2:  # Klekt
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        klekt_module(sku)
        repeat(klekt_module, sku)

    elif store_module == 3:  # StockX
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        stockx_module(sku)
        repeat(stockx_module, sku)

    elif store_module == 4:  # Sneakit
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        sneakit_module(sku, sneakit_email, sneakit_password)
        repeat(sneakit_module, sku, sneakit_email, sneakit_password)

    elif store_module == 5:  # WetheNew
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        wethenew_module(sku, wethenew_email, wethenew_password, wethenew_token)
        repeat(wethenew_module, sku, wethenew_email,
               wethenew_password, wethenew_token)

    elif store_module == 6:  # Hypeboost
        sku = str(input(Fore.YELLOW + "\t   Input SKU here: " + Style.RESET_ALL))
        hypeboost_module(sku)
        repeat(hypeboost_module, sku)

    elif store_module == 0:
        main()


def choose_module():
    Log.PrintWarning("Menu", modules)
    module = int(
        input(Fore.YELLOW + "\t   Choose a module: " + Style.RESET_ALL))

    if module == 1:
        choose_store_module()

    elif module == 2:
        run_bot()

    elif module == 0:
        exit()

    else:
        Log.PrintError("Menu", "\t   Choose a valid module!")
        choose_module()


def main():
    os.system('cls')
    Log.PrintTitle(logo)
    choose_module()


main()
