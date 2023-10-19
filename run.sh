#!/bin/bash

current_dir="$(pwd)"

source ${current_dir}/venv/bin/activate

pip install -r ${current_dir}/requirements.txt --upgrade pip

dirs=(
	network
	shopping
	steam
)

for dir in "${dirs[@]}"; do
	cd ${current_dir}/${dir}
	find -type f -name "*.py" -exec python3 '{}' \;
done
