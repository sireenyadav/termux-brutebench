#!/usr/bin/env python3
import sys
from types import ModuleType

# =========================================================================
# PROGRAMMATIC IN-MEMORY MOCK: Intercept PIL calls to prevent Pillow errors
# =========================================================================
pil_mock = ModuleType("PIL")
image_mock = ModuleType("PIL.Image")
pil_mock.Image = image_mock
sys.modules["PIL"] = pil_mock
sys.modules["PIL.Image"] = image_mock
# =========================================================================

import os
import subprocess
import time
from tqdm import tqdm

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def run_command(cmd, timeout=120):
    """Executes platform commands safely with variable time limits."""
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout else "Command completed successfully."
        else:
            return f"Execution Warning (Return Code {result.returncode}):\n{result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return f"Performance sub-test cut off after exceeding {timeout}s window."
    except Exception as e:
        return f"System loop execution error: {str(e)}"

def main():
    # Setup working execution sandbox path explicitly inside home directory
    workspace = os.path.expanduser("~/bench_workspace")
    os.makedirs(workspace, exist_ok=True)
    os.chdir(workspace)

    # Core execution configurations - Extended compilation timeouts to 600s
    steps = [
        ("Synchronizing Core Repositories", "apt update -y", 120),
        ("Deploying Benchmark Toolchains", "apt install git cmake clang openssl-tool p7zip root-repo xorgproto fio -y", 300),
        ("Analyzing Processor Architecture", "lscpu", 60),
        ("Auditing 7-Zip Core MIPS Calculations", "7z b", 180),
        ("Measuring Cryptographic Hash Limits", f"openssl speed -multi {os.cpu_count() or 4} sha256", 180),
        ("Compiling RAM Performance Library", "rm -rf tinymembench && git clone https://github.com/ssvb/tinymembench.git && cd tinymembench && sed -i '/\\.func/d' *.S && sed -i '/\\.endfunc/d' *.S && CFLAGS='-O3 -march=native' make", 600),
        ("Evaluating Memory Speed & Latency", "./tinymembench/tinymembench", 180),
        ("Compiling Vulkan Acceleration Code", "rm -rf vkpeak && git clone --recursive https://github.com/nihui/vkpeak.git && cd vkpeak && mkdir build && cd build && cmake .. && make -j$(nproc)", 600),
        ("Measuring Raw Vulkan GPU FLOPS", "export LD_LIBRARY_PATH=/system/lib64:$LD_LIBRARY_PATH && ./vkpeak/build/vkpeak", 180),
        ("Auditing ROM Flash Storage Bandwidth", "fio --name=seq_bench --ioengine=psync --rw=rw --bs=1m --size=256m --direct=1 --iodepth=1 --runtime=15 --time_based --end_fsync=1", 120)
    ]

    results = {}
    
    with tqdm(total=len(steps), desc="Benchmark Execution", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {percentage:3.0f}%]") as pbar:
        for description, command, timeout_limit in steps:
            pbar.set_postfix_str(f"Active: {description[:22]}...")
            
            # Lock the run command execution into the active sandbox folder
            output = run_command(command, timeout=timeout_limit)
            results[description] = output
            pbar.update(1)
            time.sleep(0.2)

    # Clean working folder directories completely
    os.chdir(os.path.expanduser("~"))
    subprocess.run("rm -rf bench_workspace seq_bench*", shell=True)

    print("\n[+] Compiling architecture metrics into final PDF document...")
    generate_pdf(results)

def generate_pdf(data):
    download_dir = "/storage/emulated/0/Download"
    if not os.path.exists(download_dir):
        download_dir = os.path.expanduser("~/storage/downloads")
    if not os.path.exists(download_dir):
        download_dir = os.path.expanduser("~")
        
    pdf_path = os.path.join(download_dir, "benchmark.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=colors.HexColor("#1A365D"), spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], fontSize=12, leading=15, textColor=colors.HexColor('#2B6CB0'), spaceBefore=10, spaceAfter=5
    )
    body_style = ParagraphStyle(
        'ReportBody', parent=styles['Code'], fontSize=7, leading=9, textColor=colors.HexColor('#2D3748')
    )

    story.append(Paragraph("Termux System Performance Report", title_style))
    story.append(Paragraph(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    for section_name, raw_output in data.items():
        if "Synchronizing" in section_name or "Deploying" in section_name:
            continue
            
        story.append(Paragraph(section_name, section_style))
        formatted_text = raw_output.replace('\n', '<br/>').replace(' ', '&nbsp;')
        table_data = [[Paragraph(formatted_text, body_style)]]
        
        out_table = Table(table_data, colWidths=[530])
        out_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(out_table)
        story.append(Spacer(1, 8))

    try:
        doc.build(story)
        print(f"[✔] Profiling complete! PDF report saved directly to your main Downloads folder:\n    {pdf_path}\n")
    except Exception as e:
        fallback_path = os.path.join(os.path.expanduser("~"), "benchmark.pdf")
        doc.build(SimpleDocTemplate(fallback_path, pagesize=letter))

if __name__ == "__main__":
    main()
