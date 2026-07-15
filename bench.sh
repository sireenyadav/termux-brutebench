#!/usr/bin/env bash
set -e

echo "=================================================="
echo "    BOOTSTRAPPING AUTOMATED BENCHMARK ENGINE      "
echo "=================================================="

# 1. Request standard Android directory storage authorization links
if [ ! -d "$HOME/storage" ]; then
    echo "[*] Initializing system storage access links..."
    termux-setup-storage
    echo "[!] Action required: Tap 'Allow' on the system access prompt window."
    sleep 5
fi

# 2. Synchronize apt package databases and install Python core if missing
echo "[*] Validating core operating dependencies..."
apt update -y
if ! command -v python3 &> /dev/null; then
    echo "[*] Python 3 not detected. Commencing automated deployment..."
    apt install python -y
else
    echo "[+] Python 3 platform environment verified."
fi

# 3. Securely pull user interface and data mapping libraries via pip
echo "[*] Building isolated runtime module libraries..."
pip install tqdm --quiet --no-warn-script-location
pip install reportlab --no-deps --quiet --no-warn-script-location

# 4. Stream down the master calculation matrix and pass control
echo "[*] Initializing primary performance calculation matrix..."
curl -sL https://raw.githubusercontent.com/sireenyadav/termux-brutebench/main/bench.py > bench.py
python3 bench.py

# 5. Clear out temporary pipeline loaders from the local terminal context
rm -f bench.py
