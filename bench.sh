#!/usr/bin/env bash
set -e

echo "=================================================="
echo "    BOOTSTRAPPING AUTOMATED BENCHMARK ENGINE      "
echo "=================================================="

# 1. Request standard Android folder storage authorization
if [ ! -d "$HOME/storage" ]; then
    echo "[*] Setting up storage permission symlinks..."
    termux-setup-storage
    echo "[!] A window will pop up. Please tap 'Allow' to authorize storage access."
    sleep 5
fi

# 2. Update registries and pull Python if missing
echo "[*] Verifying system execution dependencies..."
apt update -y
if ! command -v python3 &> /dev/null; then
    echo "[*] Python 3 not found. Automatically installing core runtime environment..."
    apt install python -y
else
    echo "[+] Python 3 runtime verified."
fi

# 3. Securely install modules bypassing Pillow asset chains
echo "[*] Ensuring UI progress and reporting modules are present..."
pip install tqdm --quiet --no-warn-script-location
pip install reportlab --no-deps --quiet --no-warn-script-location

# 4. Fetch the primary Python benchmark engine and execute it
echo "[*] Triggering main performance computation framework..."
curl -sL https://raw.githubusercontent.com/sireenyadav/termux-brutebench/main/bench.py > bench.py
python3 bench.py

# 5. Wiping temporary loader files
rm -f bench.py
