# <img align="left" width="40px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/2048px-Telegram_logo.svg.png" alt="awesome-ebitengine" title="kubernetes" /> telegram_bot

Track things and get notified via Telegram.

## How to use
Get your secrets ready
1. Create a new bot with @BotFather in Telegram
2. Get an auth token for the bot in format of `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` and save it in `secrets/token`
3. Get your user id from @userinfobot in format of `123456789` and save it in `secrets/user_id`

Note: My secrets are encrypted with Strongbox (https://github.com/uw-labs/strongbox)

Create a python venv and install the required packages
1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt --upgrade pip`

## Enabling cron service in WSL (If using Windows)
1. Add this line to `/etc/sudoers`  
```%sudo   ALL=(ALL) NOPASSWD: /usr/sbin/service cron start```
2. Go to Windows Start-up (`Win` + `R` and `shell:startup`)
3. Create a `.bat` file with the following command  
```wsl sudo service cron start```

## Automating runs with cron
1. Check `run.sh` for scripts that will get executed
2. Manually start `cron` service if it's not running
3. Add cron jobs to execute scripts e.g.:
```
# Telegram Bot:
0 * * * * cd /home/me/telegram_bot/ && ./run.sh
```
The script will loop through all directories specified in the `run.sh` and execute all `.py` scripts inside these directories. Remove directories you don't need from `run.sh` or rename python scripts if you want to temporarily disable them.
