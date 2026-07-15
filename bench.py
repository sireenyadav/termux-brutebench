#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from tqdm import tqdm

# ReportLab libraries for professional PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def run_command(cmd, shell=True):
    """Executes a terminal operation and captures output safely."""
    try:
        result = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        return result.stdout.strip() if result.stdout else result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Test execution timed out after 60 seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"

def main():
    print("==================================================")
    print("   INITIALIZING TERMUX AUTOMATED PROFILER V2      ")
    print("==================================================")

    # 1. Define the step sequence for the continuous progress tracking
    steps = [
        ("Registering System Repositories", "apt update -y"),
        ("Installing Engine Utilities", "apt install git cmake clang openssl-tool p7zip root-repo xorgproto -y && apt update && apt install fio -y"),
        ("Analyzing Core CPU Topology", "lscpu"),
        ("Evaluating 7-Zip Core MIPS", "7z b"),
        ("Measuring Cryptographic Scaling", f"openssl speed -multi {os.cpu_count() or 4} sha256"),
        ("Compiling RAM Test Suite", "rm -rf tinymembench && git clone https://github.com/ssvb/tinymembench.git && cd tinymembench && sed -i '/\\.func/d' *.S && sed -i '/\\.endfunc/d' *.S && CFLAGS='-O3 -march=native' make"),
        ("Evaluating Memory Bandwidth & Latency", "./tinymembench/tinymembench"),
        ("Compiling Vulkan GPU Matrices", "rm -rf vkpeak && git clone --recursive https://github.com/nihui/vkpeak.git && cd vkpeak && mkdir build && cd build && cmake .. && make -j$(nproc)"),
        ("Measuring Vulkan GPU FLOPS", "export LD_LIBRARY_PATH=/system/lib64:$LD_LIBRARY_PATH && ./vkpeak/build/vkpeak"),
        ("Executing ROM Storage Benchmarks", "fio --name=seq_bench --ioengine=psync --rw=rw --bs=1m --size=256m --direct=1 --iodepth=1 --runtime=15 --time_based --end_fsync=1")
    ]

    results = {}
    
    # 2. Continuous Constant Progress Bar Tracking Loop
    with tqdm(total=len(steps), desc="Overall Benchmark Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {percent:3.0f}%]") as pbar:
        for description, command in steps:
            pbar.set_postfix_str(f"Active: {description[:25]}...")
            
            # Specialized cleanup handlers to ensure local execution runs cleanly
            if "tinymembench/tinymembench" in command or "vkpeak" in command:
                output = run_command(command, shell=True)
            else:
                output = run_command(command)
                
            results[description] = output
            pbar.update(1)
            time.sleep(0.5)

    # Post-run filesystem environment cleanup
    run_command("rm -rf tinymembench vkpeak seq_bench*")

    print("\n[+] Compiling hardware assets into PDF format...")
    generate_pdf(results)

def generate_pdf(data):
    # Setup target mobile download directory paths securely
    download_dir = "/data/data/com.termux/files/home/storage/downloads"
    if not os.path.exists(download_dir):
        # Fallback to local home folder if storage link is missing
        download_dir = "/data/data/com.termux/files/home"
        
    pdf_path = os.path.join(download_dir, "benchmark.pdf")
    
    # Initialize page flow structure configuration
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom stylesheet layout components
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Code'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#2D3748')
    )

    # Document Header Elements
    story.append(Paragraph("Termux System Performance Report", title_style))
    story.append(Paragraph(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Parse captured output string chunks directly into layout panels
    for section_name, raw_output in data.items():
        if "Updating" in section_name or "Installing" in section_name:
            continue # Skip installation tracking output logs to keep report clean
            
        story.append(Paragraph(section_name, section_style))
        
        # Format terminal arrays inside a protected document block data matrix
        formatted_text = raw_output.replace('\n', '<br/>').replace(' ', '&nbsp;')
        table_data = [[Paragraph(formatted_text, body_style)]]
        
        out_table = Table(table_data, colWidths=[530])
        out_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        
        story.append(out_table)
        story.append(Spacer(1, 10))

    doc.build(story)
    print(f"[✔] Success! A stylized PDF layout has been compiled and saved to:\n    {pdf_path}\n")

if __name__ == "__main__":
    main()
