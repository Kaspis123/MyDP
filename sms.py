from pystyle import Colors, Colorate, Write  # pip install pystyle
import requests
import os
from colorama import init, Fore

os.system('cls' if os.name == 'nt' else 'clear')

# some colors
init()
GREEN = Fore.GREEN
RED = Fore.RED




def main():
    phone = Write.Input("[*] Enter number of the victim : ", Colors.yellow_to_red)
    print(f">>> {phone}")
    message = Write.Input("[*] ENTER YOUR MSG           :", Colors.blue_to_white)
    print(f">>> {message}")
    resp = requests.post('https://textbelt.com/text', {
        'phone': f'{phone}',
        'message': f'{message}',
        'key': 'textbelt',
    })
    print("\n")
    print(f"{GREEN} {resp.json()}")


if __name__ == "__main__":
    main()