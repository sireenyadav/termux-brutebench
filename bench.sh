#!/usr/bin/env bash
set -e

echo "=================================================="
echo "    BOOTSTRAPPING AUTOMATED BENCHMARK ENGINE      "
echo "=================================================="

# 1. Check and request standard Android local folder storage permissions
if [ ! -d "$HOME/storage" ]; then
    echo "[*] Setting up storage permission symlinks..."
    termux-setup-storage
    echo "[!] A pop-up will appear. Please tap 'Allow' to authorize storage access."
    sleep 5
fi

# 2. Update package registers and auto-install Python if missing
echo "[*] Verifying system execution dependencies..."
apt update -y
if ! command -v python3 &> /dev/null; then
    echo "[*] Python 3 not found. Automatically installing core runtime environment..."
    apt install python -y
else
    echo "[+] Python 3 runtime verified."
fi

# 3. Force silent installation of reporting and bar UI packages via pip
echo "[*] Ensuring UI progress and reporting modules are present..."
pip install tqdm reportlab --quiet --no-warn-script-location

# 4. Grab the core Python calculation matrix from your repository and pass execution
echo "[*] Triggering main performance computation framework..."
curl -sL https://raw.githubusercontent.com/sireenyadav/termux-brutebench/main/bench.py > bench.py
python3 bench.py

# 5. Sweep out the runtime loader footprint
rm -f bench.py
