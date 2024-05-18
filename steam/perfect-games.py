import telebot 
import requests
from bs4 import BeautifulSoup
import time
import datetime

# Steam vars
STEAM_PROFILE_URL = "https://steamcommunity.com/id/<steam_profile>"

# Telegram vars
with open('../secrets/bot_token', 'r') as file:
    BOT_TOKEN = file.read().strip()
with open('../secrets/user_id', 'r') as file:
    USER_ID = int(file.read().strip())
bot = telebot.TeleBot(BOT_TOKEN)

def check_perfect_games():
    previous_value = int(get_previous_value_from_file())
    current_value = int(get_current_value_from_steam())
    compare_values(previous_value, current_value)
    save_value_to_file(current_value)

def get_previous_value_from_file():
    try:
        with open('perfect-games-count.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def get_perfect_game_ids_from_file():
    try:
        with open('perfect-games.list', 'r') as file:
            # Read lines and convert each line to integer
            ids = [str(line.strip()) for line in file.readlines()]
            return ids
    except FileNotFoundError:
        return []

def get_current_value_from_steam():
    response = requests.get(STEAM_PROFILE_URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        perfect_games_label = soup.find('div', class_='label', string='Perfect Games')

        if perfect_games_label:
            perfect_games_value = perfect_games_label.find_previous_sibling('div', class_='value')
            if perfect_games_value:
                current_perfect_games = perfect_games_value.text.strip()
                return current_perfect_games
            else:
                print("Perfect Games value not found")
        else:
            print("Perfect Games label not found")

def compare_values(previous, current):
    if previous < current:
        send_message(f"🏆⬆️Congrats! New perfect Steam games count: <b>{current}</b>")
    elif previous > current:
        game = get_updated_game()
        send_message(f"🏆⬇️Perfect Steam games count went down from <b>{previous}</b> to <b>{current}</b>\nGame updated: {game}")

def get_updated_game():
    game_ids = get_perfect_game_ids_from_file()

    for game_id in game_ids:

        response = requests.get(STEAM_PROFILE_URL + "/stats/" + game_id + "/?tab/=achievements")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            percentage_div = soup.find(id='topSummaryAchievements')
            if percentage_div:
                text = percentage_div.get_text(strip=True).lower()

                index = text.find('achievements earned:')

                if index != -1:
                    start_index = text.rfind('(', 0, index)
                    end_index = text.find('%)', start_index)

                    if start_index != -1 and end_index != -1:
                        percentage_str = text[start_index + 1: end_index]
                        percentage = int(percentage_str.split('%')[0])

            if percentage < 100:
                game_url = "https://store.steampowered.com/app/" + game_id
                return game_url

            time.sleep(.5)

def get_name(id):
    return data_clean[id]

def save_value_to_file(value):
    with open('value.txt', 'w') as file:
        file.write(str(value))

def send_message(message):
    bot.send_message(USER_ID, message, parse_mode='html')

def main():
    check_perfect_games()

if __name__ == "__main__":
    main()
