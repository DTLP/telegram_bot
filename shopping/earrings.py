import telebot 
import requests
from bs4 import BeautifulSoup
import time
import datetime
import os

# Website vars
URL = 'https://safsafu.com/collections/earrings/products/silver-maneki-neko-earring'
custom_cookies = {
    'cart_currency': 'GBP',
    'localization': 'GB',
}

# Telegram vars
with open('../secrets/bot_token', 'r') as file:
    BOT_TOKEN = file.read().strip()
with open('../secrets/user_id', 'r') as file:
    USER_ID = int(file.read().strip())
bot = telebot.TeleBot(BOT_TOKEN)

# Other vars
script_path = os.path.abspath(__file__)
script_name = os.path.splitext(os.path.basename(script_path))[0]
value_file_path = os.path.join(os.getcwd(), f'{script_name}-value.txt')

def check_price():
    previous_value = int(get_previous_value_from_file())
    current_value = int(get_current_value())
    compare_values(previous_value, current_value)
    save_value_to_file(current_value)

def get_previous_value_from_file():
    try:
        with open(value_file_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def get_current_value():
    response = requests.get(URL, cookies=custom_cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        label = soup.find('span', class_='price-item price-item--regular', attrs={'data-regular-price': True})
        value = label.text.replace("£","")
        return value

def compare_values(previous, current):
    if previous > current:
        send_message(f"🛒Price went down from <b>{previous}</b> "
        f"to <b>{current}</b>{URL}")

def save_value_to_file(value):
    with open(value_file_path, 'w') as file:
        file.write(str(value))

def send_message(message):
    bot.send_message(USER_ID, message, parse_mode='html')

def main():
    check_price()

if __name__ == "__main__":
    main()
