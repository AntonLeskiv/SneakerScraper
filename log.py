from datetime import datetime
from colorama import Fore, Style


class Log:
    def PrintTitle(text):
        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

    def PrintNormal(store, text):
        timenow = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{Fore.WHITE}[{timenow}] [{store}] {text}{Style.RESET_ALL}")

    def PrintSuccess(store, text):
        timenow = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{Fore.GREEN}[{timenow}] [{store}] {text}{Style.RESET_ALL}")

    def PrintError(store, text):
        timenow = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{Fore.RED}[{timenow}] [{store}] {text}{Style.RESET_ALL}")

    def PrintWarning(store, text):
        timenow = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{Fore.YELLOW}[{timenow}] [{store}] {text}{Style.RESET_ALL}")
