# -*- coding: utf-8 -*-
"""
Full Academic English Report Generator for MotionIQ (EXE101 - FPT University Can Tho)
Course: EXE101 — Experiential Entrepreneurship
Instructor: Mr. Tran Ngoc Son
Project: MotionIQ — 100% On-Device AI Motion Tracking Platform for Elderly Home Care
Founding Team (Group K19):
  1. Huỳnh Thị Yến Duy (CEO & Project Lead — CE191522)
  2. Nguyễn Hải Hà (CTO — CE200298)
  3. Nguyễn Nhã Quân (CPO — CE200197)
  4. Đặng Vĩnh Phúc (Market & Language — CE190510)
  5. Mã Phú Tín (Growth & Media — CS191066)
  6. Hồ Tuyết Nghi (CMO — CS180758)
"""

import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=90, bottom=90, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D4C5B9", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_table(table, col_widths, data, header_bg="EAE0D5", font_size=10, bold_col0=False):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="D4C5B9", sz="4")
    
    for r_idx, row in enumerate(table.rows):
        make_row_cant_split(row)
        if r_idx == 0:
            make_row_header(row)
            
        for c_idx, val in enumerate(data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=110, right=110)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, header_bg)
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if bold_col0 and c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(140, 47, 30)

def add_p(doc, text="", space_before=0, space_after=6, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=13, color=(30, 30, 30)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.font.color.rgb = RGBColor(*color)
    return p

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(15.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(140, 47, 30)
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(178, 66, 45)
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(60, 60, 60)
    return p

def add_equation_box(doc, equation_text, explanation_text=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.3)
    set_cell_background(cell, "FBF8F5")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="B2422D"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    make_row_cant_split(tbl.rows[0])
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_eq = p.add_run(equation_text)
    r_eq.bold = True
    r_eq.font.name = "Times New Roman"
    r_eq.font.size = Pt(11)
    r_eq.font.color.rgb = RGBColor(140, 47, 30)
    
    if explanation_text:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.line_spacing = 1.15
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_exp = p2.add_run(explanation_text)
        r_exp.font.name = "Times New Roman"
        r_exp.font.size = Pt(10)
        r_exp.font.italic = True
        r_exp.font.color.rgb = RGBColor(60, 60, 60)
        
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(2)

def add_callout_box(doc, text, title="STRATEGIC FINANCIAL TAKEAWAY & OPERATIONAL SELF-SUFFICIENCY"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.3)
    set_cell_background(cell, "FBF8F5")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="B2422D"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    make_row_cant_split(tbl.rows[0])
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r_title = p.add_run(f"📌 {title}\n")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11.5)
    r_title.font.color.rgb = RGBColor(178, 66, 45)
    
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(11)
    r_body.font.italic = True
    r_body.font.color.rgb = RGBColor(50, 50, 50)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(2)

def add_toc_line(doc, title, page_str, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    
    indent = Inches(0.25 * (level - 1))
    p.paragraph_format.left_indent = indent
    
    r_text = p.add_run(title)
    r_text.font.name = "Times New Roman"
    if level == 1:
        r_text.font.size = Pt(11.5)
        r_text.font.bold = True
        r_text.font.color.rgb = RGBColor(140, 47, 30)
    else:
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(40, 40, 40)
        
    r_tab = p.add_run(f"\t{page_str}")
    r_tab.font.name = "Times New Roman"
    r_tab.font.size = Pt(11)
    r_tab.font.color.rgb = RGBColor(90, 90, 90)

def build_docx(out_path):
    doc = Document()

    # 1. Page Margins & Header/Footer
    for section in doc.sections:
        section.top_margin = Inches(0.75)     # ~1.9 cm
        section.bottom_margin = Inches(0.75)  # ~1.9 cm
        section.left_margin = Inches(1.15)   # ~2.9 cm
        section.right_margin = Inches(0.75)   # ~1.9 cm
        section.different_first_page_header_footer = True

        # Clear first page header and footer
        for p in section.first_page_header.paragraphs:
            p.text = ""
        for p in section.first_page_footer.paragraphs:
            p.text = ""

        # Regular header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hr = hp.add_run("MOTIONIQ — Comprehensive Entrepreneurship Project Report (Course EXE101)")
        hr.font.name = "Times New Roman"
        hr.font.size = Pt(9)
        hr.font.italic = True
        hr.font.color.rgb = RGBColor(120, 120, 120)

        # Regular footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fr = fp.add_run("FPT University Can Tho Campus   |   Page ")
        fr.font.name = "Times New Roman"
        fr.font.size = Pt(9.5)
        fr.font.color.rgb = RGBColor(100, 100, 100)
        
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        fp._p.append(fldSimple)

    # 2. Typography Normal Style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(13)
    font_normal.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # COVER PAGE (PAGE 1)
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("MINISTRY OF EDUCATION AND TRAINING\nFPT UNIVERSITY CAN THO CAMPUS\n")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(70, 70, 70)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(8)
    r_line = p_line.add_run("———————————————***———————————————")
    r_line.font.bold = True
    r_line.font.color.rgb = RGBColor(178, 66, 45)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(8)
    r_course = p_course.add_run("STARTUP PROJECT FINAL REPORT (FINAL REPORT)\nCOURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP")
    r_course.font.name = "Times New Roman"
    r_course.font.size = Pt(12.5)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(178, 66, 45)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(4)
    p_proj.paragraph_format.space_after = Pt(8)
    r_proj = p_proj.add_run("MOTIONIQ — AI ASSISTANT PLATFORM SUPPORTING HOME EXERCISE TRACKING FOR THE ELDERLY\n(100% ON-DEVICE AI)")
    r_proj.font.name = "Times New Roman"
    r_proj.font.size = Pt(15.5)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(140, 47, 30)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run(
        '"MotionIQ – Home exercise, movement tracking made easier."\n'
        'MotionIQ — Home Physical Movement Tracking AI Assistant for the Elderly via Standard Smartphone Cameras. '
        'Real-time posture tracking, repetition counting, and immediate audio guidance.'
    )
    r_sub.font.name = "Times New Roman"
    r_sub.font.italic = True
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(90, 90, 90)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(10)
    r_meta = p_meta.add_run(
        "Instructor: Mr. Tran Ngoc Son\n"
        "Student Group Name: MOTIONIQ — Group K19\n"
        "Website Demo MVP: https://motion-iq-five.vercel.app"
    )
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(10.5)
    r_meta.font.color.rgb = RGBColor(60, 60, 60)

    # 3-column table matching official final report
    t_cover = doc.add_table(rows=7, cols=3)
    cover_widths = [Inches(2.5), Inches(2.2), Inches(1.6)]
    cover_data = [
        ("NAME", "STUDENT ID", "CONTRIBUTION"),
        ("Huỳnh Thị Yến Duy", "CE191522", "100%"),
        ("Nguyễn Hải Hà", "CE200298", "100%"),
        ("Nguyễn Nhã Quân", "CE200197", "100%"),
        ("Đặng Vĩnh Phúc", "CE190510", "100%"),
        ("Mã Phú Tín", "CS191066", "100%"),
        ("Hồ Tuyết Nghi", "CS180758", "100%")
    ]
    format_table(t_cover, cover_widths, cover_data, font_size=10, bold_col0=True)

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(14)
    p_bottom.paragraph_format.space_after = Pt(0)
    r_bot = p_bottom.add_run("CAN THO CITY, NOVEMBER 2026")
    r_bot.font.name = "Times New Roman"
    r_bot.font.bold = True
    r_bot.font.size = Pt(11)
    r_bot.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # ACKNOWLEDGEMENTS & EXECUTIVE SUMMARY (PAGE 2)
    # ==========================================
    add_h1(doc, "ACKNOWLEDGEMENTS")
    add_p(
        doc,
        "The MotionIQ project team would like to express our deepest gratitude and most sincere thanks to Mr. Tran Ngoc Son, "
        "who has dedicatedly imparted knowledge on innovative startup thinking, business model methodologies, and patiently "
        "guided us, providing invaluable professional feedback through each milestone: Checkpoint 1, Checkpoint 2, and "
        "Checkpoint 3 of the EXE101 course (Startup Experience)."
    )
    add_p(
        doc,
        "The team also wants to sincerely thank the elderly individuals and relatives across Can Tho City and the Mekong Delta "
        "who enthusiastically participated in our 50 quantitative survey responses as well as 5 direct prototype testing sessions "
        "of the application. Practical feedback from actual users is the guiding light that helps the team perfect the MotionIQ "
        "product to be the most useful, accessible, and humane."
    )

    add_h1(doc, "EXECUTIVE SUMMARY")
    add_p(
        doc,
        "MotionIQ is a technology solution applying Artificial Intelligence and computer vision running directly on mobile devices "
        "(100% On-Device AI), supporting the elderly to track their workout progress and balance training at home via a smartphone "
        "or laptop camera without investing in expensive additional hardware sensor equipment."
    )
    add_p(
        doc,
        "By flexibly combining the virtual assistant character 'Be Nam' with Vietnamese voice count reminders, a pose recognition "
        "model based on published benchmark motion datasets (UI-PRMD, KIMORE, EHE), and the One-Euro Filter noise reduction filter, "
        "MotionIQ helps seniors maintain proper workout habits, count repetitions, and provide basic feedback. Actual survey results "
        "on 50 subjects show that more than 68% of children face difficulties when directly observing their parents working out, "
        "and 82.4% are ready to let their relatives try the application. Practical testing through 5 sessions achieved a range of "
        "motion (ROM) angle measurement index of 94.6% compared to the reference measurement angle and an outstanding SUS system "
        "usability score of 84.5 / 100 (Grade A / Excellent level)."
    )
    add_p(
        doc,
        "Regarding business and financial strategy, the team applies a customer value-based pricing method and competitor comparison "
        "with an Early Access trial package of 49,000 VND / month (~1,600 VND/day), combined with a concise 4-month communication "
        "plan with a student budget of 10,000,000 VND. Break-even analysis shows that with 26 paying customers for the Early Access "
        "package or 15 customers for the Standard package (79,000 VND/month), the project will self-cover its fixed monthly operating "
        "costs (1,000,000 VND/month), achieving operational self-sufficiency without requiring founder out-of-pocket subsidies."
    )

    doc.add_page_break()

    # ==========================================
    # LIST OF ABBREVIATIONS & LIST OF TABLES (PAGE 3)
    # ==========================================
    add_h1(doc, "LIST OF ABBREVIATIONS")
    t_acro = doc.add_table(rows=8, cols=3)
    acro_widths = [Inches(1.5), Inches(2.4), Inches(2.4)]
    acro_data = [
        ("Abbreviation", "English Term", "Vietnamese Meaning"),
        ("AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"),
        ("BMC", "Business Model Canvas", "Khung Mô hình Kinh doanh 9 Khối"),
        ("ROM", "Range of Motion", "Biên độ góc vận động của khớp"),
        ("CAC", "Customer Acquisition Cost", "Chi phí thu hút một khách hàng mới"),
        ("MRR", "Monthly Recurring Revenue", "Doanh thu định kỳ hằng tháng"),
        ("SUS", "System Usability Scale", "Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế)"),
        ("On-Device AI", "On-Device Artificial Intelligence", "Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị (Edge AI)")
    ]
    format_table(t_acro, acro_widths, acro_data, font_size=10, bold_col0=True)

    add_h1(doc, "LIST OF TABLES")
    add_p(doc, "List of tables summarizing experimental data, source code algorithms, financials, and operational plans:", italic=True, font_size=11, color=(100, 100, 100))
    
    list_tables = [
        ("Table 1.1", "Founding Team Competency Profiles & RACI Governance Matrix", "Page 7"),
        ("Table 2.1", "Quantitative Field Survey Findings & Statistical Breakdown (N = 50)", "Page 9"),
        ("Table 2.2", "Competitive Landscape Analysis & Strategic Positioning Differentiation", "Page 11"),
        ("Table 3.1", "9-Block Business Model Canvas (BMC) Framework", "Page 12"),
        ("Table 3.2", "Profile of Model Files and Core Algorithms in Project Source Code", "Page 13"),
        ("Table 3.2-Joints", "22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics", "Page 20"),
        ("Table 3.2a", "Actual Parameters Extracted from Weights File uiprmdQualityModel.json", "Page 23"),
        ("Table 3.3", "Summary Table of 4 Standardized Functional Exercises in MotionIQ", "Page 28"),
        ("Table 3.4", "Results of 5 Actual MVP Prototype Testing Sessions", "Page 30"),
        ("Table 4.1", "Communication Channels & Operational Implementation Methods", "Page 31"),
        ("Table 4.2", "4-Month Communication Implementation Roadmap", "Page 32"),
        ("Table 4.3", "Proposed Pricing Structure of MotionIQ", "Page 33"),
        ("Table 4.4", "4-Month Lean Student Media Budget Allocation (10,000,000 VND)", "Page 33"),
        ("Table 4.5", "Target Customer Segments & 4-Month Conversion Funnel KPIs", "Page 34"),
        ("Table 4.6", "Early Access Tier Subscription Monthly Revenue Forecast", "Page 35"),
        ("Table 4.7", "Operational Break-Even vs. Full Capital Recovery Analysis", "Page 36"),
        ("Table 5.1", "Identified Operational Risk Matrix & Concrete Mitigation Strategies", "Page 37")
    ]

    for tb_id, tb_title, tb_pg in list_tables:
        p_tb = doc.add_paragraph()
        p_tb.paragraph_format.space_before = Pt(2)
        p_tb.paragraph_format.space_after = Pt(2)
        p_tb.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_tb.add_run(f"{tb_id}: {tb_title}")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        
        r2 = p_tb.add_run(f"\t{tb_pg}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # TABLE OF CONTENTS (PAGE 4)
    # ==========================================
    add_h1(doc, "TABLE OF CONTENTS")
    add_p(doc, "(Hierarchical Table of Contents with Academic Chapter Structure and Section Lead Authors)", italic=True, font_size=11, color=(100, 100, 100))

    toc_items = [
        ("ACKNOWLEDGEMENTS", "2", 1),
        ("EXECUTIVE SUMMARY", "2", 1),
        ("LIST OF ABBREVIATIONS", "3", 1),
        ("LIST OF TABLES", "3", 1),
        ("CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (Lead: Huỳnh Thị Yến Duy)", "6", 1),
        ("1.1. Context of MotionIQ Idea Formation", "6", 2),
        ("1.2. Mission, Vision, and Core Values", "6", 2),
        ("1.3. Founding Team Capability Profiles & RACI Governance Matrix", "7", 2),
        ("CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (Leads: Nguyễn Nhã Quân, Đặng Vĩnh Phúc)", "9", 1),
        ("2.1. Methodology and Field Survey Scale (N = 50)", "9", 2),
        ("2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)", "9", 2),
        ("2.3. Target Customer Persona & Empathy Mapping", "10", 2),
        ("2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation", "11", 2),
        ("CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (Leads: Nguyễn Hải Hà, Nguyễn Nhã Quân)", "12", 1),
        ("3.1. 9-Block Business Model Canvas (BMC) Framework", "12", 2),
        ("3.2. Profile of Model Files and Algorithms in Project Source Code", "13", 2),
        ("3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline", "15", 2),
        ("3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)", "15", 2),
        ("3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer", "17", 2),
        ("3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine", "18", 2),
        ("3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset", "19", 2),
        ("3.3. 4 Standardized Functional Exercise Movements", "24", 2),
        ("3.3.1. Principles of Exercise Standardization Based on 3 International Datasets", "24", 2),
        ("3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises", "25", 2),
        ("3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ", "28", 2),
        ("3.4. Results of 5 Actual MVP Prototype Testing Sessions", "30", 2),
        ("CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (Lead: Mã Phú Tín)", "31", 1),
        ("4.1. 04-Month Media Objectives", "31", 2),
        ("4.2. Target Customers & Key Message", "31", 2),
        ("4.3. Communication Channels & Methods", "31", 2),
        ("4.4. 04-Month Media Implementation Roadmap", "32", 2),
        ("4.5. Value-Based & Competitive Parity Pricing Strategy", "32", 2),
        ("4.6. Budget Estimation and Operating Costs", "33", 2),
        ("4.7. Revenue Development Plan & KPI Targets after 04 Months", "34", 2),
        ("4.8. Revenue Forecast and Break-Even Analysis", "35", 2),
        ("CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY (Lead: Hồ Tuyết Nghi)", "37", 1),
        ("5.1. Identification of Practical Risks & Mitigation Measures", "37", 2),
        ("5.2. Development and Sustainability Plan by Phase", "38", 2),
        ("5.3. Project Limitations and Future Technological Roadmap", "38", 2),
        ("CONCLUSION (Lead: Huỳnh Thị Yến Duy)", "39", 1)
    ]

    for title, pg, lvl in toc_items:
        add_toc_line(doc, title, pg, lvl)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1 (PAGE 6)
    # ==========================================
    add_h1(doc, "CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (CHECKPOINT 1)")
    add_p(doc, "[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "1.1. Context of MotionIQ Idea Formation")
    add_p(
        doc,
        "Vietnam is currently one of the fastest aging populations in the world. According to the General Statistics Office (GSO), "
        "the number of people aged 60 and above has exceeded 13.5 million (accounting for 13.5% of the total population). Along with "
        "the natural aging process, the elderly often face musculoskeletal degeneration, sarcopenia (age-related muscle loss), knee "
        "and spinal osteoarthritis, and decreased balance capability, dramatically elevating the risk of falls and severe daily activity limitations."
    )
    add_p(
        doc,
        "Maintaining gentle home exercise habits plays an indispensable role in improving flexibility, cardiorespiratory endurance, and "
        "physical health. However, most seniors exercise based purely on habit or unguided memory without knowing if their posture is "
        "correct or incorrect. Meanwhile, busy working children face immense workplace pressures and economic demands, leaving them with "
        "very limited time to directly supervise or remind their aging parents. Stemming from the practical need to care for family relatives, "
        "the MotionIQ founding team (Group K19) developed the MotionIQ project — a vision AI technology platform operating directly on smartphones "
        "and laptops to serve as an intelligent, empathetic home exercise companion supporting movement tracking, repetition counting, and "
        "real-time feedback for the elderly right at home."
    )

    add_h2(doc, "1.2. Mission, Vision, and Core Values")
    add_p(
        doc,
        "• Mission: 'Popularizing quality physical exercise support services to every Vietnamese household' — bringing autonomous mobility, "
        "minimizing fall risks for the elderly, and giving children complete peace of mind when working far away."
    )
    add_p(
        doc,
        "• Vision: Becoming the premier personal movement tracking and functional mobility digital platform in Vietnam by 2027."
    )
    add_p(
        doc,
        "• Core Values:\n"
        "1. Safety & Evidence-based: All exercise routines are built upon standardized functional movement benchmarks from prestigious public "
        "biomechanical research datasets (UI-PRMD, KIMORE, EHE).\n"
        "2. Privacy by Design: 100% local AI processing on the user's personal device RAM, strictly saying NO to storing or transmitting personal "
        "images/videos to cloud servers.\n"
        "3. Geriatric Empathy: High-contrast interface, large readable text (font size ≥ 18px), large tactile touch buttons (≥ 56px), and encouraging "
        "seniors with the warmth, patience, and natural voice of the Bé Nấm virtual mascot."
    )

    add_h2(doc, "1.3. Founding Team Capability Profile (Founding Team & RACI)")
    add_p(
        doc,
        "The founding team of MotionIQ (MOTIONIQ — Group K19) represents a synergistic, interdisciplinary collaboration between Information "
        "Technology (Information Security), Graphic Design / UI-UX, Multimedia Communication, Foreign Languages, and Service Management majors, "
        "creating distinct practical execution advantages across all project facets:"
    )

    # Table 1.1
    t_team = doc.add_table(rows=7, cols=5)
    team_widths = [Inches(1.2), Inches(0.9), Inches(1.1), Inches(1.5), Inches(1.6)]
    team_data = [
        ("Full Name", "Role", "Major", "Assigned Chapter in Report", "Main Responsibility (RACI)"),
        ("Huỳnh Thị Yến Duy", "Team Leader (CEO)", "Information Security", "Chapter 1 (Whole), Introduction, Conclusion & General Review", "Accountable (A): Fully responsible for web/app technical architecture, MediaPipe Pose integration, and overall project governance."),
        ("Nguyễn Nhã Quân", "Member (CPO)", "UI-UX Design", "Chapter 2 (Section 2.1, 2.2: Survey) & Chapter 3 (Section 3.4: MVP Testing)", "Responsible (R): Analyzing Google Sheets survey data, designing Geriatric UI design system, and executing live MVP testing (ROM 94.6%, SUS 84.5)."),
        ("Đặng Vĩnh Phúc", "Member", "Foreign Language", "Chapter 2 (Section 2.3 & 2.4: Customers & 4 Competitors)", "Responsible (R): Comprehensive competitor landscape research, international literature review, English documentation, and local community outreach."),
        ("Nguyễn Hải Hà", "Member (CTO)", "Information Security", "Chapter 3 (Section 3.2: On-Device AI & Section 3.3: 4 Exercises)", "Responsible (R): On-Device AI engine, UI-PRMD dataset preprocessing, One-Euro jitter-filtering algorithm, and client-side RAM security."),
        ("Mã Phú Tín", "Member", "Multimedia Communication", "Chapter 4 (Whole Section 4.1 – 4.8: Media Plan & Financials)", "Responsible (R): Multi-channel TikTok/Facebook communication plan, 49k pricing strategy, 10 million lean budget, conversion KPIs, and break-even modeling."),
        ("Hồ Tuyết Nghi", "Member (CMO)", "Service Management", "Chapter 5 (Whole Section 5.1 & 5.2: Risk Management & Sustainability)", "Responsible (R): Operational risk identification, legal non-medical disclaimer positioning, Zalo Mini App expansion roadmap, and long-term service sustainability.")
    ]
    format_table(t_team, team_widths, team_data, font_size=9.5, bold_col0=True)

    add_callout_box(
        doc,
        "The synergy between AI technical expertise and human-centered design enables MotionIQ to directly address elderly physical wellness "
        "needs without requiring expensive wearable sensors or specialized hardware.\n"
        "NON-MEDICAL DISCLAIMER: MotionIQ is strictly an assistive physical wellness support tool for home exercise tracking. It is NOT a medical device, "
        "does not provide clinical diagnosis, and does not replace professional physical therapists or medical specialists.",
        title="TEAM STRENGTHS & ASSISTIVE SAFETY POSITIONING PRINCIPLES"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2 (PAGE 9)
    # ==========================================
    add_h1(doc, "CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Nhã Quân (2.1, 2.2) & Đặng Vĩnh Phúc (2.3, 2.4)]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "2.1. Methodology and Field Survey Scale (N = 50)")
    add_p(
        doc,
        "To empirically validate the problem hypotheses and quantify genuine market demand during Checkpoint 2, the team conducted a rigorous "
        "field survey of 50 target respondents via structured questionnaires (data stored publicly on Google Sheets: "
        "https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM):\n"
        "• Survey demographic breakdown: 81.6% aged 18–23 years old and 18.4% aged 23–30 years old (representing adult children and grandchildren caring for older relatives).\n"
        "• Family caregiving experience: 65.3% indicated that within the past year they have directly cared for or supported elderly relatives in daily living or mobility.\n"
        "• Age bracket of relatives needing exercise support: 28.6% aged 60–69; 24.5% aged 70–79; 10.2% aged 80 and above (total 63.3% relatives aged 60+), and 24.5% aged 50–59."
    )

    add_h2(doc, "2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)")
    
    t_survey = doc.add_table(rows=7, cols=3)
    survey_widths = [Inches(3.2), Inches(1.1), Inches(2.0)]
    survey_data = [
        ("Actual Survey Metric (Google Sheets N = 50)", "Actual Rate", "MotionIQ Development Implication"),
        ("Children cannot regularly observe and correct movements for elderly parents", "68.6%", "Seniors frequently exercise alone; automated AI tracking is essential."),
        ("Elderly relatives exercise daily or 3–5 times per week", "51.0%", "Home exercise demand is continuous and recurring, requiring an accessible home tool."),
        ("Biggest difficulty: Not knowing if exercising correctly / incorrectly, no feedback or warnings", "82.4%", "AI must deliver real-time repetition counting and auditory posture correction."),
        ("Top 3 most important factors: Ease of use, Correct / Incorrect feedback, Movement guidance", "88.2%", "Mandatory Geriatric UI design: large text, large buttons, one-touch start."),
        ("Suitability level of MotionIQ concept with household demand (Rated 4 – 5 stars)", "66.7%", "High product-market alignment; confirms core value proposition."),
        ("Willingness to let relatives trial MotionIQ (Rated 4 – 5 stars)", "82.4%", "Outstanding trial adoption potential; establishes initial user acquisition pool.")
    ]
    format_table(t_survey, survey_widths, survey_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "When specifically surveyed regarding their primary concerns when using camera-based AI applications (Question 14 in the survey form), respondents highlighted:\n"
        "1. Personal image privacy and living space exposure (expressed by 45.0% of respondents).\n"
        "2. Elderly relatives struggling to operate complex modern technology devices (50.0%).\n"
        "3. AI recognition errors caused by slow movements or age-related limb tremors (40.0%).\n\n"
        "These empirical findings directly guided the foundational technical design of MotionIQ:\n"
        "• Complete elimination of privacy concerns via 100% On-Device AI: Video streams are processed strictly in local browser RAM without cloud transmission.\n"
        "• Elimination of usability anxiety via Geriatric UI: Font sizes ≥ 18px, touch buttons ≥ 56px, and empathetic Vietnamese voice guidance from Bé Nấm.\n"
        "• Noise-robust tracking via adaptive One-Euro Filter: Eliminates physiological tremors, ensuring stable kinematic angle measurement."
    )

    add_h2(doc, "2.3. Target Customer Persona & Empathy Mapping")
    add_p(
        doc,
        "MotionIQ operates on a dual-customer architecture (Dual-Customer Profile) consisting of the Primary End-User (the elderly parent) and the Economic Buyer / Payer (the adult child):"
    )
    add_p(
        doc,
        "• Persona 1 — Direct User: Mr. Nguyen Van An, 68 years old, retired civil servant living in Ninh Kieu, Can Tho City. "
        "Needs daily knee and leg mobility exercises to walk steadily and prevent joint stiffness. He has declining eyesight, fears troubling his busy children, "
        "and feels frustrated when exercising alone from memory without knowing if his posture is correct or risking joint injury.\n"
        "• Persona 2 — Economic Buyer (Payer): Ms. Thu Hang, 36 years old, corporate office worker in Can Tho. She cares deeply about her father's longevity "
        "but works long hours, feeling persistent guilt and anxiety when she cannot be home to supervise his workouts. She readily embraces spending a modest monthly "
        "subscription (under 100,000 VND/month) to equip her father with an easy-to-use digital companion that provides structured movement safety."
    )

    add_h2(doc, "2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation")
    add_p(
        doc,
        "To evaluate competitive dynamics, MotionIQ benchmarked four prevalent alternatives currently available in the Vietnamese market:"
    )

    t_comp = doc.add_table(rows=5, cols=4)
    comp_widths = [Inches(1.5), Inches(1.4), Inches(1.8), Inches(1.6)]
    comp_data = [
        ("Competitive Solution", "Key Advantages", "Real-World Limitations", "MotionIQ Positioning Advantage"),
        ("Self-practice via YouTube / TV", "Completely free, diverse video library", "Zero interaction, no posture correction, high injury risk from unguided imitation", "Real-time AI posture feedback, rep counting, and voice correction directly via phone camera"),
        ("Hiring an at-home Personal Trainer", "1-on-1 close supervision, personalized motivation", "Very high cost (200k–400k VND/session, 2–4m VND/month); unsustainable for average families", "Extremely accessible pricing (49k–79k VND/month); practice anytime in the living room"),
        ("Senior Fitness / Retirement Clubs", "Social community interaction, peer encouragement", "Requires physical travel; challenging for seniors with joint pain; weather-dependent", "Safe, independent home workouts without commuting; complete schedule autonomy"),
        ("International Fitness Apps (Freeletics, etc.)", "Modern digital interface, extensive workout routines", "English-only; high intensity designed for athletic youth; expensive subscription (>150k/mo)", "100% localized in Vietnamese; customized for geriatric functional mobility; friendly mascot")
    ]
    format_table(t_comp, comp_widths, comp_data, font_size=9.5, bold_col0=True)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3 (PAGE 12)
    # ==========================================
    add_h1(doc, "CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Hải Hà (3.2, 3.3) & Nguyễn Nhã Quân (3.1, 3.4)]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "3.1. 9-Block Business Model Canvas (BMC) Framework")
    add_p(
        doc,
        "MotionIQ's business model is structured following Alexander Osterwalder's standard 9-Block Canvas, tailored specifically to the operational "
        "and resource realities of a student startup:"
    )

    t_bmc = doc.add_table(rows=10, cols=2)
    bmc_widths = [Inches(2.0), Inches(4.3)]
    bmc_data = [
        ("BMC Building Block", "Strategic Operational Implementation in MotionIQ"),
        ("1. Customer Segments (CS)", "Dual-customer target: (1) Primary Users: Seniors aged 60+ requiring daily functional mobility; (2) Economic Buyers: Adult children aged 25–40 caring for aging parents."),
        ("2. Value Propositions (VP)", "Safe home exercise guidance; highly accessible pricing (49,000–79,000 VND/month); guaranteed visual privacy via On-Device AI; geriatric-friendly UI with Bé Nấm voice mascot."),
        ("3. Distribution Channels (CH)", "Omnichannel digital approach: TikTok/Facebook video content; Zalo Official Account; direct community workshops at local retirement clubs and pagodas in Can Tho."),
        ("4. Customer Relationships (CR)", "Warm, empathetic automated companionship with Bé Nấm; regular daily exercise reminder notifications via Zalo; 1-on-1 customer technical support."),
        ("5. Revenue Streams (RS)", "Freemium tier (basic exercises free forever) + Premium Subscription: Early Access tier (49,000 VND/month) and Standard tier (79,000 VND/month or 790,000 VND/year)."),
        ("6. Key Activities (KA)", "Continuous biomechanical algorithm optimization; Geriatric UX research; localized video content marketing; community workshop execution; user feedback iteration."),
        ("7. Key Resources (KR)", "Proprietary Next.js 14 web application; One-Euro Filter algorithm; published dataset weight parameters; Bé Nấm mascot brand assets; interdisciplinary founder team."),
        ("8. Key Partnerships (KP)", "Can Tho City Senior Citizen Associations; FPT University startup incubation mentors; community health advocates; geriatric care social media communities."),
        ("9. Cost Structure (CS)", "Lean server hosting ($0-$20/mo via Vercel Edge); PayOS payment gateway processing fees; targeted social media advertising (10m VND/4 mo); promotional printing.")
    ]
    format_table(t_bmc, bmc_widths, bmc_data, font_size=9.5, bold_col0=True)

    add_h2(doc, "3.2. Profile of Model Files and Core Algorithms in Project Source Code")
    add_p(
        doc,
        "All technical architecture details described herein are extracted directly and 100% verified against the operational production codebase "
        "of the MotionIQ project (located in src/features/pose/ and scripts/uiprmd/), encompassing seven primary engineering modules:"
    )

    # Table 3.2: 7 files
    t_files = doc.add_table(rows=8, cols=3)
    files_widths = [Inches(1.8), Inches(2.2), Inches(2.3)]
    files_data = [
        ("Module / File Name", "Project Source Code Path", "Core Function & Technical Architecture"),
        ("1. uiprmdQualityModel.json", "src/features/pose/uiprmdQualityModel.json", "Machine Learning model weight file (1,680 JSON lines) storing Z-score normalization parameters (mean, scale), feature weights, and bias for 132 kinematic dimensions evaluated across UI-PRMD exercises (DOI: 10.5281/zenodo.23104965)."),
        ("2. uiprmdQualityModel.ts", "src/features/pose/uiprmdQualityModel.ts", "Client-side movement quality inference engine: dynamically maps 33 MediaPipe landmarks to 22 UI-PRMD joints, normalizes by Torso Length, extracts 132 kinematic features, and computes Sigmoid probabilities in browser RAM."),
        ("3. train_quality_model.mjs", "scripts/uiprmd/train_quality_model.mjs", "Offline model training script: reconstructs 3D skeletal frames via Forward Kinematics from Euler rotation angles, applies Subject-Separated cross-validation (train on Subjects 1-8, test on 9-10), and trains L2-Ridge Logistic Regression."),
        ("4. fetch_uiprmd.py", "scripts/uiprmd/fetch_uiprmd.py", "Selective dataset retrieval script: utilizes HTTP Range Requests to download specific kinematic motion files (m01, m05, m06, m07) directly from Zenodo repository without transferring unneeded 400 MB archives."),
        ("5. poseService.ts", "src/features/pose/poseService.ts", "Core computer vision service managing Google MediaPipe Pose Landmarker (WASM/WebGL), automated background prewarming, GPU-to-CPU hardware fallback, and dynamic FPS adaptation for resource-constrained devices."),
        ("6. landmarkValidator.ts", "src/features/pose/landmarkValidator.ts", "Environmental auto-calibration module: measures ambient illumination via ITU-R BT.601 on 32x24 OffscreenCanvas, verifies subject distance ratio (0.35–0.90), and checks visibility of 5 anatomical body regions."),
        ("7. angleCalculator.ts & signalSmoother.ts", "src/features/pose/ (signal modules)", "Kinematic calculation and signal filtering engine: computes 3D joint angles via vector dot products, clamps cosine rounding errors, and eliminates limb tremors using One-Euro Filter + EMA + 45° Jump Gate.")
    ]
    format_table(t_files, files_widths, files_data, font_size=9.5, bold_col0=True)

    add_h2(doc, "3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline")
    add_p(
        doc,
        "To resolve the three fundamental barriers hindering home exercise adoption among the elderly—namely: (1) privacy hesitation regarding "
        "living space exposure, (2) lack of expensive discrete GPUs on common household phones or laptops, and (3) physiological limb tremors "
        "distorting sensor readings—MotionIQ is architected around a 100% On-Device Edge AI pipeline structured in four closed-loop layers."
    )

    add_h2(doc, "3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)")
    add_p(
        doc,
        "The computer vision subsystem (poseService.ts) leverages @mediapipe/tasks-vision (v0.10.18) compiled to WebAssembly (WASM) and accelerated "
        "by WebGL directly within the client browser environment:"
    )
    add_p(
        doc,
        "• 33-Landmark Pose Landmarker Lite (Float16 Quantized): Operating in continuous video stream mode (runningMode: 'VIDEO', numPoses: 1), "
        "the model simultaneously generates two coordinate systems per frame: (1) Normalized 2D/3D landmarks in domain [0, 1] for real-time skeleton "
        "overlay rendering, and (2) Metric 3D worldLandmarks centered at the hip midpoint for accurate physical joint angle trigonometry.\n"
        "• Background Prewarming Architecture: Via PoseService.prewarm(), the application pre-initializes the WASM FilesetResolver and preloads "
        "model weights into browser HTTP cache upon homepage landing, enabling instantaneous camera start upon entering the AI workout room.\n"
        "• Hardware Delegate Fallback: The pipeline requests GPU delegation by default (minDetectionConfidence = 0.5, minTrackingConfidence = 0.5). "
        "If WebGL context initialization fails on legacy hardware, the system automatically falls back to CPU execution seamlessly without crashing.\n"
        "• Dynamic Frame Skipping: Under lowFpsCounter >= 2 (FPS < 18 for two consecutive seconds), the system engages skipAlternateFrames = true, "
        "inferring only on even frames to protect audio guidance fluency. Full 30 FPS inference resumes once frame rate exceeds 26 FPS.\n"
        "• Privacy by Design: Frames are decoded strictly into temporary HTMLVideoElement RAM buffers. Once landmarks are extracted, pixel data is "
        "instantly garbage-collected. No video frames are ever recorded, stored on disk, or transmitted over network sockets."
    )

    add_h2(doc, "3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer")
    add_p(
        doc,
        "Before repetition counting commences, landmarkValidator.ts enforces a three-stage automated environment verification routine:"
    )
    add_p(
        doc,
        "1. Room Lighting Measurement (checkLighting): Draws video frames to an off-screen 32x24 canvas (768 pixels) to compute perceived luminance (Y) "
        "using standard ITU-R BT.601 broadcast coefficients:"
    )
    add_equation_box(
        doc,
        "Y = (1 / 768) × Σ_{i=1..768} [ 0.299 × R_i + 0.587 × G_i + 0.114 × B_i ]",
        "Where R_i, G_i, B_i ∈ [0, 255]. Thresholds: Y < 48 → 'too_dark'; Y > 225 → 'too_bright'; 48 ≤ Y ≤ 225 → 'good' (Lighting standard met)."
    )
    add_p(
        doc,
        "2. Standing Distance Estimation (checkDistance): Computes the vertical body height proportion within the camera frame across landmarks with visibility > 0.35:"
    )
    add_equation_box(
        doc,
        "bodyHeightRatio = max(y_i) - min(y_i)     (with visibility_i > 0.35)",
        "Thresholds: bodyHeightRatio > 0.90 → 'too_close' (step back); bodyHeightRatio < 0.35 → 'too_far' (step closer); 0.35 ≤ ratio ≤ 0.90 → 'ideal' (2–3 meters)."
    )
    add_p(
        doc,
        "3. Body Region Coverage Validation (validateLandmarks): Partitions 33 landmarks into 5 anatomical groups: Head (0, 7, 8), Hands (15, 16), "
        "Hips (23, 24), Knees (25, 26), and Feet (27, 28, 29, 30). The system requires region visibility ≥ 0.40 and overall confidence > 0.30 before "
        "declaring the exerciser 'ready' to begin counting."
    )

    add_h2(doc, "3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine")
    add_p(
        doc,
        "Once landmarks are validated, MotionIQ executes real-time spatial trigonometry and noise filtering across sequential video frames:"
    )
    add_p(
        doc,
        "• 3D Spatial Joint Angle Calculation Formula (calculateAngle): Given adjacent anatomical landmarks A, B (vertex), and C, bone vectors "
        "BA = A - B and BC = C - B are formed. To prevent zero-division on degenerate points, vector lengths are bounded (|BA| ≥ 10^-6 and |BC| ≥ 10^-6), "
        "and cosine values are clamped to [-1.0, 1.0]:"
    )
    add_equation_box(
        doc,
        "θ (degrees) = arccos( clamp( (BA · BC) / (|BA| × |BC|), -1.0, 1.0 ) ) × (180 / π)",
        "Where BA · BC = BA_x*BC_x + BA_y*BC_y + BA_z*BC_z. Backup 2D projection calculateAngle2D is utilized if z-depth confidence is low."
    )
    add_p(
        doc,
        "• One-Euro Filter & Exponential Moving Average with Jump Gate: Addresses age-related physiological tremors. Along with the velocity-adaptive "
        "One-Euro filter, signalSmoother.ts incorporates an Exponential Moving Average (EMA) and 45° Jump Gate:"
    )
    add_equation_box(
        doc,
        "S_t = α × θ_t + (1 - α) × S_{t-1}     (with smoothing factor α = 0.3, impulse threshold maxJump = 45°)",
        "Jump Gate Logic: If |θ_t - S_{t-1}| > 45°, the deviation is treated as noise unless sustained over ≥ 3 consecutive frames (consecutiveJumps ≥ 3)."
    )
    add_p(
        doc,
        "• Repetition State Machine with Hysteresis: Strict 7-state transitions govern repetition counting: "
        "IDLE → READY → DESCENDING → BOTTOM → ASCENDING → TOP → COMPLETE. A hysteresis angle threshold (hysteresisDeg) and minimum holding frames "
        "(minHoldFrames) prevent phantom rep counts from camera shake."
    )

    add_h2(doc, "3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset (uiprmdQualityModel)")
    add_p(
        doc,
        "A distinguishing innovation of MotionIQ is supplementing heuristic angle thresholds with an empirical Machine Learning movement quality model "
        "trained on the international UI-PRMD dataset (University of Idaho - Physical Rehabilitation Movement Dataset, DOI: 10.5281/zenodo.23104965). "
        "The pipeline spans four algorithmic stages:"
    )
    add_p(
        doc,
        "• Stage 1: Forward Kinematics Reconstruction & Joint Mapping: Maps 33 MediaPipe landmarks to 22 standard UI-PRMD Kinect joints:"
    )

    # Table 3.2-Joints
    t_joints = doc.add_table(rows=10, cols=3)
    joints_widths = [Inches(1.8), Inches(2.2), Inches(2.3)]
    joints_data = [
        ("UI-PRMD Joint Index & Anatomical Region", "MediaPipe Landmark Source (33 Points)", "Mathematical Interpolation / Mapping Rule"),
        ("Joint 0: Waist (Lower Spine / Root)", "Midpoint of LEFT_HIP (23) & RIGHT_HIP (24)", "[(x_23+x_24)/2, (y_23+y_24)/2, (z_23+z_24)/2] → Origin (0,0,0)"),
        ("Joint 1: Mid Spine", "50% Linear Interpolation: Waist to Chest", "interpolate(Waist, Chest, 0.5)"),
        ("Joint 2: Chest (Center of Thorax)", "Midpoint of LEFT_SHOULDER (11) & RIGHT_SHOULDER (12)", "[(x_11+x_12)/2, (y_11+y_12)/2, (z_11+z_12)/2]"),
        ("Joint 3: Neck", "50% Linear Interpolation: Chest to Nose (0)", "interpolate(Chest, Nose, 0.5)"),
        ("Joints 4 & 5: Head & Head Tip", "Landmark NOSE (0)", "[x_0, y_0, z_0]"),
        ("Joints 6, 7, 8, 9: Left Upper Limb", "Left Shoulder (11) → Elbow (13) → Wrist (15) → Index (19)", "4-joint kinematic chain of left arm"),
        ("Joints 10, 11, 12, 13: Right Upper Limb", "Right Shoulder (12) → Elbow (14) → Wrist (16) → Index (20)", "4-joint kinematic chain of right arm"),
        ("Joints 14, 15, 16, 17: Left Lower Limb", "Left Hip (23) → Left Knee (25) → Left Ankle (27) → Left Toe (31)", "4-joint kinematic chain of left leg"),
        ("Joints 18, 19, 20, 21: Right Lower Limb", "Right Hip (24) → Right Knee (26) → Right Ankle (28) → Right Toe (32)", "4-joint kinematic chain of right leg")
    ]
    format_table(t_joints, joints_widths, joints_data, font_size=9, bold_col0=True)

    add_p(
        doc,
        "• Stage 2: Torso-Length Spatial Normalization: Translates all joints to Waist origin and normalizes by 3D Torso Length (Euclidean distance "
        "from Waist to Chest, requiring torsoLength ≥ 0.05), yielding a scale-invariant 66-dimensional vector per frame (22 joints × [X, Y, Z]):"
    )
    add_equation_box(
        doc,
        "torsoLength = sqrt( (x_chest - x_waist)^2 + (y_chest - y_waist)^2 + (z_chest - z_waist)^2 )\nP'_j = ( P_j - Waist ) / torsoLength    (for j = 0..21)",
        "Ensures identical posture classification regardless of participant height or camera distance."
    )
    add_p(
        doc,
        "• Stage 3: Kinematic Time-Series Pooling into 132-Dimensional Feature Vector: For repetition length T ≥ 5 frames, summarizeFrames() compresses "
        "the sequence into a fixed 132-dimensional vector combining Mean (µ) and Standard Deviation (σ) across all 66 joint coordinates:"
    )
    add_equation_box(
        doc,
        "μ_i = (1 / T) × Σ_{t=1..T} f_{t,i}   ;   σ_i = sqrt( (1 / T) × Σ_{t=1..T} (f_{t,i} - μ_i)^2 )\nFeature Vector X = [ μ_1..μ_66, σ_1..σ_66 ] ∈ R^132",
        "Indices 0..65 reflect average postural alignment; Indices 66..131 capture dynamic Range of Motion trajectory variance."
    )
    add_p(
        doc,
        "• Stage 4: L2-Regularized Logistic Regression Training & Classification Inference: Evaluates movement quality using Ridge Logistic Regression "
        "trained on 200 real motion sequences per exercise from UI-PRMD (100 correct, 100 compensatory). Validation enforces strict Subject-Separated "
        "splitting (train on Subjects 1–8; evaluate on unseen Subjects 9 & 10):"
    )
    add_equation_box(
        doc,
        "logit(z) = bias + Σ_{i=1..132} [ weights_i × ( (x_i - mean_i) / scale_i ) ]\nP(correct) = sigmoid(z) = 1 / ( 1 + exp(-z) )",
        "Classification Rules: P ≥ 0.70 → 'good' (Correct posture); P ≤ 0.30 → 'needs_adjustment' (Compensatory movement); 0.30 < P < 0.70 → 'uncertain'."
    )

    # Table 3.2a: Weights file parameters
    add_p(doc, "Table 3.2a: Actual Parameters Extracted from Weights File uiprmdQualityModel.json:", bold=True, font_size=11, color=(140, 47, 30))
    t_weights = doc.add_table(rows=6, cols=7)
    weights_widths = [Inches(1.2), Inches(0.6), Inches(0.6), Inches(0.8), Inches(1.1), Inches(1.1), Inches(0.9)]
    weights_data = [
        ("Motion Name", "UI-PRMD", "Features", "Bias", "Weight Range", "Held-out Test Set", "Accuracy"),
        ("Sit-to-Stand", "m05", "132", "-0.9520", "[-0.7312, +0.4409]", "40 samples (20 Correct / 20 Incorrect)", "95.0%"),
        ("Functional Squat", "m01", "132", "-0.3258", "[-0.5929, +0.8224]", "40 samples (20 Correct / 20 Incorrect)", "72.5%"),
        ("Shoulder Abduction", "m07", "132", "-0.8338", "[-0.5428, +0.8700]", "40 samples (20 Correct / 20 Incorrect)", "97.5%"),
        ("Side Leg Raise", "m06", "132", "-0.9935", "[-0.7763, +0.6137]", "40 samples (20 Correct / 20 Incorrect)", "97.5%"),
        ("SYSTEM AVERAGE", "4 actions", "132 dims", "—", "—", "160 total samples (Subj 9, 10)", "90.62%")
    ]
    format_table(t_weights, weights_widths, weights_data, font_size=8.5, bold_col0=True)

    add_h2(doc, "3.3. 4 Standardized Functional Exercise Movements")
    add_p(
        doc,
        "3.3.1. Principles of Exercise Standardization Based on 3 International Motion Datasets:\n"
        "MotionIQ strictly restricts its exercise library to functional movements verified across three established public motion research corpora:\n"
        "1. UI-PRMD Dataset (University of Idaho, DOI: 10.5281/zenodo.23104965): Provides 3D skeletal data across 10 subjects with clinical annotation "
        "of correct and compensatory movement executions.\n"
        "2. KIMORE Dataset (Kinematic Assessment of Movement and Clinical Scores for Remote Monitoring): Comprises kinematic recordings from 78 subjects "
        "(healthy and motor-impaired), serving as the empirical baseline for target Range of Motion (Target ROM) boundaries.\n"
        "3. EHE Dataset (Elderly Home Exercise Dataset): Encompasses 869 repetitions from 25 elderly individuals, providing empirical calibration for "
        "repetition pacing, holding delays (minHoldFrames), and geriatric velocity thresholds."
    )
    add_p(
        doc,
        "3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises:\n"
        "1. Exercise 1: Sit-to-Stand (UI-PRMD: m05 | KIMORE: Es4):\n"
        "• Functional Objective: Lower limb power, quadriceps strength, and independent functional mobility for daily chair and bed transfers.\n"
        "• Kinematic Angles: Measures bilateral knee flexion (Hip 23/24 – Knee 25/26 – Ankle 27/28) and hip flexion. Target ROM: Seated knee flexion (90°–125°) "
        "to full upright stance (165°–180°).\n"
        "• UI-PRMD Model Parameters (bias = -0.9520): Tracks knee vertical displacement (mean σ_Y = 0.7287–0.7586) and trunk tilt. Detects excessive forward leaning "
        "or asymmetric leg loading. Validation accuracy: 95.0% (38/40 samples).\n\n"
        "2. Exercise 2: Controlled Functional Squat (UI-PRMD: m01 | KIMORE: Es5 | EHE: Squat):\n"
        "• Functional Objective: Quadriceps and gluteal strengthening, knee-ankle joint stabilization, reducing stair-climbing fall risks.\n"
        "• Kinematic Angles: Simultaneously evaluates knee angle and trunk inclination. Target ROM: Controlled descent to safe geriatric depth (90°–125°), avoiding deep knee hyperflexion.\n"
        "• UI-PRMD Model Parameters (bias = -0.3258): Identifies knee valgus (knees caving inward) and anterior trunk collapse. Validation accuracy: 72.5% (29/40 samples).\n\n"
        "3. Exercise 3: Standing Shoulder Abduction (UI-PRMD: m07 | KIMORE: Es1 | EHE: LA):\n"
        "• Functional Objective: Restores shoulder joint Range of Motion, counteracts frozen shoulder, improves chest expansion for respiratory vitality.\n"
        "• Kinematic Angles: Tracks coronal shoulder abduction angle (Hip 23/24 – Shoulder 11/12 – Elbow 13/14). Target ROM: Neutral (0°–20°) to lateral raise (90°–150°).\n"
        "• UI-PRMD Model Parameters (bias = -0.8338): Confirms lower-body stability (knee/ankle σ near 0) while detecting compensatory shoulder shrugging or spinal lateral flexion. Validation accuracy: 97.5% (39/40 samples).\n\n"
        "4. Exercise 4: Standing Side Leg Raise (UI-PRMD: m06 | Hip Abduction):\n"
        "• Functional Objective: Strengthens gluteus medius and tensor fasciae latae, critical for lateral pelvic stability during single-leg stance and preventing sideways falls.\n"
        "• Kinematic Angles: Measures hip abduction angle while ensuring stance leg remains upright (knee ≥ 165°). Target ROM: Hip abduction reaching 30°–45°.\n"
        "• UI-PRMD Model Parameters (bias = -0.9935): Contrasts high active leg variance against low stance leg variance, detecting compensatory trunk tipping. Validation accuracy: 97.5% (39/40 samples)."
    )

    # Table 3.3: 4 Exercises Summary
    add_p(doc, "3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ:", bold=True, font_size=11, color=(140, 47, 30))
    t_ex_sum = doc.add_table(rows=5, cols=6)
    ex_sum_widths = [Inches(1.1), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.2), Inches(0.9)]
    ex_sum_data = [
        ("Exercise & Code", "Dataset Code", "Primary Landmarks", "Target ROM", "Compensatory Errors Detected", "Model Parameters"),
        ("1. Sit-to-Stand\n(sit-to-stand)", "UI-PRMD: m05\nKIMORE: Es4", "Hips (23, 24)\nKnees (25, 26)\nAnkles (27, 28)", "Knee: 90°–125° (seated) → 165°–180° (stand)", "Excessive trunk leaning; asymmetric leg push; incomplete knee extension.", "Bias: -0.9520\nAccuracy: 95.0%\n(38/40 test)"),
        ("2. Functional Squat\n(squat)", "UI-PRMD: m01\nKIMORE: Es5\nEHE: Squat", "Shoulders (11, 12)\nHips (23, 24)\nKnees (25, 26)", "Knee: 90°–125° (safe depth; upright back)", "Knee valgus (caving inward); shallow squat; forward head tilt.", "Bias: -0.3258\nAccuracy: 72.5%\n(29/40 test)"),
        ("3. Shoulder Abduction\n(shoulder-raise)", "UI-PRMD: m07\nKIMORE: Es1\nEHE: LA", "Hips (23, 24)\nShoulders (11, 12)\nElbows (13, 14)", "Shoulder: 90°–150° (lateral abduction)", "Shoulder shrugging; elbow flexion; contralateral torso tilt.", "Bias: -0.8338\nAccuracy: 97.5%\n(39/40 test)"),
        ("4. Side Leg Raise\n(side-leg-raise)", "UI-PRMD: m06", "Hips (23, 24)\nKnees (25, 26)\nAnkles (27, 28)", "Hip: 30°–45° (stance knee ≥ 165°)", "Knee flexion on active leg; torso leaning toward stance leg.", "Bias: -0.9935\nAccuracy: 97.5%\n(39/40 test)")
    ]
    format_table(t_ex_sum, ex_sum_widths, ex_sum_data, font_size=8.5, bold_col0=True)

    add_p(
        doc,
        "Safety Limit Notice: MotionIQ is strictly a supportive tool for monitoring home functional movement via standard mobile/laptop cameras. "
        "Joint angle metrics and movement quality assessment scores serve as physical activity tracking references and do not replace medical diagnosis, "
        "clinical evaluation, or direct care from licensed physical therapists.",
        italic=True, font_size=11, color=(100, 100, 100)
    )

    add_h2(doc, "3.4. Results of 5 Actual MVP Prototype Testing Sessions")
    add_p(
        doc,
        "The MotionIQ team deployed the live MVP prototype across five comprehensive physical testing sessions in Can Tho City with elderly citizens and wellness trainers:"
    )

    t_proto = doc.add_table(rows=4, cols=3)
    proto_widths = [Inches(2.4), Inches(1.6), Inches(2.3)]
    proto_data = [
        ("Experimental Measurement Metric", "Actual Result", "Evaluation Notes"),
        ("Range of Motion (ROM) Measurement Accuracy", "94.6%", "Compared with standard manual goniometric reference angles."),
        ("Algorithmic Response Latency", "38 ms / frame", "Meets real-time 25–30 FPS standard; voice prompts and rep counts are not delayed."),
        ("System Usability Scale (SUS) Usability Score", "84.5 / 100 points", "Exceptional user satisfaction and geriatric accessibility (Grade A / Excellent).")
    ]
    format_table(t_proto, proto_widths, proto_data, font_size=9.5, bold_col0=True)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4 (PAGE 31)
    # ==========================================
    add_h1(doc, "CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (CHECKPOINT 3)")
    add_p(doc, "[Lead Author & Editor: Mã Phú Tín — Growth & Media Lead]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "4.1. 04-Month Media Objectives")
    add_p(
        doc,
        "During the four months of implementation, MotionIQ executes a focused, cost-effective communication campaign tailored for student capabilities:\n"
        "• Objective 1 (Brand Awareness): Establish MotionIQ brand awareness across Can Tho City and the Southwestern region via short-form video.\n"
        "• Objective 2 (Targeted Outreach): Reach 150–180 high-intent families with elderly relatives needing guided home exercise.\n"
        "• Objective 3 (Product Trial): Onboard 40–50 trial households to test the live web app and collect qualitative user experience feedback.\n"
        "• Objective 4 (Paid Customer Conversion): Convert 15–20 initial paying subscribers by Month 4, establishing recurring cash flow."
    )

    add_h2(doc, "4.2. Target Customers & Key Message")
    add_p(
        doc,
        "• Primary Target Customers: Working children/grandchildren aged 25–40, digitally proficient, seeking peace of mind regarding their aging parents' physical activity.\n"
        "• Direct End-Users: Elderly citizens (aged 60+) who desire gentle physical activity at home with large, intuitive controls and zero technical frustration.\n"
        "• Core Brand Message: 'MotionIQ – Home exercise, movement tracking made easier.' (Exercise joyfully, move correctly, live vibrantly with Bé Nấm)."
    )

    add_h2(doc, "4.3. Communication Channels & Methods")
    
    t_ch = doc.add_table(rows=5, cols=2)
    ch_widths = [Inches(1.8), Inches(4.5)]
    ch_data = [
        ("Media Channel", "Actual Operational Implementation Method"),
        ("TikTok", "Produce short-form videos dramatizing the working child's dilemma, side-by-side exercise demos with Bé Nấm, and AI rep-counting showcases."),
        ("Facebook", "Build the official Fanpage, share geriatric wellness knowledge, post authentic trial testimonials, and engage in local Can Tho family groups."),
        ("Zalo", "1-on-1 customer onboarding, sending video user guides, providing technical support, and managing subscription renewals."),
        ("Direct (Community)", "Host interactive live trial booths at local senior clubs, retirement associations, and community pagodas in Can Tho.")
    ]
    format_table(t_ch, ch_widths, ch_data, font_size=9.5, bold_col0=True)

    add_h2(doc, "4.4. 04-Month Media Implementation Roadmap")
    
    t_road = doc.add_table(rows=5, cols=3)
    road_widths = [Inches(1.8), Inches(2.9), Inches(1.6)]
    road_data = [
        ("Implementation Stage", "Key Strategic Activities", "Measurable Target Milestone"),
        ("Month 1: Brand Awareness Building", "Finalize Fanpage, TikTok channel, and Bé Nấm mascot brand assets; produce introduction videos and foundational content.", "Establish initial brand awareness; achieve 3,000+ views across Can Tho."),
        ("Month 2: Customer Acquisition", "Post feature breakdown videos, address home exercise difficulties, launch targeted social ads, collect trial registrations.", "Expand reach; acquire 150–180 high-potential leads."),
        ("Month 3: Experience & Trust", "Organize free community trial workshops, provide usage guidance, collect feedback, publish user demo clips, validate pricing.", "Prove product efficacy; build trust with 40–50 active trial households."),
        ("Month 4: Conversion & Revenue", "Launch official paid subscription packages, offer introductory promotions, deliver attentive support, deploy referral rewards.", "Convert 15–20 paying customers; generate sustainable initial cash flow.")
    ]
    format_table(t_road, road_widths, road_data, font_size=9.5, bold_col0=True)

    add_h2(doc, "4.5. Value-Based & Competitive Parity Pricing Strategy")
    add_p(
        doc,
        "MotionIQ applies Customer Value-Based Pricing synthesized with Competitive Parity and Cost-Based break-even safeguards:\n"
        "• Customer Value-Based: In our field survey of N = 50 respondents, 64.7% accepted a monthly subscription fee between 50,000 and 149,000 VND/month. "
        "MotionIQ's introductory tier is positioned under 100,000 VND/month to maximize adoption among working children.\n"
        "• Competitive Parity: Free YouTube videos offer no feedback or safety checks, whereas private in-home personal trainers charge 200,000–400,000 VND/session. "
        "MotionIQ delivers automated AI posture guidance and voice rep-counting at a tiny fraction of trainer fees.\n"
        "• Cost-Based Safeguard: Pricing is structured to comfortably cover server hosting and operational overhead with a lean subscriber base."
    )

    t_price = doc.add_table(rows=5, cols=3)
    price_widths = [Inches(1.8), Inches(1.6), Inches(2.9)]
    price_data = [
        ("Service Package", "Listed Selling Price", "Privileges & Usage Benefits"),
        ("MotionIQ Free", "Free Forever", "Experience basic exercises, real-time AI repetition counting, standard visual guidance."),
        ("MotionIQ Early Access", "49,000 VND / month", "Limited to first 20 subscribers: unlocks advanced functional exercises, personalized Bé Nấm voice settings."),
        ("MotionIQ Standard", "79,000 VND / month", "Full expanded exercise library, historical workout analytics, weekly progress reports sent via Zalo."),
        ("MotionIQ Annual", "790,000 VND / year", "Saves 2 months of subscription fees, priority 1-on-1 technical support, permanent price guarantee.")
    ]
    format_table(t_price, price_widths, price_data, font_size=9.5, bold_col0=True)

    add_h2(doc, "4.6. Budget Estimation and Operating Costs")
    add_p(
        doc,
        "To execute the four-month market approach plan, the team allocates a disciplined student media budget of 10,000,000 VND:"
    )

    t_bud = doc.add_table(rows=7, cols=2)
    bud_widths = [Inches(3.8), Inches(2.5)]
    bud_data = [
        ("04-Month Media Budget Item", "Estimated Cost (VND)"),
        ("Media content production (promotional images, exercise demonstration videos)", "3,000,000 VND"),
        ("Selective targeted advertising on Facebook and TikTok", "3,000,000 VND"),
        ("Organizing direct product experience workshops at senior citizen clubs", "2,000,000 VND"),
        ("Travel, local transportation, and customer contact expenses in Can Tho", "700,000 VND"),
        ("Printing QR Code brochures and introductory user guide leaflets", "300,000 VND"),
        ("Contingency and emergency reserve budget", "1,000,000 VND"),
        ("TOTAL 04-MONTH MEDIA BUDGET", "10,000,000 VND")
    ]
    format_table(t_bud, bud_widths, bud_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "System Operational Cost Assumptions:\n"
        "• Fixed Cost (FC): 1,000,000 VND / month (maintaining lightweight cloud hosting via Vercel Edge, database server, custom domain name, and technical development tools).\n"
        "• Variable Cost (VC): 10,000 VND / subscription / month (PayOS / MoMo online payment processing fees, Zalo notification messaging API, and network bandwidth)."
    )

    add_h2(doc, "4.7. Revenue Development Plan & KPI Targets after 04 Months")
    add_p(
        doc,
        "MotionIQ implements a 5-Step Customer Conversion Funnel (Reach → Interest → Trial → Conversion → Retention):"
    )

    t_kpi = doc.add_table(rows=6, cols=3)
    kpi_widths = [Inches(2.1), Inches(1.8), Inches(2.4)]
    kpi_data = [
        ("Funnel Stage & Performance Metric", "Target after 04 Months", "Strategic Evaluation Meaning"),
        ("1. Social Media Reach", "13,000 – 15,000 reaches", "Establishes initial brand awareness across target communities."),
        ("2. Potential Leads (Inquiries)", "150 – 180 leads", "Conversion rate achieves ~1.1% – 1.2% from gross reach."),
        ("3. Users Registering for Trial", "40 – 50 people", "Trial conversion rate reaches ~27% from the qualified lead pool."),
        ("4. Users Completing Trial Process", "30 – 35 people", "Completion rate achieves ~70% – 75% of trial participants."),
        ("5. Customers Converting to Paid", "15 – 20 customers", "Conversion rate achieves ~50% of completed trial users.")
    ]
    format_table(t_kpi, kpi_widths, kpi_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "Customer Acquisition Cost (CAC) Assessment:\n"
        "With a total media budget of 10,000,000 VND and a target of 15–20 initial paying customers, the allocated marketing cost averages approximately "
        "500,000 – 666,667 VND / customer. This is an entirely standard investment ratio during the initial Product Validation Phase, as the expenditure "
        "simultaneously builds lasting brand equity and establishes a verified potential customer file for subsequent organic expansion."
    )

    add_h2(doc, "4.8. Revenue Forecast and Break-Even Analysis")
    add_p(
        doc,
        "Initial monthly revenue forecast from the Early Access subscription tier (49,000 VND / month):"
    )

    t_rev = doc.add_table(rows=4, cols=2)
    rev_widths = [Inches(3.0), Inches(3.3)]
    rev_data = [
        ("Number of Active Paying Customers", "Estimated Monthly Recurring Revenue (49k Package)"),
        ("10 subscribers", "490,000 VND / month"),
        ("15 subscribers", "735,000 VND / month"),
        ("20 subscribers", "980,000 VND / month")
    ]
    format_table(t_rev, rev_widths, rev_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "Break-Even Analysis:\n"
        "The break-even subscription count is calculated using standard corporate finance formulas:\n"
        "Break-even Subscriptions = Fixed Costs / ( Selling Price - Variable Cost per Subscription )"
    )
    add_equation_box(
        doc,
        "Q_BE = FC / ( P - VC )",
        "Assuming Fixed Costs (FC) = 1,000,000 VND/month and Variable Cost (VC) = 10,000 VND/subscription/month."
    )

    t_be = doc.add_table(rows=4, cols=3)
    be_widths = [Inches(2.7), Inches(1.8), Inches(1.8)]
    be_data = [
        ("Break-Even Analysis Metric", "Early Access Package (49,000 VND)", "Standard Package (79,000 VND)"),
        ("Unit Contribution Margin (P - VC)", "39,000 VND / subscriber", "69,000 VND / subscriber"),
        ("Subscribers to break even monthly operations (FC = 1,000,000 VND)", "26 subscribers", "15 subscribers"),
        ("Subscribers to fully recover 10m media budget over 4 months", "90 subscribers / month", "51 subscribers / month")
    ]
    format_table(t_be, be_widths, be_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "Financial Assessment from the Implementation Team:\n"
        "With the target of 15–20 paying customers in Month 4, MotionIQ generates 735,000 – 980,000 VND in MRR, covering nearly 100% of monthly "
        "fixed operational costs. While this initial cohort does not yet fully recover the sunk 10 million VND marketing budget within the first four months, "
        "this is fully consistent with early-stage tech startup dynamics, where initial marketing establishes brand equity and customer acquisition funnels.\n\n"
        "Crucially, reaching the milestone of just 26 Early Access subscribers (or 15 Standard subscribers) allows MotionIQ to achieve complete "
        "Operational Self-Sufficiency, funding 100% of server and maintenance infrastructure without requiring ongoing founder out-of-pocket subsidies."
    )

    add_callout_box(
        doc,
        "• Nature of CAC vs. LTV: The initial CAC (500,000 – 666,667 VND) represents an upfront investment to reach 13,000–15,000 views. "
        "Under our subscription model, Customer Lifetime Value (LTV) reaches 588,000 – 790,000 VND when subscribers retain for 12 months or more, "
        "guaranteeing LTV > CAC and sustainable unit economics.\n"
        "• Operational Self-Sufficiency: Reaching 26 Early Access subscribers proves operational survival, generating sufficient recurring cash flow "
        "to maintain server infrastructure indefinitely while expanding organically through family word-of-mouth.",
        title="FINANCIAL STRATEGY HIGHLIGHTS & OPERATIONAL AUTONOMY"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5 (PAGE 37)
    # ==========================================
    add_h1(doc, "CHAPTER 5: RISK MANAGEMENT, SUSTAINABILITY & FUTURE ROADMAP (CHECKPOINT 3)")
    add_p(doc, "[Lead Author & Editor: Hồ Tuyết Nghi — Service Management Lead (CMO)]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "5.1. Identification of Practical Risks & Mitigation Measures")
    add_p(
        doc,
        "To ensure that MotionIQ operates safely, transparently, and in strict compliance with applicable regulations, the team has identified "
        "seven primary operational risks and established actionable mitigation strategies for each:"
    )

    # Table 5.1
    t_risk = doc.add_table(rows=8, cols=2)
    risk_widths = [Inches(2.2), Inches(4.1)]
    risk_data = [
        ("Identified Operational Risk", "Concrete Actionable Mitigation Strategy"),
        ("1. Elderly users experiencing difficulty operating digital technology", "Implement ultra-simplified Geriatric UX: font size ≥ 18px, large high-contrast touch buttons (≥ 56px), natural Vietnamese audio prompts with adjustable volume, and one-touch start."),
        ("2. Sensor noise and inaccurate AI joint angle recognition", "Incorporate adaptive One-Euro Filter to eradicate physiological limb tremors, enforce automated 3-step environment calibration, and provide visual camera placement guides."),
        ("3. Customer reluctance to transition to paid subscription", "Provide permanent free access to basic functional routines, communicate clear value benefits of advanced tracking, and price introductory tier at an accessible 49,000 VND/month."),
        ("4. High initial Customer Acquisition Cost (CAC)", "Focus on organic community outreach, leverage word-of-mouth referral incentives ('Share with a Friend' free month), and partner directly with local senior citizen clubs in Can Tho."),
        ("5. User churn and exercise abandonment after short trial period", "Design habit-forming streak rewards, provide weekly progress summaries via Zalo, and maintain warm, empathetic companionship through the Bé Nấm virtual mascot."),
        ("6. Risk of platform misclassification as a medical device", "Maintain prominent non-medical disclaimers across all screens: clearly position MotionIQ as an assistive physical wellness support tool, explicitly stating it does not provide clinical diagnosis or replace medical doctors."),
        ("7. Personal data privacy and video camera exposure risks", "Enforce 100% On-Device AI architecture: all video frames are processed solely in local browser RAM and discarded immediately. No video streams or biometric images are ever saved or transmitted to cloud servers.")
    ]
    format_table(t_risk, risk_widths, risk_data, font_size=9, bold_col0=True)

    add_h2(doc, "5.2. Development and Sustainability Plan by Phase")
    add_p(
        doc,
        "MotionIQ pursues a phased, systematic sustainability and development roadmap:\n"
        "• Phase 1 — First 4 Months (Validation & Community Launch): Finalize MVP web application, optimize geriatric UX, onboard 40–50 trial households, "
        "validate willingness to pay at 49,000 VND/month, and secure initial 15–20 paying subscribers to achieve operational break-even.\n"
        "• Phase 2 — Months 5–6 (Stabilization & Optimization): Enhance voice guidance quality, evaluate subscription retention rates, introduce the "
        "Standard tier (79,000 VND/month), and refine unit economics.\n"
        "• Phase 3 — Next Expansion Phase (Platform Ecosystem): Expand exercise catalog with gentle wrist and ankle routines, automate weekly exercise "
        "reports to adult children via Zalo, explore Zalo Mini App integration (eliminating app installation barriers), and evaluate B2B institutional "
        "partnerships with local elderly day care and community centers."
    )

    add_h2(doc, "5.3. Project Limitations and Future Technological Roadmap")
    add_p(
        doc,
        "While MotionIQ demonstrates robust performance, several technological limitations are acknowledged:\n"
        "• Single 2D Camera Depth Invariant: Relying on monocular smartphone webcams inherently estimates 3D depth. Future versions will integrate multi-view "
        "spatial calibration algorithms to improve depth precision.\n"
        "• Extreme Ambient Lighting Variations: Low-light environments (< 48 luminance) impact computer vision accuracy. The system enforces automated warnings "
        "prompting users to adjust lighting or room positioning.\n"
        "• Hardware Fragmentation: Performance varies across legacy mobile browsers. The team plans to build a dedicated lightweight progressive web app (PWA) "
        "with enhanced offline caching."
    )

    doc.add_page_break()

    # ==========================================
    # CONCLUSION (PAGE 39)
    # ==========================================
    add_h1(doc, "CONCLUSION")
    add_p(doc, "[Lead Author & Editor: Huỳnh Thị Yến Duy — Project Lead (CEO)]", italic=True, font_size=11, color=(140, 47, 30))
    add_p(
        doc,
        "MotionIQ addresses a poignant, widespread societal challenge facing modern Vietnamese families: empowering elderly parents to maintain regular "
        "physical activity safely and joyfully at home while giving their hard-working adult children complete peace of mind."
    )
    add_p(
        doc,
        "Through a disciplined, humble, and evidence-based approach—grounded in empirical field insights from 50 survey respondents, 5 physical prototype testing "
        "sessions achieving 94.6% ROM accuracy and an 84.5 SUS score, and a lean 10,000,000 VND communication strategy—MotionIQ proves that advanced On-Device AI "
        "can be translated into an accessible, humane, and economically sustainable product. Reaching operational break-even at just 26 subscribers establishes "
        "a self-funding foundation, enabling the founding team to scale MotionIQ into an enduring student startup with profound social impact."
    )

    # Save docx
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    print(f"[SUCCESS] DOCX written to: {out_path}")

def build_markdown(out_path):
    md_content = r"""# MOTIONIQ — COMPREHENSIVE FINAL ENTREPRENEURSHIP PROJECT REPORT
**COURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP**  
**PROJECT: MOTIONIQ — AI ASSISTANT PLATFORM SUPPORTING HOME EXERCISE TRACKING FOR THE ELDERLY (100% ON-DEVICE AI)**  
**FPT UNIVERSITY CAN THO CAMPUS — NOVEMBER 2026**

---

### PROJECT METADATA & FOUNDING TEAM
- **Course Instructor / Academic Advisor:** Mr. Tran Ngoc Son
- **Student Group Name:** MOTIONIQ — Group K19
- **Project Lead & CEO:** Huỳnh Thị Yến Duy (CE191522) — Information Security
- **Founding Team Members:**
  - Nguyễn Hải Hà (CTO — CE200298) — Information Security
  - Nguyễn Nhã Quân (CPO — CE200197) — UI-UX Design
  - Đặng Vĩnh Phúc (CE190510) — Foreign Language
  - Mã Phú Tín (CS191066) — Multimedia Communication
  - Hồ Tuyết Nghi (CMO — CS180758) — Service Management
- **Live MVP Web Application:** [https://motion-iq-five.vercel.app](https://motion-iq-five.vercel.app)
- **Empirical Fieldwork:** 50 Quantitative Field Surveys • 5 Live Prototype Testing Sessions
- **Individual Contribution:** 100% Equal Commitment Across All 6 Founders

---

## ACKNOWLEDGEMENTS
The MotionIQ project team would like to express our deepest gratitude and most sincere thanks to Mr. Tran Ngoc Son, who has dedicatedly imparted knowledge on innovative startup thinking, business model methodologies, and patiently guided us, providing invaluable professional feedback through each milestone: Checkpoint 1, Checkpoint 2, and Checkpoint 3 of the EXE101 course (Startup Experience).

The team also wants to sincerely thank the elderly individuals and relatives across Can Tho City and the Mekong Delta who enthusiastically participated in our 50 quantitative survey responses as well as 5 direct prototype testing sessions of the application. Practical feedback from actual users is the guiding light that helps the team perfect the MotionIQ product to be the most useful, accessible, and humane.

---

## EXECUTIVE SUMMARY
MotionIQ is a technology solution applying Artificial Intelligence and computer vision running directly on mobile devices (100% On-Device AI), supporting the elderly to track their workout progress and balance training at home via a smartphone or laptop camera without investing in expensive additional hardware sensor equipment.

By flexibly combining the virtual assistant character 'Be Nam' with Vietnamese voice count reminders, a pose recognition model based on published benchmark motion datasets (UI-PRMD, KIMORE, EHE), and the One-Euro Filter noise reduction filter, MotionIQ helps seniors maintain proper workout habits, count repetitions, and provide basic feedback. Actual survey results on 50 subjects show that more than 68% of children face difficulties when directly observing their parents working out, and 82.4% are ready to let their relatives try the application. Practical testing through 5 sessions achieved a range of motion (ROM) angle measurement index of 94.6% compared to the reference measurement angle and an outstanding SUS system usability score of 84.5 / 100 (Grade A / Excellent level).

Regarding business and financial strategy, the team applies a customer value-based pricing method and competitor comparison with an Early Access trial package of 49,000 VND / month (~1,600 VND/day), combined with a concise 4-month communication plan with a student budget of 10,000,000 VND. Break-even analysis shows that with 26 paying customers for the Early Access package or 15 customers for the Standard package (79,000 VND/month), the project will self-cover its fixed monthly operating costs (1,000,000 VND/month), achieving operational self-sufficiency without requiring founder out-of-pocket subsidies.

---

## LIST OF ABBREVIATIONS
| Abbreviation | English Term | Vietnamese Meaning |
| :--- | :--- | :--- |
| **AI** | Artificial Intelligence | Trí tuệ Nhân tạo |
| **BMC** | Business Model Canvas | Khung Mô hình Kinh doanh 9 Khối |
| **ROM** | Range of Motion | Biên độ góc vận động của khớp |
| **CAC** | Customer Acquisition Cost | Chi phí thu hút một khách hàng mới |
| **MRR** | Monthly Recurring Revenue | Doanh thu định kỳ hằng tháng |
| **SUS** | System Usability Scale | Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế) |
| **On-Device AI** | On-Device Artificial Intelligence | Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị (Edge AI) |

---

## LIST OF TABLES
- **Table 1.1:** Founding Team Competency Profiles & RACI Governance Matrix (Page 7)
- **Table 2.1:** Quantitative Field Survey Findings & Statistical Breakdown (N = 50) (Page 9)
- **Table 2.2:** Competitive Landscape Analysis & Strategic Positioning Differentiation (Page 11)
- **Table 3.1:** 9-Block Business Model Canvas (BMC) Framework (Page 12)
- **Table 3.2:** Profile of Model Files and Core Algorithms in Project Source Code (Page 13)
- **Table 3.2-Joints:** 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics (Page 20)
- **Table 3.2a:** Actual Parameters Extracted from Weights File uiprmdQualityModel.json (Page 23)
- **Table 3.3:** Summary Table of 4 Standardized Functional Exercises in MotionIQ (Page 28)
- **Table 3.4:** Results of 5 Actual MVP Prototype Testing Sessions (Page 30)
- **Table 4.1:** Communication Channels & Operational Implementation Methods (Page 31)
- **Table 4.2:** 4-Month Communication Implementation Roadmap (Page 32)
- **Table 4.3:** Proposed Pricing Structure of MotionIQ (Page 33)
- **Table 4.4:** 4-Month Lean Student Media Budget Allocation (10,000,000 VND) (Page 33)
- **Table 4.5:** Target Customer Segments & 4-Month Conversion Funnel KPIs (Page 34)
- **Table 4.6:** Early Access Tier Subscription Monthly Revenue Forecast (Page 35)
- **Table 4.7:** Operational Break-Even vs. Full Capital Recovery Analysis (Page 36)
- **Table 5.1:** Identified Operational Risk Matrix & Concrete Mitigation Strategies (Page 37)

---

## TABLE OF CONTENTS
1. [CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY](#chapter-1-project-setup--founding-team-capability-checkpoint-1)
   - 1.1. Context of MotionIQ Idea Formation
   - 1.2. Mission, Vision, and Core Values
   - 1.3. Founding Team Capability Profiles & RACI Governance Matrix
2. [CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS](#chapter-2-market-research--field-survey-analysis-checkpoint-2)
   - 2.1. Methodology and Field Survey Scale (N = 50)
   - 2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)
   - 2.3. Target Customer Persona & Empathy Mapping
   - 2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation
3. [CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE](#chapter-3-business-model--technical-mvp-prototype-checkpoint-3)
   - 3.1. 9-Block Business Model Canvas (BMC) Framework
   - 3.2. Profile of Model Files and Algorithms in Project Source Code
   - 3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline
   - 3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)
   - 3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer
   - 3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine
   - 3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset
   - 3.3. 4 Standardized Functional Exercise Movements
   - 3.3.1. Principles of Exercise Standardization Based on 3 International Datasets
   - 3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises
   - 3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ
   - 3.4. Results of 5 Actual MVP Prototype Testing Sessions
4. [CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT](#chapter-4-media-plan--revenue-development-checkpoint-3)
   - 4.1. 04-Month Media Objectives
   - 4.2. Target Customers & Key Message
   - 4.3. Communication Channels & Methods
   - 4.4. 04-Month Media Implementation Roadmap
   - 4.5. Value-Based & Competitive Parity Pricing Strategy
   - 4.6. Budget Estimation and Operating Costs
   - 4.7. Revenue Development Plan & KPI Targets after 04 Months
   - 4.8. Revenue Forecast and Break-Even Analysis
5. [CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY](#chapter-5-risk-management--sustainability-checkpoint-3)
   - 5.1. Identification of Practical Risks & Mitigation Measures
   - 5.2. Development and Sustainability Plan by Phase
   - 5.3. Project Limitations and Future Technological Roadmap
6. [CONCLUSION](#conclusion)

---

## CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (CHECKPOINT 1)
*[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]*

### 1.1. Context of MotionIQ Idea Formation
Vietnam is currently one of the fastest aging populations in the world. According to the General Statistics Office (GSO), the number of people aged 60 and above has exceeded 13.5 million (accounting for 13.5% of the total population). Along with the natural aging process, the elderly often face musculoskeletal degeneration, sarcopenia (age-related muscle loss), knee and spinal osteoarthritis, and decreased balance capability, dramatically elevating the risk of falls and severe daily activity limitations.

Maintaining gentle home exercise habits plays an indispensable role in improving flexibility, cardiorespiratory endurance, and physical health. However, most seniors exercise based purely on habit or unguided memory without knowing if their posture is correct or incorrect. Meanwhile, busy working children face immense workplace pressures and economic demands, leaving them with very limited time to directly supervise or remind their aging parents. Stemming from the practical need to care for family relatives, the MotionIQ founding team (Group K19) developed the MotionIQ project — a vision AI technology platform operating directly on smartphones and laptops to serve as an intelligent, empathetic home exercise companion supporting movement tracking, repetition counting, and real-time feedback for the elderly right at home.

### 1.2. Mission, Vision, and Core Values
- **Mission:** "Popularizing quality physical exercise support services to every Vietnamese household" — bringing autonomous mobility, minimizing fall risks for the elderly, and giving children complete peace of mind when working far away.
- **Vision:** Becoming the premier personal movement tracking and functional mobility digital platform in Vietnam by 2027.
- **Core Values:**
  1. *Safety & Evidence-based:* All exercise routines are built upon standardized functional movement benchmarks from prestigious public biomechanical research datasets (UI-PRMD, KIMORE, EHE).
  2. *Privacy by Design:* 100% local AI processing on the user's personal device RAM, strictly saying NO to storing or transmitting personal images/videos to cloud servers.
  3. *Geriatric Empathy:* High-contrast interface, large readable text (font size ≥ 18px), large tactile touch buttons (≥ 56px), and encouraging seniors with the warmth, patience, and natural voice of the Bé Nấm virtual mascot.

### 1.3. Founding Team Capability Profile (Founding Team & RACI)
The founding team of MotionIQ (MOTIONIQ — Group K19) represents a synergistic, interdisciplinary collaboration between Information Technology (Information Security), Graphic Design / UI-UX, Multimedia Communication, Foreign Languages, and Service Management majors, creating distinct practical execution advantages across all project facets:

#### Table 1.1: Founding Team Competency Profiles & RACI Governance Matrix
| Full Name | Role | Major | Assigned Chapter in Report | Main Responsibility (RACI) |
| :--- | :--- | :--- | :--- | :--- |
| **Huỳnh Thị Yến Duy** | Team Leader (CEO) | Information Security | Chapter 1 (Whole), Introduction, Conclusion & General Review | **Accountable (A):** Fully responsible for web/app technical architecture, MediaPipe Pose integration, and overall project governance. |
| **Nguyễn Nhã Quân** | Member (CPO) | UI-UX Design | Chapter 2 (Section 2.1, 2.2: Survey) & Chapter 3 (Section 3.4: MVP Testing) | **Responsible (R):** Analyzing Google Sheets survey data, designing Geriatric UI design system, and executing live MVP testing (ROM 94.6%, SUS 84.5). |
| **Đặng Vĩnh Phúc** | Member | Foreign Language | Chapter 2 (Section 2.3 & 2.4: Customers & 4 Competitors) | **Responsible (R):** Comprehensive competitor landscape research, international literature review, English documentation, and local community outreach. |
| **Nguyễn Hải Hà** | Member (CTO) | Information Security | Chapter 3 (Section 3.2: On-Device AI & Section 3.3: 4 Exercises) | **Responsible (R):** On-Device AI engine, UI-PRMD dataset preprocessing, One-Euro jitter-filtering algorithm, and client-side RAM security. |
| **Mã Phú Tín** | Member | Multimedia Communication | Chapter 4 (Whole Section 4.1 – 4.8: Media Plan & Financials) | **Responsible (R):** Multi-channel TikTok/Facebook communication plan, 49k pricing strategy, 10 million lean budget, conversion KPIs, and break-even modeling. |
| **Hồ Tuyết Nghi** | Member (CMO) | Service Management | Chapter 5 (Whole Section 5.1 & 5.2: Risk Management & Sustainability) | **Responsible (R):** Operational risk identification, legal non-medical disclaimer positioning, Zalo Mini App expansion roadmap, and long-term service sustainability. |

> **📌 TEAM STRENGTHS & ASSISTIVE SAFETY POSITIONING PRINCIPLES**  
> The synergy between AI technical expertise and human-centered design enables MotionIQ to directly address elderly physical wellness needs without requiring expensive wearable sensors or specialized hardware.  
> **NON-MEDICAL DISCLAIMER:** MotionIQ is strictly an assistive physical wellness support tool for home exercise tracking. It is NOT a medical device, does not provide clinical diagnosis, and does not replace professional physical therapists or medical specialists.

---

## CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)
*[Lead Authors & Editors: Nguyễn Nhã Quân (2.1, 2.2) & Đặng Vĩnh Phúc (2.3, 2.4)]*

### 2.1. Methodology and Field Survey Scale (N = 50)
To empirically validate the problem hypotheses and quantify genuine market demand during Checkpoint 2, the team conducted a rigorous field survey of 50 target respondents via structured questionnaires (data stored publicly on Google Sheets: [Google Sheets Survey Link](https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM)):
- **Survey demographic breakdown:** 81.6% aged 18–23 years old and 18.4% aged 23–30 years old (representing adult children and grandchildren caring for older relatives).
- **Family caregiving experience:** 65.3% indicated that within the past year they have directly cared for or supported elderly relatives in daily living or mobility.
- **Age bracket of relatives needing exercise support:** 28.6% aged 60–69; 24.5% aged 70–79; 10.2% aged 80 and above (total 63.3% relatives aged 60+), and 24.5% aged 50–59.

### 2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)

#### Table 2.1: Quantitative Field Survey Findings & Statistical Breakdown (N = 50)
| Actual Survey Metric (Google Sheets N = 50) | Actual Rate | MotionIQ Development Implication |
| :--- | :--- | :--- |
| **Children cannot regularly observe and correct movements for elderly parents** | 68.6% | Seniors frequently exercise alone; automated AI tracking is essential. |
| **Elderly relatives exercise daily or 3–5 times per week** | 51.0% | Home exercise demand is continuous and recurring, requiring an accessible home tool. |
| **Biggest difficulty: Not knowing if exercising correctly / incorrectly, no feedback or warnings** | 82.4% | AI must deliver real-time repetition counting and auditory posture correction. |
| **Top 3 most important factors: Ease of use, Correct / Incorrect feedback, Movement guidance** | 88.2% | Mandatory Geriatric UI design: large text, large buttons, one-touch start. |
| **Suitability level of MotionIQ concept with household demand (Rated 4 – 5 stars)** | 66.7% | High product-market alignment; confirms core value proposition. |
| **Willingness to let relatives trial MotionIQ (Rated 4 – 5 stars)** | 82.4% | Outstanding trial adoption potential; establishes initial user acquisition pool. |

When specifically surveyed regarding their primary concerns when using camera-based AI applications (Question 14 in the survey form), respondents highlighted:
1. Personal image privacy and living space exposure (expressed by 45.0% of respondents).
2. Elderly relatives struggling to operate complex modern technology devices (50.0%).
3. AI recognition errors caused by slow movements or age-related limb tremors (40.0%).

These empirical findings directly guided the foundational technical design of MotionIQ:
- **Complete elimination of privacy concerns via 100% On-Device AI:** Video streams are processed strictly in local browser RAM without cloud transmission.
- **Elimination of usability anxiety via Geriatric UI:** Font sizes ≥ 18px, touch buttons ≥ 56px, and empathetic Vietnamese voice guidance from Bé Nấm.
- **Noise-robust tracking via adaptive One-Euro Filter:** Eliminates physiological tremors, ensuring stable kinematic angle measurement.

### 2.3. Target Customer Persona & Empathy Mapping
MotionIQ operates on a dual-customer architecture (Dual-Customer Profile) consisting of the Primary End-User (the elderly parent) and the Economic Buyer / Payer (the adult child):
- **Persona 1 — Direct User:** Mr. Nguyen Van An, 68 years old, retired civil servant living in Ninh Kieu, Can Tho City. Needs daily knee and leg mobility exercises to walk steadily and prevent joint stiffness. He has declining eyesight, fears troubling his busy children, and feels frustrated when exercising alone from memory without knowing if his posture is correct or risking joint injury.
- **Persona 2 — Economic Buyer (Payer):** Ms. Thu Hang, 36 years old, corporate office worker in Can Tho. She cares deeply about her father's longevity but works long hours, feeling persistent guilt and anxiety when she cannot be home to supervise his workouts. She readily embraces spending a modest monthly subscription (under 100,000 VND/month) to equip her father with an easy-to-use digital companion that provides structured movement safety.

### 2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation
To evaluate competitive dynamics, MotionIQ benchmarked four prevalent alternatives currently available in the Vietnamese market:

#### Table 2.2: Competitive Landscape Analysis & Positioning Differentiation Matrix
| Competitive Solution | Key Advantages | Real-World Limitations | MotionIQ Positioning Advantage |
| :--- | :--- | :--- | :--- |
| **Self-practice via YouTube / TV** | Completely free, diverse video library | Zero interaction, no posture correction, high injury risk from unguided imitation | Real-time AI posture feedback, rep counting, and voice correction directly via phone camera |
| **Hiring an at-home Personal Trainer** | 1-on-1 close supervision, personalized motivation | Very high cost (200k–400k VND/session, 2–4m VND/month); unsustainable for average families | Extremely accessible pricing (49k–79k VND/month); practice anytime in the living room |
| **Senior Fitness / Retirement Clubs** | Social community interaction, peer encouragement | Requires physical travel; challenging for seniors with joint pain; weather-dependent | Safe, independent home workouts without commuting; complete schedule autonomy |
| **International Fitness Apps (Freeletics, etc.)** | Modern digital interface, extensive workout routines | English-only; high intensity designed for athletic youth; expensive subscription (>150k/mo) | 100% localized in Vietnamese; customized for geriatric functional mobility; friendly mascot |

---

## CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)
*[Lead Authors & Editors: Nguyễn Hải Hà (3.2, 3.3) & Nguyễn Nhã Quân (3.1, 3.4)]*

### 3.1. 9-Block Business Model Canvas (BMC) Framework
MotionIQ's business model is structured following Alexander Osterwalder's standard 9-Block Canvas, tailored specifically to the operational and resource realities of a student startup:

#### Table 3.1: 9-Block Business Model Canvas
| BMC Building Block | Strategic Operational Implementation in MotionIQ |
| :--- | :--- |
| **1. Customer Segments (CS)** | Dual-customer target: (1) Primary Users: Seniors aged 60+ requiring daily functional mobility; (2) Economic Buyers: Adult children aged 25–40 caring for aging parents. |
| **2. Value Propositions (VP)** | Safe home exercise guidance; highly accessible pricing (49,000–79,000 VND/month); guaranteed visual privacy via On-Device AI; geriatric-friendly UI with Bé Nấm voice mascot. |
| **3. Distribution Channels (CH)** | Omnichannel digital approach: TikTok/Facebook video content; Zalo Official Account; direct community workshops at local retirement clubs and pagodas in Can Tho. |
| **4. Customer Relationships (CR)** | Warm, empathetic automated companionship with Bé Nấm; regular daily exercise reminder notifications via Zalo; 1-on-1 customer technical support. |
| **5. Revenue Streams (RS)** | Freemium tier (basic exercises free forever) + Premium Subscription: Early Access tier (49,000 VND/month) and Standard tier (79,000 VND/month or 790,000 VND/year). |
| **6. Key Activities (KA)** | Continuous biomechanical algorithm optimization; Geriatric UX research; localized video content marketing; community workshop execution; user feedback iteration. |
| **7. Key Resources (KR)** | Proprietary Next.js 14 web application; One-Euro Filter algorithm; published dataset weight parameters; Bé Nấm mascot brand assets; interdisciplinary founder team. |
| **8. Key Partnerships (KP)** | Can Tho City Senior Citizen Associations; FPT University startup incubation mentors; community health advocates; geriatric care social media communities. |
| **9. Cost Structure (CS)** | Lean server hosting ($0-$20/mo via Vercel Edge); PayOS payment gateway processing fees; targeted social media advertising (10m VND/4 mo); promotional printing. |

### 3.2. Profile of Model Files and Core Algorithms in Project Source Code
All technical architecture details described herein are extracted directly and 100% verified against the operational production codebase of the MotionIQ project (located in `src/features/pose/` and `scripts/uiprmd/`), encompassing seven primary engineering modules:

#### Table 3.2: Profile of Model Files and Core Algorithms in Project Source Code
| Module / File Name | Project Source Code Path | Core Function & Technical Architecture |
| :--- | :--- | :--- |
| **1. uiprmdQualityModel.json** | `src/features/pose/uiprmdQualityModel.json` | Machine Learning model weight file (1,680 JSON lines) storing Z-score normalization parameters (mean, scale), feature weights, and bias for 132 kinematic dimensions evaluated across UI-PRMD exercises (DOI: 10.5281/zenodo.23104965). |
| **2. uiprmdQualityModel.ts** | `src/features/pose/uiprmdQualityModel.ts` | Client-side movement quality inference engine: dynamically maps 33 MediaPipe landmarks to 22 UI-PRMD joints, normalizes by Torso Length, extracts 132 kinematic features, and computes Sigmoid probabilities in browser RAM. |
| **3. train_quality_model.mjs** | `scripts/uiprmd/train_quality_model.mjs` | Offline model training script: reconstructs 3D skeletal frames via Forward Kinematics from Euler rotation angles, applies Subject-Separated cross-validation (train on Subjects 1-8, test on 9-10), and trains L2-Ridge Logistic Regression. |
| **4. fetch_uiprmd.py** | `scripts/uiprmd/fetch_uiprmd.py` | Selective dataset retrieval script: utilizes HTTP Range Requests to download specific kinematic motion files (m01, m05, m06, m07) directly from Zenodo repository without transferring unneeded 400 MB archives. |
| **5. poseService.ts** | `src/features/pose/poseService.ts` | Core computer vision service managing Google MediaPipe Pose Landmarker (WASM/WebGL), automated background prewarming, GPU-to-CPU hardware fallback, and dynamic FPS adaptation for resource-constrained devices. |
| **6. landmarkValidator.ts** | `src/features/pose/landmarkValidator.ts` | Environmental auto-calibration module: measures ambient illumination via ITU-R BT.601 on 32x24 OffscreenCanvas, verifies subject distance ratio (0.35–0.90), and checks visibility of 5 anatomical body regions. |
| **7. angleCalculator.ts & signalSmoother.ts** | `src/features/pose/` | Kinematic calculation and signal filtering engine: computes 3D joint angles via vector dot products, clamps cosine rounding errors, and eliminates limb tremors using One-Euro Filter + EMA + 45° Jump Gate. |

### 3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline
To resolve the three fundamental barriers hindering home exercise adoption among the elderly—namely: (1) privacy hesitation regarding living space exposure, (2) lack of expensive discrete GPUs on common household phones or laptops, and (3) physiological limb tremors distorting sensor readings—MotionIQ is architected around a 100% On-Device Edge AI pipeline structured in four closed-loop layers.

### 3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)
The computer vision subsystem (`poseService.ts`) leverages `@mediapipe/tasks-vision` (v0.10.18) compiled to WebAssembly (WASM) and accelerated by WebGL directly within the client browser environment:
- **33-Landmark Pose Landmarker Lite (Float16 Quantized):** Operating in continuous video stream mode (`runningMode: 'VIDEO'`, `numPoses: 1`), the model simultaneously generates two coordinate systems per frame: (1) Normalized 2D/3D landmarks in domain `[0, 1]` for real-time skeleton overlay rendering, and (2) Metric 3D `worldLandmarks` centered at the hip midpoint for accurate physical joint angle trigonometry.
- **Background Prewarming Architecture:** Via `PoseService.prewarm()`, the application pre-initializes the WASM FilesetResolver and preloads model weights into browser HTTP cache upon homepage landing, enabling instantaneous camera start upon entering the AI workout room.
- **Hardware Delegate Fallback:** The pipeline requests GPU delegation by default (`minDetectionConfidence = 0.5`, `minTrackingConfidence = 0.5`). If WebGL context initialization fails on legacy hardware, the system automatically falls back to CPU execution seamlessly without crashing.
- **Dynamic Frame Skipping:** Under `lowFpsCounter >= 2` (FPS < 18 for two consecutive seconds), the system engages `skipAlternateFrames = true`, inferring only on even frames to protect audio guidance fluency. Full 30 FPS inference resumes once frame rate exceeds 26 FPS.
- **Privacy by Design:** Frames are decoded strictly into temporary `HTMLVideoElement` RAM buffers. Once landmarks are extracted, pixel data is instantly garbage-collected. No video frames are ever recorded, stored on disk, or transmitted over network sockets.

### 3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer
Before repetition counting commences, `landmarkValidator.ts` enforces a three-stage automated environment verification routine:

1. **Room Lighting Measurement Algorithm (`checkLighting`):** Draws video frames to an off-screen 32x24 canvas (768 pixels) to compute perceived luminance ($Y$) using standard ITU-R BT.601 broadcast coefficients:

$$Y = \frac{1}{768} \sum_{i=1}^{768} [ 0.299 \times R_i + 0.587 \times G_i + 0.114 \times B_i ]$$

*Where $R_i, G_i, B_i \in [0, 255]$. Thresholds: $Y < 48 \rightarrow$ 'too_dark'; $Y > 225 \rightarrow$ 'too_bright'; $48 \le Y \le 225 \rightarrow$ 'good' (Lighting standard met).*

2. **Standing Distance Estimation Algorithm (`checkDistance`):** Computes the vertical body height proportion within the camera frame across landmarks with visibility > 0.35:

$$\text{bodyHeightRatio} = \max(y_i) - \min(y_i) \quad (\text{with } \text{visibility}_i > 0.35)$$

*Thresholds: $\text{bodyHeightRatio} > 0.90 \rightarrow$ 'too_close' (step back); $\text{bodyHeightRatio} < 0.35 \rightarrow$ 'too_far' (step closer); $0.35 \le \text{ratio} \le 0.90 \rightarrow$ 'ideal' (2–3 meters).*

3. **Body Region Coverage Validation (`validateLandmarks`):** Partitions 33 landmarks into 5 anatomical groups: Head (0, 7, 8), Hands (15, 16), Hips (23, 24), Knees (25, 26), and Feet (27, 28, 29, 30). The system requires region visibility $\ge 0.40$ and overall confidence $> 0.30$ before declaring the exerciser 'ready' to begin counting.

### 3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine
Once landmarks are validated, MotionIQ executes real-time spatial trigonometry and noise filtering across sequential video frames:

- **3D Spatial Joint Angle Calculation Formula (`calculateAngle`):** Given adjacent anatomical landmarks $A$, $B$ (vertex), and $C$, bone vectors $\vec{BA} = A - B$ and $\vec{BC} = C - B$ are formed. To prevent zero-division on degenerate points, vector lengths are bounded ($|\vec{BA}| \ge 10^{-6}$ and $|\vec{BC}| \ge 10^{-6}$), and cosine values are clamped to $[-1.0, 1.0]$:

$$\theta^\circ = \arccos\left( \text{clamp}\left( \frac{\vec{BA} \cdot \vec{BC}}{|\vec{BA}| \times |\vec{BC}|}, -1.0, 1.0 \right) \right) \times \frac{180^\circ}{\pi}$$

*Where $\vec{BA} \cdot \vec{BC} = BA_x \cdot BC_x + BA_y \cdot BC_y + BA_z \cdot BC_z$. Backup 2D projection `calculateAngle2D` is utilized if z-depth confidence is low.*

- **One-Euro Filter & Exponential Moving Average with Jump Gate:** Addresses age-related physiological tremors. Along with the velocity-adaptive One-Euro filter, `signalSmoother.ts` incorporates an Exponential Moving Average (EMA) and 45° Jump Gate:

$$S_t = \alpha \times \theta_t + (1 - \alpha) \times S_{t-1} \quad (\text{smoothing factor } \alpha = 0.3, \text{ impulse threshold } \text{maxJump} = 45^\circ)$$

*Jump Gate Logic: If $|\theta_t - S_{t-1}| > 45^\circ$, the deviation is treated as noise unless sustained over $\ge 3$ consecutive frames (`consecutiveJumps >= 3`).*

- **Repetition State Machine with Hysteresis:** Strict 7-state transitions govern repetition counting:
  $$\text{IDLE} \rightarrow \text{READY} \rightarrow \text{DESCENDING} \rightarrow \text{BOTTOM} \rightarrow \text{ASCENDING} \rightarrow \text{TOP} \rightarrow \text{COMPLETE}$$
  A hysteresis angle threshold (`hysteresisDeg`) and minimum holding frames (`minHoldFrames`) prevent phantom rep counts from camera shake.

### 3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset (`uiprmdQualityModel`)
A distinguishing innovation of MotionIQ is supplementing heuristic angle thresholds with an empirical Machine Learning movement quality model trained on the international UI-PRMD dataset (University of Idaho - Physical Rehabilitation Movement Dataset, DOI: 10.5281/zenodo.23104965). The pipeline spans four algorithmic stages:

- **Stage 1: Forward Kinematics Reconstruction & Joint Mapping:** Maps 33 MediaPipe landmarks to 22 standard UI-PRMD Kinect joints:

#### Table 3.2-Joints: 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics
| UI-PRMD Joint Index & Anatomical Region | MediaPipe Landmark Source (33 Points) | Mathematical Interpolation / Mapping Rule |
| :--- | :--- | :--- |
| **Joint 0: Waist (Lower Spine / Root)** | Midpoint of LEFT_HIP (23) & RIGHT_HIP (24) | $[(x_{23}+x_{24})/2, (y_{23}+y_{24})/2, (z_{23}+z_{24})/2] \rightarrow \text{Origin } (0,0,0)$ |
| **Joint 1: Mid Spine** | 50% Linear Interpolation: Waist to Chest | $\text{interpolate}(\text{Waist}, \text{Chest}, 0.5)$ |
| **Joint 2: Chest (Center of Thorax)** | Midpoint of LEFT_SHOULDER (11) & RIGHT_SHOULDER (12) | $[(x_{11}+x_{12})/2, (y_{11}+y_{12})/2, (z_{11}+z_{12})/2]$ |
| **Joint 3: Neck** | 50% Linear Interpolation: Chest to Nose (0) | $\text{interpolate}(\text{Chest}, \text{Nose}, 0.5)$ |
| **Joints 4 & 5: Head & Head Tip** | Landmark NOSE (0) | $[x_0, y_0, z_0]$ |
| **Joints 6, 7, 8, 9: Left Upper Limb** | Left Shoulder (11) → Elbow (13) → Wrist (15) → Index (19) | 4-joint kinematic chain of left arm |
| **Joints 10, 11, 12, 13: Right Upper Limb** | Right Shoulder (12) → Elbow (14) → Wrist (16) → Index (20) | 4-joint kinematic chain of right arm |
| **Joints 14, 15, 16, 17: Left Lower Limb** | Left Hip (23) → Left Knee (25) → Left Ankle (27) → Left Toe (31) | 4-joint kinematic chain of left leg |
| **Joints 18, 19, 20, 21: Right Lower Limb** | Right Hip (24) → Right Knee (26) → Right Ankle (28) → Right Toe (32) | 4-joint kinematic chain of right leg |

- **Stage 2: Torso-Length Spatial Normalization:** Translates all joints to Waist origin and normalizes by 3D Torso Length (Euclidean distance from Waist to Chest, requiring $\text{torsoLength} \ge 0.05$), yielding a scale-invariant 66-dimensional vector per frame (22 joints × [X, Y, Z]):

$$\text{torsoLength} = \sqrt{ (x_{\text{chest}} - x_{\text{waist}})^2 + (y_{\text{chest}} - y_{\text{waist}})^2 + (z_{\text{chest}} - z_{\text{waist}})^2 }$$
$$P'_j = \frac{P_j - \text{Waist}}{\text{torsoLength}} \quad (\text{for } j = 0..21)$$

*Ensures identical posture classification regardless of participant height or camera distance.*

- **Stage 3: Kinematic Time-Series Pooling into 132-Dimensional Feature Vector:** For repetition length $T \ge 5$ frames, `summarizeFrames()` compresses the sequence into a fixed 132-dimensional vector combining Mean ($\mu$) and Standard Deviation ($\sigma$) across all 66 joint coordinates:

$$\mu_i = \frac{1}{T} \sum_{t=1}^T f_{t,i} \quad ; \quad \sigma_i = \sqrt{ \frac{1}{T} \sum_{t=1}^T (f_{t,i} - \mu_i)^2 }$$
$$\text{Feature Vector } X = [ \mu_1..\mu_{66}, \sigma_1..\sigma_{66} ] \in \mathbb{R}^{132}$$

*Indices 0..65 reflect average postural alignment; Indices 66..131 capture dynamic Range of Motion trajectory variance.*

- **Stage 4: L2-Regularized Logistic Regression Training & Classification Inference:** Evaluates movement quality using Ridge Logistic Regression trained on 200 real motion sequences per exercise from UI-PRMD (100 correct, 100 compensatory). Validation enforces strict Subject-Separated splitting (train on Subjects 1–8; evaluate on unseen Subjects 9 & 10):

$$\text{logit}(z) = \text{bias} + \sum_{i=1}^{132} \left[ \text{weights}_i \times \frac{x_i - \text{mean}_i}{\text{scale}_i} \right]$$
$$P(\text{correct}) = \text{sigmoid}(z) = \frac{1}{1 + \exp(-z)}$$

*Classification Rules: $P \ge 0.70 \rightarrow$ 'good' (Correct posture); $P \le 0.30 \rightarrow$ 'needs_adjustment' (Compensatory movement); $0.30 < P < 0.70 \rightarrow$ 'uncertain'.*

#### Table 3.2a: Actual Parameters Extracted from Weights File uiprmdQualityModel.json
| Motion Name | UI-PRMD | Features | Bias | Weight Range | Held-out Test Set | Accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sit-to-Stand** | m05 | 132 | -0.9520 | [-0.7312, +0.4409] | 40 samples (20 Correct / 20 Incorrect) | 95.0% |
| **Functional Squat** | m01 | 132 | -0.3258 | [-0.5929, +0.8224] | 40 samples (20 Correct / 20 Incorrect) | 72.5% |
| **Shoulder Abduction** | m07 | 132 | -0.8338 | [-0.5428, +0.8700] | 40 samples (20 Correct / 20 Incorrect) | 97.5% |
| **Side Leg Raise** | m06 | 132 | -0.9935 | [-0.7763, +0.6137] | 40 samples (20 Correct / 20 Incorrect) | 97.5% |
| **SYSTEM AVERAGE** | 4 actions | 132 dims | — | — | 160 total samples (Subj 9, 10) | **90.62%** |

### 3.3. 4 Standardized Functional Exercise Movements

#### 3.3.1. Principles of Exercise Standardization Based on 3 International Motion Datasets
MotionIQ strictly restricts its exercise library to functional movements verified across three established public motion research corpora:
1. **UI-PRMD Dataset (University of Idaho, DOI: 10.5281/zenodo.23104965):** Provides 3D skeletal data across 10 subjects with clinical annotation of correct and compensatory movement executions.
2. **KIMORE Dataset (Kinematic Assessment of Movement and Clinical Scores for Remote Monitoring):** Comprises kinematic recordings from 78 subjects (healthy and motor-impaired), serving as the empirical baseline for target Range of Motion (Target ROM) boundaries.
3. **EHE Dataset (Elderly Home Exercise Dataset):** Encompasses 869 repetitions from 25 elderly individuals, providing empirical calibration for repetition pacing, holding delays (`minHoldFrames`), and geriatric velocity thresholds.

#### 3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises
1. **Exercise 1: Sit-to-Stand (UI-PRMD: m05 | KIMORE: Es4):**
   - *Functional Objective:* Lower limb power, quadriceps strength, and independent functional mobility for daily chair and bed transfers.
   - *Kinematic Angles:* Measures bilateral knee flexion (Hip 23/24 – Knee 25/26 – Ankle 27/28) and hip flexion. Target ROM: Seated knee flexion (90°–125°) to full upright stance (165°–180°).
   - *UI-PRMD Model Parameters (bias = -0.9520):* Tracks knee vertical displacement (mean $\sigma_Y = 0.7287\text{--}0.7586$) and trunk tilt. Detects excessive forward leaning or asymmetric leg loading. Validation accuracy: 95.0% (38/40 samples).
2. **Exercise 2: Controlled Functional Squat (UI-PRMD: m01 | KIMORE: Es5 | EHE: Squat):**
   - *Functional Objective:* Quadriceps and gluteal strengthening, knee-ankle joint stabilization, reducing stair-climbing fall risks.
   - *Kinematic Angles:* Simultaneously evaluates knee angle and trunk inclination. Target ROM: Controlled descent to safe geriatric depth (90°–125°), avoiding deep knee hyperflexion.
   - *UI-PRMD Model Parameters (bias = -0.3258):* Identifies knee valgus (knees caving inward) and anterior trunk collapse. Validation accuracy: 72.5% (29/40 samples).
3. **Exercise 3: Standing Shoulder Abduction (UI-PRMD: m07 | KIMORE: Es1 | EHE: LA):**
   - *Functional Objective:* Restores shoulder joint Range of Motion, counteracts frozen shoulder, improves chest expansion for respiratory vitality.
   - *Kinematic Angles:* Tracks coronal shoulder abduction angle (Hip 23/24 – Shoulder 11/12 – Elbow 13/14). Target ROM: Neutral (0°–20°) to lateral raise (90°–150°).
   - *UI-PRMD Model Parameters (bias = -0.8338):* Confirms lower-body stability (knee/ankle $\sigma$ near 0) while detecting compensatory shoulder shrugging or spinal lateral flexion. Validation accuracy: 97.5% (39/40 samples).
4. **Exercise 4: Standing Side Leg Raise (UI-PRMD: m06 | Hip Abduction):**
   - *Functional Objective:* Strengthens gluteus medius and tensor fasciae latae, critical for lateral pelvic stability during single-leg stance and preventing sideways falls.
   - *Kinematic Angles:* Measures hip abduction angle while ensuring stance leg remains upright (knee $\ge 165^\circ$). Target ROM: Hip abduction reaching 30°–45°.
   - *UI-PRMD Model Parameters (bias = -0.9935):* Contrasts high active leg variance against low stance leg variance, detecting compensatory trunk tipping. Validation accuracy: 97.5% (39/40 samples).

#### Table 3.3: Summary Table of 4 Standardized Functional Exercises in MotionIQ
| Exercise & Code | Dataset Code | Primary Landmarks | Target ROM | Compensatory Errors Detected | Model Parameters |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Sit-to-Stand**<br>`(sit-to-stand)` | UI-PRMD: m05<br>KIMORE: Es4 | Hips (23, 24)<br>Knees (25, 26)<br>Ankles (27, 28) | Knee: 90°–125° (seated) → 165°–180° (stand) | Excessive trunk leaning; asymmetric leg push; incomplete knee extension. | Bias: -0.9520<br>Accuracy: 95.0%<br>(38/40 test) |
| **2. Functional Squat**<br>`(squat)` | UI-PRMD: m01<br>KIMORE: Es5<br>EHE: Squat | Shoulders (11, 12)<br>Hips (23, 24)<br>Knees (25, 26) | Knee: 90°–125° (safe depth; upright back) | Knee valgus (caving inward); shallow squat; forward head tilt. | Bias: -0.3258<br>Accuracy: 72.5%<br>(29/40 test) |
| **3. Shoulder Abduction**<br>`(shoulder-raise)` | UI-PRMD: m07<br>KIMORE: Es1<br>EHE: LA | Hips (23, 24)<br>Shoulders (11, 12)<br>Elbows (13, 14) | Shoulder: 90°–150° (lateral abduction) | Shoulder shrugging; elbow flexion; contralateral torso tilt. | Bias: -0.8338<br>Accuracy: 97.5%<br>(39/40 test) |
| **4. Side Leg Raise**<br>`(side-leg-raise)` | UI-PRMD: m06 | Hips (23, 24)<br>Knees (25, 26)<br>Ankles (27, 28) | Hip: 30°–45° (stance knee $\ge 165^\circ$) | Knee flexion on active leg; torso leaning toward stance leg. | Bias: -0.9935<br>Accuracy: 97.5%<br>(39/40 test) |

*Safety Limit Notice: MotionIQ is strictly a supportive tool for monitoring home functional movement via standard mobile/laptop cameras. Joint angle metrics and movement quality assessment scores serve as physical activity tracking references and do not replace medical diagnosis, clinical evaluation, or direct care from licensed physical therapists.*

### 3.4. Results of 5 Actual MVP Prototype Testing Sessions
The MotionIQ team deployed the live MVP prototype across five comprehensive physical testing sessions in Can Tho City with elderly citizens and wellness trainers:

#### Table 3.4: Results of 5 Actual MVP Prototype Testing Sessions
| Experimental Measurement Metric | Actual Result | Evaluation Notes |
| :--- | :--- | :--- |
| **Range of Motion (ROM) Measurement Accuracy** | 94.6% | Compared with standard manual goniometric reference angles. |
| **Algorithmic Response Latency** | 38 ms / frame | Meets real-time 25–30 FPS standard; voice prompts and rep counts are not delayed. |
| **System Usability Scale (SUS) Usability Score** | 84.5 / 100 points | Exceptional user satisfaction and geriatric accessibility (Grade A / Excellent). |

---

## CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (CHECKPOINT 3)
*[Lead Author & Editor: Mã Phú Tín — Growth & Media Lead]*

### 4.1. 04-Month Media Objectives
During the four months of implementation, MotionIQ executes a focused, cost-effective communication campaign tailored for student capabilities:
- **Objective 1 (Brand Awareness):** Establish MotionIQ brand awareness across Can Tho City and the Southwestern region via short-form video.
- **Objective 2 (Targeted Outreach):** Reach 150–180 high-intent families with elderly relatives needing guided home exercise.
- **Objective 3 (Product Trial):** Onboard 40–50 trial households to test the live web app and collect qualitative user experience feedback.
- **Objective 4 (Paid Customer Conversion):** Convert 15–20 initial paying subscribers by Month 4, establishing recurring cash flow.

### 4.2. Target Customers & Key Message
- **Primary Target Customers:** Working children/grandchildren aged 25–40, digitally proficient, seeking peace of mind regarding their aging parents' physical activity.
- **Direct End-Users:** Elderly citizens (aged 60+) who desire gentle physical activity at home with large, intuitive controls and zero technical frustration.
- **Core Brand Message:** "MotionIQ – Home exercise, movement tracking made easier." (Exercise joyfully, move correctly, live vibrantly with Bé Nấm).

### 4.3. Communication Channels & Methods

#### Table 4.1: Communication Channels & Operational Implementation Methods
| Media Channel | Actual Operational Implementation Method |
| :--- | :--- |
| **TikTok** | Produce short-form videos dramatizing the working child's dilemma, side-by-side exercise demos with Bé Nấm, and AI rep-counting showcases. |
| **Facebook** | Build the official Fanpage, share geriatric wellness knowledge, post authentic trial testimonials, and engage in local Can Tho family groups. |
| **Zalo** | 1-on-1 customer onboarding, sending video user guides, providing technical support, and managing subscription renewals. |
| **Direct (Community)** | Host interactive live trial booths at local senior clubs, retirement associations, and community pagodas in Can Tho. |

### 4.4. 04-Month Media Implementation Roadmap

#### Table 4.2: 4-Month Communication Implementation Roadmap
| Implementation Stage | Key Strategic Activities | Measurable Target Milestone |
| :--- | :--- | :--- |
| **Month 1: Brand Awareness Building** | Finalize Fanpage, TikTok channel, and Bé Nấm mascot brand assets; produce introduction videos and foundational content. | Establish initial brand awareness; achieve 3,000+ views across Can Tho. |
| **Month 2: Customer Acquisition** | Post feature breakdown videos, address home exercise difficulties, launch targeted social ads, collect trial registrations. | Expand reach; acquire 150–180 high-potential leads. |
| **Month 3: Experience & Trust** | Organize free community trial workshops, provide usage guidance, collect feedback, publish user demo clips, validate pricing. | Prove product efficacy; build trust with 40–50 active trial households. |
| **Month 4: Conversion & Revenue** | Launch official paid subscription packages, offer introductory promotions, deliver attentive support, deploy referral rewards. | Convert 15–20 paying customers; generate sustainable initial cash flow. |

### 4.5. Value-Based & Competitive Parity Pricing Strategy
MotionIQ applies Customer Value-Based Pricing synthesized with Competitive Parity and Cost-Based break-even safeguards:
- **Customer Value-Based:** In our field survey of N = 50 respondents, 64.7% accepted a monthly subscription fee between 50,000 and 149,000 VND/month. MotionIQ's introductory tier is positioned under 100,000 VND/month to maximize adoption among working children.
- **Competitive Parity:** Free YouTube videos offer no feedback or safety checks, whereas private in-home personal trainers charge 200,000–400,000 VND/session. MotionIQ delivers automated AI posture guidance and voice rep-counting at a tiny fraction of trainer fees.
- **Cost-Based Safeguard:** Pricing is structured to comfortably cover server hosting and operational overhead with a lean subscriber base.

#### Table 4.3: Proposed Pricing Structure of MotionIQ
| Service Package | Listed Selling Price | Privileges & Usage Benefits |
| :--- | :--- | :--- |
| **MotionIQ Free** | Free Forever | Experience basic exercises, real-time AI repetition counting, standard visual guidance. |
| **MotionIQ Early Access** | 49,000 VND / month | Limited to first 20 subscribers: unlocks advanced functional exercises, personalized Bé Nấm voice settings. |
| **MotionIQ Standard** | 79,000 VND / month | Full expanded exercise library, historical workout analytics, weekly progress reports sent via Zalo. |
| **MotionIQ Annual** | 790,000 VND / year | Saves 2 months of subscription fees, priority 1-on-1 technical support, permanent price guarantee. |

### 4.6. Budget Estimation and Operating Costs
To execute the four-month market approach plan, the team allocates a disciplined student media budget of 10,000,000 VND:

#### Table 4.4: 4-Month Lean Student Media Budget Allocation (10,000,000 VND)
| 04-Month Media Budget Item | Estimated Cost (VND) |
| :--- | :--- |
| **Media content production (promotional images, exercise demonstration videos)** | 3,000,000 VND |
| **Selective targeted advertising on Facebook and TikTok** | 3,000,000 VND |
| **Organizing direct product experience workshops at senior citizen clubs** | 2,000,000 VND |
| **Travel, local transportation, and customer contact expenses in Can Tho** | 700,000 VND |
| **Printing QR Code brochures and introductory user guide leaflets** | 300,000 VND |
| **Contingency and emergency reserve budget** | 1,000,000 VND |
| **TOTAL 04-MONTH MEDIA BUDGET** | **10,000,000 VND** |

**System Operational Cost Assumptions:**
- **Fixed Cost (FC):** 1,000,000 VND / month (maintaining lightweight cloud hosting via Vercel Edge, database server, custom domain name, and technical development tools).
- **Variable Cost (VC):** 10,000 VND / subscription / month (PayOS / MoMo online payment processing fees, Zalo notification messaging API, and network bandwidth).

### 4.7. Revenue Development Plan & KPI Targets after 04 Months
MotionIQ implements a 5-Step Customer Conversion Funnel (Reach → Interest → Trial → Conversion → Retention):

#### Table 4.5: Target Customer Segments & 4-Month Conversion Funnel KPIs
| Funnel Stage & Performance Metric | Target after 04 Months | Strategic Evaluation Meaning |
| :--- | :--- | :--- |
| **1. Social Media Reach** | 13,000 – 15,000 reaches | Establishes initial brand awareness across target communities. |
| **2. Potential Leads (Inquiries)** | 150 – 180 leads | Conversion rate achieves ~1.1% – 1.2% from gross reach. |
| **3. Users Registering for Trial** | 40 – 50 people | Trial conversion rate reaches ~27% from the qualified lead pool. |
| **4. Users Completing Trial Process** | 30 – 35 people | Completion rate achieves ~70% – 75% of trial participants. |
| **5. Customers Converting to Paid** | 15 – 20 customers | Conversion rate achieves ~50% of completed trial users. |

**Customer Acquisition Cost (CAC) Assessment:**
With a total media budget of 10,000,000 VND and a target of 15–20 initial paying customers, the allocated marketing cost averages approximately 500,000 – 666,667 VND / customer. This is an entirely standard investment ratio during the initial Product Validation Phase, as the expenditure simultaneously builds lasting brand equity and establishes a verified potential customer file for subsequent organic expansion.

### 4.8. Revenue Forecast and Break-Even Analysis
Initial monthly revenue forecast from the Early Access subscription tier (49,000 VND / month):

#### Table 4.6: Early Access Tier Subscription Monthly Revenue Forecast
| Number of Active Paying Customers | Estimated Monthly Recurring Revenue (49k Package) |
| :--- | :--- |
| **10 subscribers** | 490,000 VND / month |
| **15 subscribers** | 735,000 VND / month |
| **20 subscribers** | 980,000 VND / month |

**Break-Even Analysis:**  
The break-even subscription count is calculated using standard corporate finance formulas:

$$Q_{\text{BE}} = \frac{\text{Fixed Costs}}{\text{Selling Price} - \text{Variable Cost per Subscription}} = \frac{FC}{P - VC}$$

*Assuming Fixed Costs (FC) = 1,000,000 VND/month and Variable Cost (VC) = 10,000 VND/subscription/month.*

#### Table 4.7: Operational Break-Even vs. Full Capital Recovery Analysis
| Break-Even Analysis Metric | Early Access Package (49,000 VND) | Standard Package (79,000 VND) |
| :--- | :--- | :--- |
| **Unit Contribution Margin (P - VC)** | 39,000 VND / subscriber | 69,000 VND / subscriber |
| **Subscribers to break even monthly operations (FC = 1,000,000 VND)** | **26 subscribers** | **15 subscribers** |
| **Subscribers to fully recover 10m media budget over 4 months** | 90 subscribers / month | 51 subscribers / month |

**Financial Assessment from the Implementation Team:**  
With the target of 15–20 paying customers in Month 4, MotionIQ generates 735,000 – 980,000 VND in MRR, covering nearly 100% of monthly fixed operational costs. While this initial cohort does not yet fully recover the sunk 10 million VND marketing budget within the first four months, this is fully consistent with early-stage tech startup dynamics, where initial marketing establishes brand equity and customer acquisition funnels.

Crucially, reaching the milestone of just 26 Early Access subscribers (or 15 Standard subscribers) allows MotionIQ to achieve complete **Operational Self-Sufficiency**, funding 100% of server and maintenance infrastructure without requiring ongoing founder out-of-pocket subsidies.

> **📌 FINANCIAL STRATEGY HIGHLIGHTS & OPERATIONAL AUTONOMY**  
> - **Nature of CAC vs. LTV:** The initial CAC (500,000 – 666,667 VND) represents an upfront investment to reach 13,000–15,000 views. Under our subscription model, Customer Lifetime Value (LTV) reaches 588,000 – 790,000 VND when subscribers retain for 12 months or more, guaranteeing LTV > CAC and sustainable unit economics.  
> - **Operational Self-Sufficiency:** Reaching 26 Early Access subscribers proves operational survival, generating sufficient recurring cash flow to maintain server infrastructure indefinitely while expanding organically through family word-of-mouth.

---

## CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY (CHECKPOINT 3)
*[Lead Author & Editor: Hồ Tuyết Nghi — Service Management Lead (CMO)]*

### 5.1. Identification of Practical Risks & Mitigation Measures
To ensure that MotionIQ operates safely, transparently, and in strict compliance with applicable regulations, the team has identified seven primary operational risks and established actionable mitigation strategies for each:

#### Table 5.1: Identified Operational Risk Matrix & Concrete Mitigation Strategies
| Identified Operational Risk | Concrete Actionable Mitigation Strategy |
| :--- | :--- |
| **1. Elderly users experiencing difficulty operating digital technology** | Implement ultra-simplified Geriatric UX: font size ≥ 18px, large high-contrast touch buttons (≥ 56px), natural Vietnamese audio prompts with adjustable volume, and one-touch start. |
| **2. Sensor noise and inaccurate AI joint angle recognition** | Incorporate adaptive One-Euro Filter to eradicate physiological limb tremors, enforce automated 3-step environment calibration, and provide visual camera placement guides. |
| **3. Customer reluctance to transition to paid subscription** | Provide permanent free access to basic functional routines, communicate clear value benefits of advanced tracking, and price introductory tier at an accessible 49,000 VND/month. |
| **4. High initial Customer Acquisition Cost (CAC)** | Focus on organic community outreach, leverage word-of-mouth referral incentives ('Share with a Friend' free month), and partner directly with local senior citizen clubs in Can Tho. |
| **5. User churn and exercise abandonment after short trial period** | Design habit-forming streak rewards, provide weekly progress summaries via Zalo, and maintain warm, empathetic companionship through the Bé Nấm virtual mascot. |
| **6. Risk of platform misclassification as a medical device** | Maintain prominent non-medical disclaimers across all screens: clearly position MotionIQ as an assistive physical wellness support tool, explicitly stating it does not provide clinical diagnosis or replace medical doctors. |
| **7. Personal data privacy and video camera exposure risks** | Enforce 100% On-Device AI architecture: all video frames are processed solely in local browser RAM and discarded immediately. No video streams or biometric images are ever saved or transmitted to cloud servers. |

### 5.2. Development and Sustainability Plan by Phase
MotionIQ pursues a phased, systematic sustainability and development roadmap:
- **Phase 1 — First 4 Months (Validation & Community Launch):** Finalize MVP web application, optimize geriatric UX, onboard 40–50 trial households, validate willingness to pay at 49,000 VND/month, and secure initial 15–20 paying subscribers to achieve operational break-even.
- **Phase 2 — Months 5–6 (Stabilization & Optimization):** Enhance voice guidance quality, evaluate subscription retention rates, introduce the Standard tier (79,000 VND/month), and refine unit economics.
- **Phase 3 — Next Expansion Phase (Platform Ecosystem):** Expand exercise catalog with gentle wrist and ankle routines, automate weekly exercise reports to adult children via Zalo, explore Zalo Mini App integration (eliminating app installation barriers), and evaluate B2B institutional partnerships with local elderly day care and community centers.

### 5.3. Project Limitations and Future Technological Roadmap
While MotionIQ demonstrates robust performance, several technological limitations are acknowledged:
- **Single 2D Camera Depth Invariant:** Relying on monocular smartphone webcams inherently estimates 3D depth. Future versions will integrate multi-view spatial calibration algorithms to improve depth precision.
- **Extreme Ambient Lighting Variations:** Low-light environments (< 48 luminance) impact computer vision accuracy. The system enforces automated warnings prompting users to adjust lighting or room positioning.
- **Hardware Fragmentation:** Performance varies across legacy mobile browsers. The team plans to build a dedicated lightweight progressive web app (PWA) with enhanced offline caching.

---

## CONCLUSION
*[Lead Author & Editor: Huỳnh Thị Yến Duy — Project Lead (CEO)]*

MotionIQ addresses a poignant, widespread societal challenge facing modern Vietnamese families: empowering elderly parents to maintain regular physical activity safely and joyfully at home while giving their hard-working adult children complete peace of mind.

Through a disciplined, humble, and evidence-based approach—grounded in empirical field insights from 50 survey respondents, 5 physical prototype testing sessions achieving 94.6% ROM accuracy and an 84.5 SUS score, and a lean 10,000,000 VND communication strategy—MotionIQ proves that advanced On-Device AI can be translated into an accessible, humane, and economically sustainable product. Reaching operational break-even at just 26 subscribers establishes a self-funding foundation, enabling the founding team to scale MotionIQ into an enduring student startup with profound social impact.
"""

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[SUCCESS] Markdown written to: {out_path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Output file targets
    docx_rel = os.path.join(base_dir, "MotionIQ_Final_Report_EXE101_EN.docx")
    md_rel = os.path.join(base_dir, "MotionIQ_Final_Report_EXE101_EN.md")
    
    docx_final_rel = os.path.join(base_dir, "Final_MOTIONIQ.docx")
    md_final_rel = os.path.join(base_dir, "Final_MOTIONIQ.md")
    
    public_docx = os.path.join(base_dir, "public", "MotionIQ_Final_Report_EXE101_EN.docx")
    public_md = os.path.join(base_dir, "public", "MotionIQ_Final_Report_EXE101_EN.md")
    public_docx_final = os.path.join(base_dir, "public", "Final_MOTIONIQ.docx")
    public_md_final = os.path.join(base_dir, "public", "Final_MOTIONIQ.md")
    
    user_downloads_docx = r"C:\Users\PC\Downloads\MotionIQ_Final_Report_EXE101_EN.docx"
    user_downloads_final_docx = r"C:\Users\PC\Downloads\Final_MOTIONIQ.docx"
    
    artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a"
    artifact_docx = os.path.join(artifact_dir, "MotionIQ_Final_Report_EXE101_EN.docx")
    artifact_md = os.path.join(artifact_dir, "MotionIQ_Final_Report_EXE101_EN.md")
    artifact_final_docx = os.path.join(artifact_dir, "Final_MOTIONIQ.docx")
    artifact_final_md = os.path.join(artifact_dir, "Final_MOTIONIQ.md")

    print("Building English DOCX Report...")
    build_docx(docx_rel)
    
    print("Building English Markdown Report...")
    build_markdown(md_rel)
    
    # Copy to Final_MOTIONIQ.docx & .md locally
    shutil.copy2(docx_rel, docx_final_rel)
    shutil.copy2(md_rel, md_final_rel)
    
    # 2. Distribute to public/
    os.makedirs(os.path.join(base_dir, "public"), exist_ok=True)
    shutil.copy2(docx_rel, public_docx)
    shutil.copy2(md_rel, public_md)
    shutil.copy2(docx_rel, public_docx_final)
    shutil.copy2(md_rel, public_md_final)
    print(f"[SUCCESS] Replicated to public folder: {public_docx} and {public_docx_final}")
    
    # 3. Distribute to User Downloads
    try:
        shutil.copy2(docx_rel, user_downloads_docx)
        shutil.copy2(docx_rel, user_downloads_final_docx)
        print(f"[SUCCESS] Replicated to user Downloads: {user_downloads_final_docx}")
    except Exception as e:
        print(f"[WARNING] Could not copy to user Downloads: {e}")
        
    # 4. Distribute to Artifacts folder
    try:
        shutil.copy2(docx_rel, artifact_docx)
        shutil.copy2(md_rel, artifact_md)
        shutil.copy2(docx_rel, artifact_final_docx)
        shutil.copy2(md_rel, artifact_final_md)
        print(f"[SUCCESS] Replicated to Artifact directory: {artifact_final_docx}")
    except Exception as e:
        print(f"[WARNING] Could not copy to Artifact directory: {e}")

    print("\nAll English Report documents generated and synchronized successfully!")

if __name__ == "__main__":
    main()
