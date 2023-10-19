import telebot 
import requests
from bs4 import BeautifulSoup
import time
import datetime

# Steam vars
URLS = ["https://store.steampowered.com/app/1434950/HighFleet",
        "https://store.steampowered.com/app/526870/Satisfactory",
        "https://store.steampowered.com/app/892970/Valheim"]

# Telegram vars
with open('../secrets/bot_token', 'r') as file:
    BOT_TOKEN = file.read().strip()
with open('../secrets/user_id', 'r') as file:
    USER_ID = int(file.read().strip())
bot = telebot.TeleBot(BOT_TOKEN)

def check_achievementsy(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        achievements_label = soup.find('div', class_='label', string='Steam Achievements')

        print(achievements_label)

        if achievements_label:
            send_message("🎮 Achievements added!\n" + url)

def send_message(message):
    bot.send_message(USER_ID, message, parse_mode='html')

def main():
    for url in URLS:
        check_achievementsy(url)

if __name__ == "__main__":
    main()
