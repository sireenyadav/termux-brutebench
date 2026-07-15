#!/usr/bin/env bash

# Termux All-in-One Hardware Profiling Suite
# Automated execution script for unrooted environments

set -e # Exit immediately if a command exits with a non-zero status

clear
echo "=================================================="
echo "   INITIALIZING TERMUX HARDWARE BENCHMARK SUITE   "
echo "=================================================="

# 1. SETUP ENVIRONMENT AND DEPENDENCIES
echo -e "\n[*] Updating system package registries..."
apt update && apt upgrade -y

echo -e "\n[*] Installing core compilation tools and dependencies..."
apt install git cmake clang openssl-tool p7zip root-repo xorgproto -y

# Explicitly pull fio from the root-repo now that it's registered
apt update && apt install fio -y

# Create a temporary workspace for compilation assets
WORKSPACE="$HOME/bench_workspace"
rm -rf "$WORKSPACE" && mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

echo "=================================================="
echo "1. RUNNING RAW CPU BRUTE-FORCE TESTS"
echo "=================================================="
THREADS=$(nproc)
echo "[+] Detected CPU hardware threads: $THREADS"
echo -e "\n--- LSCPU HARDWARE PROFILE ---"
lscpu

echo -e "\n--- 7-ZIP CORE BENCHMARK ---"
7z b

echo -e "\n--- OPENSSL SHA256 MULTI-THREADED CEILING ($THREADS Threads) ---"
openssl speed -multi "$THREADS" sha256

echo -e "\n--- OPENSSL SHA256 SINGLE-THREADED BASELINE ---"
openssl speed sha256

echo "=================================================="
echo "2. COMPILING AND RUNNING RAM BENCHMARK"
echo "=================================================="
echo "[+] Cloning tinymembench source..."
git clone https://github.com/ssvb/tinymembench.git
cd tinymembench

echo "[+] Applying compiler patch for Clang compatibility..."
sed -i '/\.func/d' *.S
sed -i '/\.endfunc/d' *.S

echo "[+] Compiling native optimized binary assets..."
CFLAGS="-O3 -march=native" make

echo -e "\n--- TINYMEMBENCH RUNTIME METRICS ---"
./tinymembench
cd "$WORKSPACE"

echo "=================================================="
echo "3. COMPILING AND RUNNING VULKAN GPU FLOPS METRICS"
echo "=================================================="
echo "[+] Cloning vkpeak project infrastructure..."
git clone --recursive https://github.com/nihui/vkpeak.git
cd vkpeak
mkdir build && cd build
cmake ..
make -j"$THREADS"

echo -e "\n--- VKPEAK VULKAN GPU FLOPS PROFILE ---"
# Explicitly append the native vendor drivers location
export LD_LIBRARY_PATH=/system/lib64:$LD_LIBRARY_PATH
./vkpeak
cd "$WORKSPACE"

echo "=================================================="
echo "4. EXECUTING FILE STORAGE (ROM) PIPELINE SUB-TESTS"
echo "=================================================="
echo -e "\n--- FIO SEQUENTIAL READ/WRITE THROUGHPUT ---"
fio --name=seq_bench --ioengine=psync --rw=rw --bs=1m --size=256m --direct=1 --iodepth=1 --runtime=15 --time_based --end_fsync=1

# Storage cleanup loop
rm -f seq_bench*

echo "=================================================="
echo "          ALL HARDWARE TESTS COMPLETE             "
echo "=================================================="
echo "[+] Cleaning temporary workspace assets..."
rm -rf "$WORKSPACE"
