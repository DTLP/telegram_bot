#!/bin/bash

current_dir="$(pwd)"

source /home/$USER/homelab/telegram_bot/venv/bin/activate

pip install -r requirements.txt --upgrade pip

for dir in *; do
	if [ -d "$dir" ] && [ "$(basename "$dir")" != "venv" ]; then
		cd "$current_dir/$dir"
		python *.py
		cd -
	fi
done
