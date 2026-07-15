#!/usr/bin/env bash
set -e
# 1. Force verify Android terminal storage hooks exist
if [ ! -d "$HOME/storage" ]; then
    echo "[!] Setting up storage permission links..."
    termux-setup-storage
    sleep 3
fi

# 2. Bootstrap Python platform prerequisites
pkg install python -y
pip install tqdm reportlab --quiet

# 3. Pull down the live Python script module and execute it
curl -sL https://raw.githubusercontent.com/sireenyadav/termux-brutebench/main/bench.py > bench.py
python3 bench.py
rm -f bench.py
