import telebot 
import requests
from bs4 import BeautifulSoup
import time
import datetime

# Steam vars
URL = "https://store.steampowered.com/app/1086940/Baldurs_Gate_3"

# Telegram vars
with open('../secrets/bot_token', 'r') as file:
    BOT_TOKEN = file.read().strip()
with open('../secrets/user_id', 'r') as file:
    USER_ID = int(file.read().strip())
bot = telebot.TeleBot(BOT_TOKEN)

def check_crossplay():
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        crossplay_label = soup.find('div', class_='label', string='Cross-Platform Multiplayer')

        print(crossplay_label)

        if crossplay_label:
            send_message("🎮 Crossplay added!\n" + URL)

def send_message(message):
    bot.send_message(USER_ID, message, parse_mode='html')

def main():
    check_crossplay()

if __name__ == "__main__":
    main()
