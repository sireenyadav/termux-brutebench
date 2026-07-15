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

# ReportLab document engine layers load cleanly
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def run_command(cmd, shell=True):
    """Executes platform binaries safely with structured time boundaries."""
    try:
        result = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout else "Command executed successfully with zero output lines."
        else:
            return f"Execution Warning (Return Code {result.returncode}):\n{result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Performance sub-test processing limit exceeded 120-second timeout window."
    except Exception as e:
        return f"System loop execution error: {str(e)}"

def main():
    # Core performance execution sequence checklist
    steps = [
        ("Synchronizing Core Repositories", "apt update -y"),
        ("Deploying Benchmark Toolchains", "apt install git cmake clang openssl-tool p7zip root-repo xorgproto -y && apt update && apt install fio -y"),
        ("Analyzing Processor Architecture", "lscpu"),
        ("Auditing 7-Zip Core MIPS Calculations", "7z b"),
        ("Measuring Cryptographic Hash Limits", f"openssl speed -multi {os.cpu_count() or 4} sha256"),
        ("Compiling RAM Performance Library", "rm -rf tinymembench && git clone https://github.com/ssvb/tinymembench.git && cd tinymembench && sed -i '/\\.func/d' *.S && sed -i '/\\.endfunc/d' *.S && CFLAGS='-O3 -march=native' make"),
        ("Evaluating Memory Speed & Latency", "./tinymembench/tinymembench"),
        ("Compiling Vulkan Acceleration Code", "rm -rf vkpeak && git clone --recursive https://github.com/nihui/vkpeak.git && cd vkpeak && mkdir build && cd build && cmake .. && make -j$(nproc)"),
        ("Measuring Raw Vulkan GPU FLOPS", "export LD_LIBRARY_PATH=/system/lib64:$LD_LIBRARY_PATH && ./vkpeak/build/vkpeak"),
        ("Auditing ROM Flash Storage Bandwidth", "fio --name=seq_bench --ioengine=psync --rw=rw --bs=1m --size=256m --direct=1 --iodepth=1 --runtime=15 --time_based --end_fsync=1")
    ]

    results = {}
    
    # Corrected progress string parsing configuration (swapped percent for percentage)
    with tqdm(total=len(steps), desc="Benchmark Execution", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {percentage:3.0f}%]") as pbar:
        for description, command in steps:
            pbar.set_postfix_str(f"Active: {description[:22]}...")
            
            # Context state routing adjustments
            if "tinymembench/tinymembench" in command or "vkpeak" in command:
                output = run_command(command, shell=True)
            else:
                output = run_command(command)
                
            results[description] = output
            pbar.update(1)
            time.sleep(0.3)

    # Clean working folder directories completely
    run_command("rm -rf tinymembench vkpeak seq_bench*")

    print("\n[+] Compiling architecture metrics into final PDF document...")
    generate_pdf(results)

def generate_pdf(data):
    # Establish default paths for Android internal shared storage panels
    download_dir = "/data/data/com.termux/files/home/storage/downloads"
    if not os.path.exists(download_dir):
        download_dir = "/data/data/com.termux/files/home"
        
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
        # Safely convert spacing characters to web layout structures
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

    doc.build(story)
    print(f"[✔] Profiling complete! Structured PDF layout saved directly to target directory:\n    {pdf_path}\n")

if __name__ == "__main__":
    main()
