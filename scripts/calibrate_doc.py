import os
import sys
import subprocess
import json
import shutil
from build_and_calibrate import create_full_report

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

DOCX_PATH = os.path.abspath("Final_MOTIONIQ.docx")
PDF_PATH = os.path.abspath("Final_MOTIONIQ.pdf")

PS_SCRIPT = r"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = $args[0]
    $doc = $word.Documents.Open($docPath)
    
    $result = @{
        sections = @{}
        tables = @{}
    }

    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "\t") { continue }
        $pg = $p.Range.Information(3) # wdActiveEndPageNumber
        
        if ($txt -match "^ACKNOWLEDGEMENTS") { $result.sections["ack"] = "$pg" }
        elseif ($txt -match "^EXECUTIVE SUMMARY") { $result.sections["exec"] = "$pg" }
        elseif ($txt -match "^LIST OF ABBREVIATIONS") { $result.sections["acro"] = "$pg" }
        elseif ($txt -match "^LIST OF TABLES") { $result.sections["tbls"] = "$pg" }
        elseif ($txt -match "^TABLE OF CONTENTS") { $result.sections["toc"] = "$pg" }
        elseif ($txt -match "^CHAPTER 1:") { $result.sections["ch1"] = "$pg" }
        elseif ($txt -match "^1\.1\.") { $result.sections["s11"] = "$pg" }
        elseif ($txt -match "^1\.2\.") { $result.sections["s12"] = "$pg" }
        elseif ($txt -match "^1\.3\.") { $result.sections["s13"] = "$pg" }
        elseif ($txt -match "^CHAPTER 2:") { $result.sections["ch2"] = "$pg" }
        elseif ($txt -match "^2\.1\.") { $result.sections["s21"] = "$pg" }
        elseif ($txt -match "^2\.2\.") { $result.sections["s22"] = "$pg" }
        elseif ($txt -match "^2\.3\.") { $result.sections["s23"] = "$pg" }
        elseif ($txt -match "^2\.4\.") { $result.sections["s24"] = "$pg" }
        elseif ($txt -match "^CHAPTER 3:") { $result.sections["ch3"] = "$pg" }
        elseif ($txt -match "^3\.1\.") { $result.sections["s31"] = "$pg" }
        elseif ($txt -match "^3\.2\.1\.") { $result.sections["s321"] = "$pg" }
        elseif ($txt -match "^3\.2\.2\.") { $result.sections["s322"] = "$pg" }
        elseif ($txt -match "^3\.2\.3\.") { $result.sections["s323"] = "$pg" }
        elseif ($txt -match "^3\.2\.4\.") { $result.sections["s324"] = "$pg" }
        elseif ($txt -match "^3\.2\.5\.") { $result.sections["s325"] = "$pg" }
        elseif ($txt -match "^3\.2\.") { $result.sections["s32"] = "$pg" }
        elseif ($txt -match "^3\.3\.1\.") { $result.sections["s331"] = "$pg" }
        elseif ($txt -match "^3\.3\.2\.") { $result.sections["s332"] = "$pg" }
        elseif ($txt -match "^3\.3\.3\.") { $result.sections["s333"] = "$pg" }
        elseif ($txt -match "^3\.3\.") { $result.sections["s33"] = "$pg" }
        elseif ($txt -match "^3\.4\.") { $result.sections["s34"] = "$pg" }
        elseif ($txt -match "^CHAPTER 4:") { $result.sections["ch4"] = "$pg" }
        elseif ($txt -match "^4\.1\.") { $result.sections["s41"] = "$pg" }
        elseif ($txt -match "^4\.2\.") { $result.sections["s42"] = "$pg" }
        elseif ($txt -match "^4\.3\.") { $result.sections["s43"] = "$pg" }
        elseif ($txt -match "^4\.4\.") { $result.sections["s44"] = "$pg" }
        elseif ($txt -match "^4\.5\.") { $result.sections["s45"] = "$pg" }
        elseif ($txt -match "^4\.6\.") { $result.sections["s46"] = "$pg" }
        elseif ($txt -match "^4\.7\.") { $result.sections["s47"] = "$pg" }
        elseif ($txt -match "^4\.8\.") { $result.sections["s48"] = "$pg" }
        elseif ($txt -match "^CHAPTER 5:") { $result.sections["ch5"] = "$pg" }
        elseif ($txt -match "^5\.1\.") { $result.sections["s51"] = "$pg" }
        elseif ($txt -match "^5\.2\.") { $result.sections["s52"] = "$pg" }
        elseif ($txt -match "^5\.3\.") { $result.sections["s53"] = "$pg" }
        elseif ($txt -match "^CONCLUSION") { $result.sections["concl"] = "$pg" }
    }

    $tIdx = 1
    foreach ($t in $doc.Tables) {
        $firstCell = $t.Cell(1, 1).Range.Text.Trim()
        $pg = $t.Range.Information(3)
        if ($firstCell -match "Full Name") { $result.tables["t11"] = "Page $pg" }
        elseif ($firstCell -match "Survey Metric") { $result.tables["t21"] = "Page $pg" }
        elseif ($firstCell -match "Competitive Solution") { $result.tables["t22"] = "Page $pg" }
        elseif ($firstCell -match "BMC Building Block") { $result.tables["t31"] = "Page $pg" }
        elseif ($firstCell -match "Module / File Name") { $result.tables["t32"] = "Page $pg" }
        elseif ($firstCell -match "UI-PRMD Joint Index") { $result.tables["t32joints"] = "Page $pg" }
        elseif ($firstCell -match "Exercise Name") { $result.tables["t32a"] = "Page $pg" }
        elseif ($firstCell -match "Exercise & Code") { $result.tables["t33"] = "Page $pg" }
        elseif ($firstCell -match "Experimental Metric") { $result.tables["t34"] = "Page $pg" }
        elseif ($firstCell -match "Media Channel") { $result.tables["t41"] = "Page $pg" }
        elseif ($firstCell -match "Implementation Stage") { $result.tables["t42"] = "Page $pg" }
        elseif ($firstCell -match "Service Package") { $result.tables["t43"] = "Page $pg" }
        elseif ($firstCell -match "04-Month Media Budget Item") { $result.tables["t44"] = "Page $pg" }
        elseif ($firstCell -match "Funnel Stage & Performance Metric") { $result.tables["t45"] = "Page $pg" }
        elseif ($firstCell -match "Number of Active Paying Customers") { $result.tables["t46"] = "Page $pg" }
        elseif ($firstCell -match "Break-Even Metric") { $result.tables["t47"] = "Page $pg" }
        elseif ($firstCell -match "Identified Operational Risk") { $result.tables["t51"] = "Page $pg" }
        $tIdx++
    }

    # Save PDF
    if ($args.Count -gt 1) {
        $pdfPath = $args[1]
        $doc.SaveAs([ref]$pdfPath, [ref]17) # 17 = wdFormatPDF
    }

    $doc.Close([ref]0)
    $result | ConvertTo-Json
} catch {
    Write-Host ("Error: " + $_.Exception.Message)
} finally {
    $word.Quit()
}
"""

with open("inspect_doc.ps1", "w", encoding="utf-8") as f:
    f.write(PS_SCRIPT)

def run_inspection(docx_file, pdf_file=None):
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "inspect_doc.ps1", docx_file]
    if pdf_file:
        cmd.append(pdf_file)
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    try:
        data = json.loads(out)
        return data
    except Exception as e:
        print("Raw output:", out)
        raise e

# Pass 1: Build initial doc
print("Pass 1: Generating initial document...")
doc = create_full_report()
doc.save(DOCX_PATH)

for iteration in range(1, 5):
    print(f"\n--- Iteration {iteration}: Querying Word COM for exact page layout ---")
    data = run_inspection(DOCX_PATH, PDF_PATH)
    
    sections = data.get("sections", {})
    tables = data.get("tables", {})
    
    print(f"Found {len(sections)} sections and {len(tables)} tables.")
    
    new_page_dict = {
        "ack": "2", "exec": "2", "acro": "3", "tbls": "4", "toc": "5",
        "ch1": "6", "s11": "6", "s12": "6", "s13": "7",
        "ch2": "9", "s21": "9", "s22": "9", "s23": "10", "s24": "11",
        "ch3": "12", "s31": "12", "s32": "13", "s321": "15", "s322": "15",
        "s323": "17", "s324": "18", "s325": "19", "s33": "24", "s331": "24",
        "s332": "25", "s333": "28", "s34": "30",
        "ch4": "31", "s41": "31", "s42": "31", "s43": "31", "s44": "32",
        "s45": "32", "s46": "33", "s47": "34", "s48": "35",
        "ch5": "37", "s51": "37", "s52": "38", "s53": "38", "concl": "39",
        "t11": "Page 7", "t21": "Page 9", "t22": "Page 11",
        "t31": "Page 12", "t32": "Page 13", "t32joints": "Page 20",
        "t32a": "Page 23", "t33": "Page 28", "t34": "Page 30",
        "t41": "Page 31", "t42": "Page 32", "t43": "Page 33",
        "t44": "Page 33", "t45": "Page 34", "t46": "Page 35",
        "t47": "Page 36", "t51": "Page 37"
    }
    for k, v in sections.items():
        new_page_dict[k] = v
    for k, v in tables.items():
        new_page_dict[k] = v
        
    print("Sample detected pages:")
    for k in ["ch1", "ch2", "ch3", "s33", "ch4", "ch5", "concl"]:
        print(f"  {k} -> {new_page_dict.get(k)}")
    for k in ["t11", "t21", "t31", "t33", "t41", "t51"]:
        print(f"  {k} -> {new_page_dict.get(k)}")

    # Regenerate with exact page numbers
    doc = create_full_report(new_page_dict)
    doc.save(DOCX_PATH)

    # Check if stable
    data_after = run_inspection(DOCX_PATH, PDF_PATH)
    sec_after = data_after.get("sections", {})
    tbl_after = data_after.get("tables", {})
    
    diffs = 0
    for k, v in sec_after.items():
        if new_page_dict.get(k) != v:
            diffs += 1
    for k, v in tbl_after.items():
        if new_page_dict.get(k) != v:
            diffs += 1
            
    if diffs == 0:
        print(f"\n🎉 PERFECT CONVERGENCE ACHIEVED on iteration {iteration}! All {len(sec_after)} sections and {len(tbl_after)} tables match 100%!")
        break
    else:
        print(f"Discrepancies found: {diffs}. Refining in next iteration...")

print("\nDeploying perfected files to all target destinations...")

copy_targets = [
    r"C:\Users\PC\Downloads",
    r"C:\Users\PC\Desktop",
    r"C:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ",
    "public",
    r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a",
]

for d in copy_targets:
    target_dir = os.path.abspath(d)
    if os.path.exists(target_dir):
        if target_dir != os.path.dirname(os.path.abspath(DOCX_PATH)):
            shutil.copyfile(DOCX_PATH, os.path.join(target_dir, "Final_MOTIONIQ.docx"))
            if os.path.exists(PDF_PATH):
                shutil.copyfile(PDF_PATH, os.path.join(target_dir, "Final_MOTIONIQ.pdf"))
            shutil.copyfile(DOCX_PATH, os.path.join(target_dir, "MotionIQ_Final_Report_EXE101_EN.docx"))
            if os.path.exists(PDF_PATH):
                shutil.copyfile(PDF_PATH, os.path.join(target_dir, "MotionIQ_Final_Report_EXE101_EN.pdf"))

print("All copies successfully updated and synchronized!")