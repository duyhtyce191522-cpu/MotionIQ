# -*- coding: utf-8 -*-
"""
Full English Report Generator for MotionIQ (EXE101 - FPT University Can Tho)
Generates:
1. MotionIQ_Final_Report_EXE101_EN.docx (Formatted Academic Word Document)
2. MotionIQ_Final_Report_EXE101_EN.md (Comprehensive Markdown Document)
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

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
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
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(140, 47, 30)
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(178, 66, 45)
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(60, 60, 60)
    return p

def add_callout_box(doc, text, title="STRATEGIC FINANCIAL TAKEAWAY & OPERATIONAL SELF-SUFFICIENCY"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.3)
    set_cell_background(cell, "FBF8F5")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
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
    p_spacer.paragraph_format.space_before = Pt(4)
    p_spacer.paragraph_format.space_after = Pt(4)

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

    # 1. Page Margins (Academic Standard: Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # ~2.0 cm
        section.bottom_margin = Inches(0.79)  # ~2.0 cm
        section.left_margin = Inches(1.18)   # ~3.0 cm
        section.right_margin = Inches(0.79)   # ~2.0 cm
        section.different_first_page_header_footer = True

        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hr = hp.add_run("MOTIONIQ — Comprehensive Entrepreneurship Project Report (Course EXE101)")
        hr.font.name = "Times New Roman"
        hr.font.size = Pt(9)
        hr.font.italic = True
        hr.font.color.rgb = RGBColor(120, 120, 120)

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

    # 2. Base Typography Styles
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(13)
    font_normal.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # COVER PAGE
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("MINISTRY OF EDUCATION AND TRAINING\nFPT UNIVERSITY CAN THO CAMPUS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(70, 70, 70)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(16)
    r_line = p_line.add_run("———————————————***———————————————")
    r_line.font.bold = True
    r_line.font.color.rgb = RGBColor(178, 66, 45)

    p_title_sub = doc.add_paragraph()
    p_title_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_title_sub.add_run("FINAL ENTREPRENEURSHIP PROJECT REPORT\nCOURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(178, 66, 45)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(14)
    r_title = p_title.add_run("MOTIONIQ — ON-DEVICE AI MOTION TRACKING PLATFORM FOR ELDERLY HOME CARE\n(100% ON-DEVICE AI)")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(140, 47, 30)

    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(28)
    r_tag = p_tag.add_run('"MotionIQ – Exercise at home, motion tracking made simpler."\n(Consolidated: Checkpoint 1 • Checkpoint 2 • Checkpoint 3 • Marketing & Financial Revenue Strategy)')
    r_tag.font.name = "Times New Roman"
    r_tag.font.italic = True
    r_tag.font.size = Pt(11)
    r_tag.font.color.rgb = RGBColor(100, 100, 100)

    # Info table on cover
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    set_table_borders(info_table, color="D4C5B9", sz="4")
    col_widths = [Inches(2.3), Inches(4.0)]
    
    info_data = [
        ("Academic Advisor:", "Mr. Tran Ngoc Son"),
        ("Student Team:", "MOTIONIQ — Cohort K19"),
        ("Project Lead & CEO:", "Huynh Thi Yen Duy — Student ID: CE191522"),
        ("Founding Members:", "Nguyen Hai Ha (CTO) • Nguyen Nha Quan (CPO)\nMa Phu Tin • Dang Vinh Phuc • Ho Tuyet Nghi (CMO)"),
        ("Live MVP Web Application:", "https://motion-iq-five.vercel.app"),
        ("Empirical Fieldwork:", "50 Quantitative Field Surveys • 5 Live Prototype Testing Sessions")
    ]

    for idx, (lbl, val) in enumerate(info_data):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width, cell_val.width = col_widths[0], col_widths[1]
        set_cell_margins(cell_lbl, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cell_val, top=80, bottom=80, left=120, right=120)
        set_cell_background(cell_lbl, "F8F5F2")
        set_cell_background(cell_val, "FFFFFF")
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.name = "Times New Roman"
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGBColor(60, 60, 60)
        
        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        if "http" in val:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(178, 66, 45)

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(32)
    r_bot = p_bottom.add_run("CAN THO CITY, NOVEMBER 2026")
    r_bot.font.name = "Times New Roman"
    r_bot.font.bold = True
    r_bot.font.size = Pt(12)
    r_bot.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # ACKNOWLEDGEMENTS
    # ==========================================
    add_h1(doc, "ACKNOWLEDGEMENTS")
    add_p(
        doc,
        "The MotionIQ project team wishes to express our deepest gratitude and sincerest appreciation to our instructor, "
        "Mr. Tran Ngoc Son, who has dedicated his profound expertise, innovative entrepreneurial thinking, and structured guidance "
        "to mentor our team throughout Checkpoint 1, Checkpoint 2, and Checkpoint 3 of Course EXE101 (Experiential Entrepreneurship)."
    )
    add_p(
        doc,
        "We also extend our heartfelt thanks to the elderly citizens and families across Can Tho City and the Mekong Delta region who "
        "generously participated in our 50 quantitative field surveys and 5 in-person physical prototype testing sessions. Your authentic "
        "feedback, enthusiastic encouragement, and honest critiques have served as the guiding compass enabling us to develop an assistive "
        "technology platform that is not only technically robust but also deeply humane, empathetic, and culturally tailored."
    )

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================
    add_h1(doc, "EXECUTIVE SUMMARY")
    add_p(
        doc,
        "MotionIQ is an assistive AI computer vision technology platform engineered to run 100% on-device (Edge AI) via standard web browsers. "
        "The solution is designed specifically to support elderly citizens in tracking their daily physical movement, functional mobility exercises, "
        "and balance routines at home through standard smartphone or laptop webcams—eliminating the need for expensive wearable hardware sensors or external devices."
    )
    add_p(
        doc,
        "By integrating an endearing virtual assistant mascot named 'Bé Nấm' (Little Mushroom) with natural, real-time Vietnamese voice guidance, "
        "biomechanical kinematic models trained on published human movement datasets (UI-PRMD, KIMORE, EHE), and dynamic One-Euro Filter jitter smoothing, "
        "MotionIQ assists seniors in maintaining correct exercise postures, accurately counts repetitions, and delivers immediate supportive feedback. "
        "Empirical field research across N = 50 target respondents revealed that over 68% of adult children face severe scheduling constraints that prevent "
        "them from directly observing their aging parents' exercises, while 82.4% expressed high willingness to trial our home-based digital platform. "
        "Live testing across 5 prototype evaluation sessions demonstrated a 94.6% Range of Motion (ROM) angular measurement accuracy relative to manual "
        "goniometric benchmarks and achieved an outstanding System Usability Scale (SUS) score of 84.5 / 100 (Grade A / Excellent)."
    )
    add_p(
        doc,
        "From a commercial and financial perspective, MotionIQ adopts a customer-value-based and competitive parity pricing strategy with an Early Access "
        "introductory tier priced at 49,000 VND / month (~1,600 VND/day), followed by a Standard tier at 79,000 VND / month. The initiative operates on a "
        "lean 4-month marketing budget of 10,000,000 VND and a fixed monthly operational overhead of 1,000,000 VND/month. Break-even analysis proves that "
        "reaching just 26 active Early Access subscribers (or 15 Standard subscribers) generates sufficient Monthly Recurring Revenue (MRR ~1,000,000 VND) "
        "to achieve complete operational self-sufficiency without requiring ongoing founder out-of-pocket subsidies."
    )

    # ==========================================
    # LIST OF ACRONYMS
    # ==========================================
    add_h2(doc, "LIST OF ACRONYMS")
    t_acro = doc.add_table(rows=8, cols=3)
    t_acro.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_acro.autofit = False
    set_table_borders(t_acro, color="D4C5B9", sz="4")
    
    acro_widths = [Inches(1.5), Inches(2.4), Inches(2.4)]
    acro_data = [
        ("Acronym", "Full English Term", "Vietnamese Definition / Meaning"),
        ("AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"),
        ("BMC", "Business Model Canvas", "Khung Mô hình Kinh doanh 9 Khối"),
        ("ROM", "Range of Motion", "Biên độ góc vận động của khớp cơ thể"),
        ("CAC", "Customer Acquisition Cost", "Chi phí thu hút một khách hàng mới"),
        ("MRR", "Monthly Recurring Revenue", "Doanh thu định kỳ hằng tháng"),
        ("SUS", "System Usability Scale", "Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế)"),
        ("On-Device AI", "On-Device Artificial Intelligence", "Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị (Edge AI)")
    ]

    for row_idx, row in enumerate(t_acro.rows):
        for col_idx, text in enumerate(acro_data[row_idx]):
            cell = row.cells[col_idx]
            cell.width = acro_widths[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            if row_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if row_idx % 2 == 0 else "FFFFFF")

    # ==========================================
    # LIST OF TABLES
    # ==========================================
    add_h1(doc, "LIST OF TABLES")
    list_tables = [
        ("Table 1.1", "Founding Team Competency Profile & RACI Matrix", "Page 5"),
        ("Table 2.1", "Quantitative Field Survey Findings & Statistical Breakdown (N = 50)", "Page 6"),
        ("Table 2.2", "Competitive Landscape Analysis & Strategic Differentiation Matrix", "Page 7"),
        ("Table 3.1", "9-Block Business Model Canvas (BMC) Framework", "Page 8"),
        ("Table 3.2", "4 Standardized Functional Movement Exercises & Kinematic Thresholds", "Page 9"),
        ("Table 3.3", "Empirical Prototype Testing Results across 5 Live Sessions", "Page 10"),
        ("Table 4.1", "4-Month Lean Marketing Budget Allocation (10,000,000 VND)", "Page 11"),
        ("Table 4.2", "5-Stage Customer Conversion Funnel & Target Performance KPIs", "Page 12"),
        ("Table 4.3", "Early Access Tier Subscription Revenue Forecast", "Page 13"),
        ("Table 4.4", "Operational Break-Even vs. Capital Recovery Analysis", "Page 13"),
        ("Table 5.1", "Operational Risk Identification, Impact Assessment & Mitigation Framework", "Page 14"),
        ("Table 5.2", "Multi-Stage Sustainability & Technological Evolution Roadmap", "Page 15")
    ]

    for tb_id, tb_title, tb_pg in list_tables:
        p_tb = doc.add_paragraph()
        p_tb.paragraph_format.space_before = Pt(3)
        p_tb.paragraph_format.space_after = Pt(3)
        p_tb.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_tb.add_run(f"{tb_id}: {tb_title}")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11.5)
        
        r2 = p_tb.add_run(f"\t{tb_pg}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11.5)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(100, 100, 100)

    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    doc.add_page_break()
    add_h1(doc, "TABLE OF CONTENTS")
    add_p(doc, "(Hierarchical Table of Contents with Academic Chapter Structure and Section Lead Authors)", italic=True, font_size=11, color=(100, 100, 100))

    toc_items = [
        ("ACKNOWLEDGEMENTS", "2", 1),
        ("EXECUTIVE SUMMARY", "2", 1),
        ("LIST OF ACRONYMS", "3", 1),
        ("LIST OF TABLES", "4", 1),
        ("CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (Lead: Huỳnh Thị Yến Duy)", "5", 1),
        ("1.1. Demographic Context & Origin of the MotionIQ Initiative", "5", 2),
        ("1.2. Organizational Mission, Vision, and Core Values", "5", 2),
        ("1.3. Founding Team Competency Profiles & RACI Governance Matrix", "6", 2),
        ("CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (Leads: Nguyễn Nhã Quân, Đặng Vĩnh Phúc)", "7", 1),
        ("2.1. Empirical Survey Methodology & Sample Scope (N = 50)", "7", 2),
        ("2.2. Quantitative Survey Findings from Google Sheets (N = 50)", "7", 2),
        ("2.3. Dual Target Customer Personas & Empathy Mapping", "8", 2),
        ("2.4. Competitive Landscape Analysis & Positioning Differentiation", "8", 2),
        ("CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (Leads: Nguyễn Hải Hà, Nguyễn Nhã Quân)", "9", 1),
        ("3.1. 9-Block Business Model Canvas (BMC) Framework", "9", 2),
        ("3.2. Technical Architecture & 100% On-Device AI Biomechanical Pipeline", "10", 2),
        ("3.3. 4 Standardized Functional Movement Exercises", "10", 2),
        ("3.4. Empirical Validation across 5 Live Prototype Testing Sessions", "10", 2),
        ("CHAPTER 4: COMMUNICATION STRATEGY & REVENUE GROWTH (Lead: Mã Phú Tín)", "11", 1),
        ("4.1. 4-Month Strategic Communication Objectives", "11", 2),
        ("4.2. Dual Customer Segments & Core Value Messaging", "11", 2),
        ("4.3. Marketing Channels & Community Engagement Tactics", "11", 2),
        ("4.4. 4-Month Communication Implementation Roadmap", "12", 2),
        ("4.5. Value-Based & Competitive Parity Pricing Strategy", "12", 2),
        ("4.6. Lean Budget Estimation & Operational Cost Structure", "13", 2),
        ("4.7. Revenue Growth Plan & Conversion Funnel KPIs", "13", 2),
        ("4.8. Revenue Projections, Break-Even Analysis & Strategic Financial Callout", "14", 2),
        ("CHAPTER 5: RISK MANAGEMENT, SUSTAINABILITY & FUTURE ROADMAP (Lead: Hồ Tuyết Nghi)", "15", 1),
        ("5.1. Operational Risk Identification & Mitigation Framework", "15", 2),
        ("5.2. Multi-Stage Sustainability and Strategic Growth Plan", "15", 2),
        ("5.3. Project Limitations and Future Technological Roadmap", "16", 2),
        ("CONCLUSION (Lead: Huỳnh Thị Yến Duy)", "17", 1)
    ]

    for title, pg, lvl in toc_items:
        add_toc_line(doc, title, pg, lvl)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1
    # ==========================================
    add_h1(doc, "CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (CHECKPOINT 1)")
    add_p(doc, "[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "1.1. Demographic Context & Origin of the MotionIQ Initiative")
    add_p(
        doc,
        "Vietnam is undergoing one of the fastest demographic aging processes in the world. According to the General Statistics Office (GSO), "
        "the elderly population (aged 60 and older) has surpassed 13.5 million citizens, representing more than 13.5% of the national population. "
        "Forecasts indicate that Vietnam will officially transition from an 'aging society' to an 'aged society' by 2036. Alongside natural biological aging, "
        "elderly individuals face widespread musculoskeletal degeneration, sarcopenia (age-related muscle wasting), osteoarthritis, diminished joint mobility, "
        "and balance instability, which dramatically increases the risk of accidental falls."
    )
    add_p(
        doc,
        "In modern Vietnamese society, adult children in their 20s to 40s (the 'sandwich generation') face immense workplace pressures and economic demands, "
        "leaving them with very limited time to directly supervise or assist their aging parents' daily physical exercises at home. Meanwhile, professional "
        "physical therapy or personalized wellness training centers charge between 150,000 and 300,000 VND per session—a cost that creates an unsustainable "
        "financial burden for ordinary households when sustained over months. Consequently, millions of elderly Vietnamese either abandon exercise altogether "
        "or practice unguided movements from memory, leading to improper joint postures, severe biomechanical compensations, and increased injury risk."
    )
    add_p(
        doc,
        "MotionIQ was conceived to solve this acute societal dilemma. By harnessing computer vision and artificial intelligence operating entirely within standard "
        "web browsers (100% On-Device AI), MotionIQ transforms any standard smartphone, tablet, or laptop camera into an intelligent, empathetic home exercise companion. "
        "MotionIQ provides immediate posture guidance and natural Vietnamese voice prompts without requiring wearable sensors or invasive hardware, empowering seniors "
        "to maintain regular physical activity with complete autonomy and offering peace of mind to working adult children."
    )

    add_h2(doc, "1.2. Organizational Mission, Vision, and Core Values")
    add_p(
        doc,
        "1. Mission Statement:\n"
        "To empower elderly Vietnamese citizens to maintain daily functional mobility and exercise safely, autonomously, and joyfully at home through accessible, "
        "privacy-centric AI technology, while bridging the emotional and caregiving distance between generations in busy modern families."
    )
    add_p(
        doc,
        "2. Vision Statement:\n"
        "To become the most trusted and widespread digital motion tracking and physical wellness support platform for seniors in Vietnam and Southeast Asia, "
        "setting the industry benchmark for ethical, on-device edge AI in non-medical home care."
    )
    add_p(
        doc,
        "3. Core Values (4T Framework):\n"
        "• Thấu cảm (Deep Empathy): Every product design decision originates from a profound understanding of geriatric physical limitations, psychological needs, and technological fears.\n"
        "• Tiện ích (Accessible Simplicity): Designing a minimalist, intuitive geriatric user interface (Geriatric UX) with large touch targets, zero complex menus, and natural Vietnamese voice feedback.\n"
        "• Tin cậy (Absolute Trust & Privacy): Zero camera streaming, zero cloud video retention. 100% on-device AI guarantees that personal visual data never leaves the user's living room.\n"
        "• Thực tiễn (Affordable Practicality): High-performance assistive technology priced affordably for ordinary Vietnamese households (less than 2,000 VND per day)."
    )

    add_h2(doc, "1.3. Founding Team Competency Profiles & RACI Governance Matrix")
    add_p(
        doc,
        "The MotionIQ founding team unites six passionate students from FPT University Can Tho Campus, combining diverse skill sets across software engineering, "
        "artificial intelligence, product management, multimedia design, and market development:"
    )
    add_p(
        doc,
        "1. Huỳnh Thị Yến Duy (Project Lead & CEO — Student ID: CE191522): Overall project leadership, strategic vision, resource allocation, investor relations, and external stakeholder management.\n"
        "2. Nguyễn Hải Hà (Chief Technology Officer — CTO): Full-stack systems architecture, Next.js 14 engineering, MediaPipe Pose integration, WebGL/WASM acceleration, and One-Euro Filter algorithm development.\n"
        "3. Nguyễn Nhã Quân (Chief Product Officer — CPO): Product requirements document (PRD) formulation, geriatric UX/UI design system, user testing protocols, and feedback engine logic.\n"
        "4. Đặng Vĩnh Phúc (Market Research & Language Specialist): Quantitative survey execution, bilingual localization, academic terminology compliance, and persona empathy mapping.\n"
        "5. Mã Phú Tín (Growth & Media Lead): Omni-channel communication execution, short-form video production (TikTok/Reels), community engagement, and digital conversion funnels.\n"
        "6. Hồ Tuyết Nghi (Chief Marketing Officer — CMO): Marketing positioning, risk governance frameworks, B2C subscription pricing strategies, and customer retention programs."
    )

    t_raci = doc.add_table(rows=9, cols=7)
    t_raci.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_raci.autofit = False
    set_table_borders(t_raci, color="D4C5B9", sz="4")
    raci_widths = [Inches(1.8), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(1.0)]
    
    raci_data = [
        ("Project Task / Functional Domain", "Yến Duy", "Hải Hà", "Nhã Quân", "Vĩnh Phúc", "Phú Tín", "Tuyết Nghi"),
        ("Project Ideation & Milestone Management", "A / R", "C", "C", "I", "I", "C"),
        ("Software Architecture & AI Pipeline", "I", "A / R", "C", "I", "I", "I"),
        ("Product PRD & Geriatric UX/UI Design", "C", "C", "A / R", "I", "C", "C"),
        ("Field Survey & Market Research Analysis", "C", "I", "C", "A / R", "I", "C"),
        ("Communication Plan & Content Creation", "I", "I", "I", "I", "A / R", "C"),
        ("Pricing Strategy & Financial Modeling", "A", "I", "C", "I", "C", "A / R"),
        ("Risk Governance & Legal Compliance", "A", "C", "I", "I", "I", "A / R"),
        ("Prototype Testing & User Evaluation", "C", "C", "A / R", "C", "I", "I")
    ]

    for r_idx, row in enumerate(t_raci.rows):
        for c_idx, val in enumerate(raci_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = raci_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if "A / R" in val or val == "A":
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(doc, "[Note: R = Responsible; A = Accountable; C = Consulted; I = Informed]", italic=True, font_size=10, color=(100, 100, 100))

    # ==========================================
    # CHAPTER 2
    # ==========================================
    doc.add_page_break()
    add_h1(doc, "CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Nhã Quân — CPO & Đặng Vĩnh Phúc — Market Specialist]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "2.1. Empirical Survey Methodology & Sample Scope (N = 50)")
    add_p(
        doc,
        "To establish a rigorous, evidence-based foundation for product development, the MotionIQ team conducted an extensive empirical field survey "
        "across Can Tho City (Ninh Kieu, Cai Rang, Binh Thuy districts) and neighboring Southwestern provinces during October 2026. Data was collected via "
        "a standardized Google Form questionnaire combined with direct in-person interviews with elderly residents at local community centers, senior citizen "
        "clubs, and residential neighborhoods. A total of 50 fully validated, high-quality responses were recorded (N = 50), comprising 32 adult children "
        "(aged 22–45) caring for aging parents and 18 elderly individuals (aged 60–78)."
    )

    add_h2(doc, "2.2. Quantitative Survey Findings from Google Sheets (N = 50)")
    add_p(
        doc,
        "Statistical synthesis of the 50 survey responses yielded crucial quantitative insights into consumer pain points, technology readiness, and economic willingness:"
    )

    t_surv = doc.add_table(rows=9, cols=3)
    t_surv.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_surv.autofit = False
    set_table_borders(t_surv, color="D4C5B9", sz="4")
    surv_widths = [Inches(3.3), Inches(1.2), Inches(1.8)]
    
    surv_data = [
        ("Survey Indicator / Survey Question", "Percentage", "Quantitative Count"),
        ("Difficulty supervising parents' home exercises due to busy work schedules", "68.0%", "34 / 50 respondents"),
        ("Seniors experiencing fear of improper posture, joint strain, or falling", "74.0%", "37 / 50 respondents"),
        ("Willingness to trial an AI camera-based exercise support web application", "82.4%", "41 / 50 respondents"),
        ("Preference for simple web/app interface requiring zero hardware purchase", "88.0%", "44 / 50 respondents"),
        ("Strong demand for real-time Vietnamese voice encouragement & counting", "92.0%", "46 / 50 respondents"),
        ("Willingness to pay: 30,000 – 50,000 VND / month (Introductory Price Range)", "50.0%", "25 / 50 respondents"),
        ("Willingness to pay: 50,000 – 100,000 VND / month (Standard Price Range)", "28.0%", "14 / 50 respondents"),
        ("Willingness to pay: Greater than 100,000 VND / month (Premium Range)", "6.0%", "3 / 50 respondents")
    ]

    for r_idx, row in enumerate(t_surv.rows):
        for c_idx, val in enumerate(surv_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = surv_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 1 and ("68.0%" in val or "74.0%" in val or "82.4%" in val or "92.0%" in val):
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(
        doc,
        "Key Research Takeaways:\n"
        "1. The Core Societal Pain Point is Proven: Nearly 7 out of 10 working adult children feel guilty and anxious about being unable to supervise their parents' "
        "daily physical movement. Concurrently, 74% of seniors experience hesitation and fear of injury when exercising unassisted.\n"
        "2. Overwhelming Trial Intent: 82.4% readiness to trial confirms strong product-market resonance for an accessible home motion tracking solution.\n"
        "3. Optimal Commercial Sweet Spot: Exactly 78.0% of respondents endorsed subscription pricing within the 30,000 to 100,000 VND/month band, "
        "directly validating our Early Access pricing at 49,000 VND/month and Standard tier at 79,000 VND/month."
    )

    add_h2(doc, "2.3. Dual Target Customer Personas & Empathy Mapping")
    add_p(
        doc,
        "Because MotionIQ operates in a multi-generational household context where the economic purchaser and the end-user are distinct family members, "
        "we construct two interconnected customer personas and empathy maps:"
    )
    add_p(
        doc,
        "1. Economic Buyer Persona — 'Trần Minh Triết' (Age: 32):\n"
        "• Demographics: Senior IT Project Manager, living in Ninh Kieu, Can Tho. Monthly income: 25,000,000 VND. Married, caring for 67-year-old mother living separately.\n"
        "• Psychographics & Pains: Works 10 hours daily. Constantly worries that his mother will slip, trip, or strain her knee joints while exercising alone at home. "
        "Feels guilty about his busy schedule. Cannot afford 200,000 VND/session for home physical therapy.\n"
        "• Desired Gains: An automated, non-invasive platform that guides his mother to exercise accurately and sends transparent weekly activity summaries to his phone."
    )
    add_p(
        doc,
        "2. End-User Persona — 'Bà Tư' (Nguyễn Thị Mai, Age: 67):\n"
        "• Demographics: Retired primary school teacher, residing in Binh Thuy, Can Tho. Suffers from mild bilateral knee osteoarthritis and mild balance degradation.\n"
        "• Psychographics & Pains: Anxious about becoming a physical or financial burden to her children. Enjoys gentle morning movement but forgets proper posture cues. "
        "Intimidated by complex modern apps, tiny text, and English tech jargon. Afraid of camera hacking or privacy violations.\n"
        "• Desired Gains: An inviting, easy-to-read app with large buttons, warm Vietnamese spoken words ('Bác làm rất tốt!'), and zero hardware setup hassles."
    )

    add_h2(doc, "2.4. Competitive Landscape Analysis & Positioning Differentiation")
    add_p(
        doc,
        "MotionIQ navigates a competitive market comprising four distinct alternatives, none of which comprehensively address the home exercise needs of elderly Vietnamese:"
    )

    t_comp = doc.add_table(rows=7, cols=5)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp.autofit = False
    set_table_borders(t_comp, color="D4C5B9", sz="4")
    comp_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2)]
    
    comp_data = [
        ("Evaluation Dimension", "MotionIQ (Our Platform)", "Freeletics / Nike App", "Kaia Health / Sword", "Physical Therapy Centers"),
        ("Primary Target Demographic", "Elderly (Aged 60+) & Families", "Young Fitness Enthusiasts", "Post-op Clinical Patients", "General Medical Patients"),
        ("Hardware / Sensor Requirements", "Zero (Standard WebCam)", "Zero (Smartphone)", "Wearable Sensors Required", "In-Clinic Machinery"),
        ("AI Processing Location", "100% On-Device (Zero Cloud)", "Server-side / Cloud", "Proprietary Cloud Portal", "N/A (Manual Inspection)"),
        ("Audio Feedback Language", "Natural Vietnamese Voice", "English / Pre-recorded", "English / US Clinicians", "In-person Vietnamese"),
        ("User Privacy Architecture", "Absolute (Frames deleted on RAM)", "Cloud Video Streaming", "Medical Cloud HIPAA", "In-person Observation"),
        ("Price Point / Affordability", "49,000 – 79,000 VND / month", "250,000 – 350,000 VND / mo", "$100+ USD / month", "150k – 300k VND / session")
    ]

    for r_idx, row in enumerate(t_comp.rows):
        for c_idx, val in enumerate(comp_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = comp_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 1:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(
        doc,
        "MotionIQ's Strategic 'Blue Ocean' Positioning:\n"
        "MotionIQ establishes an uncontested market space at the intersection of geriatric-specific movement support, absolute edge AI privacy, and hyper-affordable "
        "local pricing. While Western fitness applications target young athletes with high-intensity regimens and medical therapy platforms require prohibitive "
        "hardware setups, MotionIQ democratizes physical wellness for ordinary Vietnamese households through a zero-install, privacy-first web platform."
    )

    # ==========================================
    # CHAPTER 3
    # ==========================================
    doc.add_page_break()
    add_h1(doc, "CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Hải Hà — CTO & Nguyễn Nhã Quân — CPO]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "3.1. 9-Block Business Model Canvas (BMC) Framework")
    add_p(
        doc,
        "MotionIQ structures its business architecture using the 9-block Business Model Canvas, aligning technological capabilities with sustainable value creation:"
    )

    t_bmc = doc.add_table(rows=10, cols=2)
    t_bmc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bmc.autofit = False
    set_table_borders(t_bmc, color="D4C5B9", sz="4")
    bmc_widths = [Inches(2.2), Inches(4.1)]
    
    bmc_data = [
        ("BMC Block", "Strategic Content & Operational Implementation"),
        ("1. Customer Segments (CS)", "• Dual Customer Segments:\n- Economic Buyer: Adult children (aged 22–45) caring for aging parents.\n- Primary End-User: Elderly citizens (aged 60+) needing daily home functional exercise."),
        ("2. Value Propositions (VP)", "• For Seniors: Safe, autonomous exercise tracking with natural Vietnamese voice feedback; zero hardware required; non-intrusive 100% on-device AI privacy.\n• For Children: Peace of mind regarding parental safety; transparent weekly progress sync."),
        ("3. Channels (CH)", "• TikTok & Facebook Reels short-form storytelling; Facebook elderly care communities; Senior Citizen Clubs & Pagoda activations in Can Tho; Direct Web App (motion-iq-five.vercel.app)."),
        ("4. Customer Relationships (CR)", "• Warm, encouraging virtual assistant mascot 'Bé Nấm'; automated daily exercise reminders; responsive Zalo customer support; community wellness challenges."),
        ("5. Revenue Streams (RS)", "• B2C Subscriptions: Early Access (49,000 VND/month), Standard (79,000 VND/month), Annual Pass (790,000 VND/year).\n• Future B2B Licensing: Senior community centers and private nursing residences."),
        ("6. Key Resources (KR)", "• Proprietary On-Device AI computer vision algorithms; UI-PRMD / KIMORE benchmark dataset mapping; Next.js 14 web codebase; Multi-disciplinary founding team."),
        ("7. Key Activities (KA)", "• Web platform development & UX refinement; On-device model optimization; Short-form video production; Direct community workshops and field testing."),
        ("8. Key Partnerships (KP)", "• Local elderly associations and senior physical culture clubs in Can Tho; FPT University entrepreneurial mentorship; Cloud infrastructure providers (Vercel, Supabase)."),
        ("9. Cost Structure (CS)", "• Fixed OPEX: Web hosting & cloud telemetry (1,000,000 VND/month).\n• 4-Month Marketing Launch Budget: 10,000,000 VND (digital media ads, printing, offline activations).")
    ]

    for r_idx, row in enumerate(t_bmc.rows):
        for c_idx, val in enumerate(bmc_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = bmc_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(140, 47, 30)

    add_h2(doc, "3.2. Technical Architecture & 100% On-Device AI Biomechanical Pipeline")
    add_p(
        doc,
        "MotionIQ is built on modern web technologies including Next.js 14 (App Router), TypeScript, and Tailwind CSS. The computer vision pipeline "
        "operates entirely within client-side WebAssembly (WASM) and WebGL contexts via Google MediaPipe Pose, ensuring 100% On-Device execution without "
        "streaming video frames to any remote server."
    )
    add_p(
        doc,
        "1. Mathematical Formulation of Joint Kinematics:\n"
        "To calculate anatomical joint angles (e.g., knee flexion, hip angle, shoulder abduction), MotionIQ computes the 3D forward kinematic vector angle between "
        "three sequential skeletal landmarks A, B (the joint vertex), and C using vector dot products and Euclidean norms:\n\n"
        "Let u = A - B and v = C - B. The interior joint angle θ is derived as:\n"
        "θ = arccos [ (u • v) / (||u|| * ||v||) ]\n\n"
        "Where u • v = (ux * vx) + (uy * vy) + (uz * vz) and ||u|| = sqrt(ux^2 + uy^2 + uz^2)."
    )
    add_p(
        doc,
        "2. Anthropometric Scale Normalization:\n"
        "Because user distance from the camera and physical height vary across households, coordinates are normalized relative to the torso length:\n"
        "L_torso = || x_hip_midpoint - x_shoulder_midpoint ||\n"
        "d_norm = d / L_torso\n"
        "This invariant normalization ensures identical posture scoring regardless of whether the user stands 2 meters or 3 meters away from the smartphone."
    )
    add_p(
        doc,
        "3. Feature Vector Extraction & Classification:\n"
        "For each incoming video frame at 30 FPS, MotionIQ constructs a 132-dimensional feature vector (33 pose landmarks * [x, y, z, visibility]). "
        "This vector is evaluated against an L2-Ridge Regularized Logistic Regression classifier trained on open standardized movement datasets (UI-PRMD, KIMORE):\n"
        "min_w  sum_i log(1 + exp(-y_i * w^T x_i)) + λ ||w||_2^2"
    )
    add_p(
        doc,
        "4. Dynamic Jitter Smoothing via One-Euro Filter:\n"
        "To prevent frame-to-frame landmark jitter caused by camera noise or ambient lighting changes, MotionIQ implements the adaptive One-Euro Filter. "
        "The filter automatically adjusts its cutoff frequency fc based on the instantaneous velocity of skeletal movement:\n"
        "f_c = f_c_min + β * |dx/dt|\n"
        "During high-speed transitions, the cutoff frequency increases to eliminate latency; during stationary holding phases, it decreases to eliminate high-frequency jitter."
    )
    add_p(
        doc,
        "5. Architectural Privacy Safeguards:\n"
        "MotionIQ decodes raw WebCam frames directly into temporary WebGL GPU texture buffers. Once landmark coordinates are extracted by MediaPipe in browser RAM, "
        "the raw pixel buffers are immediately discarded by browser garbage collection. No visual images or video recordings are ever written to disk or transmitted over the network."
    )

    add_h2(doc, "3.3. 4 Standardized Functional Movement Exercises")
    add_p(
        doc,
        "To ensure safety and physiological efficacy for seniors, MotionIQ incorporates four standardized functional movement exercises adapted from "
        "established geriatric physical fitness assessments (such as the 30-Second Chair Stand Test and Senior Fitness Test):"
    )

    t_ex = doc.add_table(rows=5, cols=4)
    t_ex.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ex.autofit = False
    set_table_borders(t_ex, color="D4C5B9", sz="4")
    ex_widths = [Inches(1.5), Inches(1.8), Inches(1.5), Inches(1.5)]
    
    ex_data = [
        ("Exercise Name", "Primary Functional Objective", "Key Kinematic Angles", "Recommended Camera Angle"),
        ("1. Đứng lên – Ngồi xuống (Sit-to-Stand)", "Lower limb power, quadriceps strength & independent mobility", "Knee angle: Standing ≥ 150°, Fully seated ≤ 105°", "Diagonal 45°–90° side view, waist height, 2–3m"),
        ("2. Đứng thẳng nâng tay (Shoulder Abduction)", "Shoulder joint range of motion, upper body posture & breathing", "Arm-torso angle: Neutral ~20°, Abduction ≥ 85°", "Direct frontal view (0°), chest height, 2–3m"),
        ("3. Đứng dang chân (Side Leg Raise)", "Hip abductor strength, lateral pelvic balance & fall prevention", "Hip abduction angle: Standing ~15°, Extended ≥ 35°", "Direct frontal view (0°), waist height, 2–3m"),
        ("4. Đứng tấn cơ bản (Assisted Squat)", "Core stability, gluteal activation & knee joint stabilization", "Knee angle: Standing ~165°, Squat depth ≤ 115°", "Diagonal 45° side view, waist height, 2–3m")
    ]

    for r_idx, row in enumerate(t_ex.rows):
        for c_idx, val in enumerate(ex_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = ex_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 0:
                    run.font.bold = True

    add_h2(doc, "3.4. Empirical Validation across 5 Live Prototype Testing Sessions")
    add_p(
        doc,
        "The MotionIQ team deployed the live MVP prototype (accessible at https://motion-iq-five.vercel.app) across five comprehensive physical testing sessions "
        "in Can Tho City, involving 10 elderly participants (aged 60–75) and 5 local physical fitness trainers who evaluated biomechanical accuracy and usability:"
    )

    t_eval = doc.add_table(rows=6, cols=5)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_eval.autofit = False
    set_table_borders(t_eval, color="D4C5B9", sz="4")
    eval_widths = [Inches(1.2), Inches(1.4), Inches(1.3), Inches(1.2), Inches(1.2)]
    
    eval_data = [
        ("Session #", "Target Exercises Tested", "ROM Measurement Accuracy", "Rep Counting Accuracy", "Mean SUS Usability Score"),
        ("Session 1", "Sit-to-Stand (Chair)", "92.4% (vs Goniometer)", "96.0% (48/50 reps)", "80.0 / 100 (Grade B)"),
        ("Session 2", "Shoulder Abduction", "95.1% (vs Goniometer)", "98.0% (49/50 reps)", "82.5 / 100 (Grade A-)"),
        ("Session 3", "Side Leg Raise", "93.8% (vs Goniometer)", "94.0% (47/50 reps)", "85.0 / 100 (Grade A)"),
        ("Session 4", "Assisted Squat", "95.5% (vs Goniometer)", "96.0% (48/50 reps)", "86.0 / 100 (Grade A)"),
        ("Session 5 (Consolidated)", "All 4 Exercises", "96.2% (vs Goniometer)", "98.0% (49/50 reps)", "89.0 / 100 (Grade A+)")
    ]

    for r_idx, row in enumerate(t_eval.rows):
        for c_idx, val in enumerate(eval_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = eval_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if r_idx == 5:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(
        doc,
        "Summary of Prototype Testing Milestones:\n"
        "• Overall ROM Accuracy: Achieved a mean of 94.6% relative to manual goniometric reference measurements.\n"
        "• Repetition Counting Reliability: Successfully counted 96.4% of total repetitions across all test sessions.\n"
        "• System Usability Scale (SUS): Reached an exceptional average score of 84.5 / 100, firmly positioning MotionIQ in the 'Grade A / Excellent' "
        "tier of international software usability standards."
    )

    # ==========================================
    # CHAPTER 4
    # ==========================================
    doc.add_page_break()
    add_h1(doc, "CHAPTER 4: COMMUNICATION STRATEGY, FINANCIAL PLANNING & REVENUE GROWTH")
    add_p(doc, "[Lead Author & Editor: Mã Phú Tín — Growth & Media Lead]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "4.1. 4-Month Strategic Communication Objectives")
    add_p(
        doc,
        "MotionIQ executes a tightly disciplined, four-month omnichannel communication campaign designed to achieve four core measurable milestones:\n"
        "1. Brand Awareness: Generate 15,000+ total views and impressions across Can Tho City and the Southwestern region via short-form video and social media.\n"
        "2. Platform Engagement: Drive 1,500+ web visits to the live interactive MVP web application (https://motion-iq-five.vercel.app).\n"
        "3. Trial Onboarding: Acquire 40 to 50 active family trial accounts with direct parent-child participation.\n"
        "4. Paid Customer Conversion: Convert 15 to 20 paying subscribers by Month 4 under the Early Access tier (49,000 VND/month), generating verifiable initial MRR."
    )

    add_h2(doc, "4.2. Dual Customer Segments & Core Value Messaging")
    add_p(
        doc,
        "To resonate with both sides of the multi-generational household, MotionIQ crafts targeted dual-track communication messages:\n"
        "• For Adult Children (The Economic Buyer): 'Gửi trọn hiếu tâm, đồng hành cùng sức khỏe cha mẹ mỗi ngày' (A Gift of Filial Love: Empowering Your Parents' Daily Vitality). "
        "Emphasizes peace of mind, automated posture safety, and loving care without intruding on busy working hours.\n"
        "• For Elderly Users (The Primary End-User): 'Tập vui, tập đúng, sống khỏe mỗi ngày cùng Bé Nấm' (Exercise Joyfully, Move Correctly, Live Vibrantly with Bé Nấm). "
        "Emphasizes warm Vietnamese companionship, large readable text, zero tech anxiety, and absolute visual privacy."
    )

    add_h2(doc, "4.3. Marketing Channels & Community Engagement Tactics")
    add_p(
        doc,
        "MotionIQ concentrates marketing resources across four cost-effective channels suited for student budgets:\n"
        "1. Short-Form Video Marketing (TikTok, Facebook Reels, YouTube Shorts): Emotional storytelling dramatizing the 'sandwich generation' dilemma, "
        "side-by-side exercise demos with 'Bé Nấm', and real footage of elderly users practicing at home.\n"
        "2. Facebook Community Groups: Active engagement in Can Tho family groups, retirement forums, and geriatric health care communities, sharing helpful "
        "functional fitness tips and inviting beta testers.\n"
        "3. Direct Community Activations (Senior Citizen Clubs & Pagodas): Organizing live weekend trial booths at cultural centers and pagodas in Can Tho, "
        "offering hands-on guidance for seniors to try camera tracking on laptops or tablets.\n"
        "4. Word-of-Mouth & Family Referral Engine: Providing a 'Share with a Friend' referral program where each existing family receives 1 bonus month of free access "
        "when referring another family."
    )

    add_h2(doc, "4.4. 4-Month Communication Implementation Roadmap")
    add_p(
        doc,
        "• Month 1 (Awareness & Emotional Hook): Launch short-form video series addressing the emotional challenge of caring for aging parents from afar. "
        "Deploy organic Reels and TikTok content targeting adult children in Southwestern Vietnam.\n"
        "• Month 2 (Interactive Demos & Community Workshops): Introduce the live MVP web application. Host two direct demonstration workshops at senior clubs in Ninh Kieu. "
        "Distribute informative printed brochures with QR codes.\n"
        "• Month 3 (Early Access Launch & Social Proof): Roll out the Early Access subscription tier (49,000 VND/month). Share authentic video testimonials from initial trial families. "
        "Implement referral incentives.\n"
        "• Month 4 (Conversion Optimization & Retention Analysis): Consolidate user feedback, track renewal rates among paying subscribers, and optimize ad spend on top-performing channels."
    )

    add_h2(doc, "4.5. Value-Based & Competitive Parity Pricing Strategy")
    add_p(
        doc,
        "MotionIQ employs a value-based pricing model benchmarked against competing market alternatives:\n"
        "• Market Comparison: Traditional physical therapy centers charge 150,000 – 300,000 VND per single session (totaling 1.8M – 3.6M VND/month for 12 sessions). "
        "Western fitness apps charge 250,000 – 350,000 VND/month for generic English workouts without posture feedback.\n"
        "• MotionIQ Tiered Pricing Architecture:\n"
        "  1. Free Tier (Trải nghiệm): 1 standardized exercise (Sit-to-Stand), 5 exercise sessions per week, full Vietnamese voice guidance. Zero commitment.\n"
        "  2. Early Access Tier (Tiên phong): 49,000 VNĐ / month (~1,600 VNĐ/day). Unlocks all 4 standardized exercises, unlimited daily workouts, personalized repetition goals, and progress tracking.\n"
        "  3. Standard Tier (Tiêu chuẩn): 79,000 VNĐ / month (~2,600 VNĐ/day). Unlocks all exercises, weekly Zalo progress summaries sent to adult children, and multi-profile family support.\n"
        "  4. Annual Loyalty Pass (Đồng hành Trọn năm): 790,000 VNĐ / year (saves 17% compared to monthly standard rate, equivalent to ~2,100 VNĐ/day)."
    )

    add_h2(doc, "4.6. Lean Budget Estimation & Operational Cost Structure")
    add_p(
        doc,
        "With a realistic student entrepreneurial capital of 10,000,000 VND, the founding team allocates marketing expenditures with strict discipline:"
    )

    t_bud = doc.add_table(rows=6, cols=3)
    t_bud.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bud.autofit = False
    set_table_borders(t_bud, color="D4C5B9", sz="4")
    bud_widths = [Inches(3.3), Inches(1.5), Inches(1.5)]
    
    bud_data = [
        ("Marketing Expenditure Category", "Allocated Budget (VND)", "Percentage (%)"),
        ("Short-Form Video Production & Digital Ads (TikTok / Reels)", "3,500,000 VND", "35.0%"),
        ("Community Outreach & Digital Community Engagement", "2,500,000 VND", "25.0%"),
        ("Direct Community Activations & Senior Clubs Workshops", "2,000,000 VND", "20.0%"),
        ("Printed Materials (Brochures / Standees / Trial Incentives)", "2,000,000 VND", "20.0%"),
        ("TOTAL 4-MONTH MARKETING BUDGET", "10,000,000 VND", "100.0%")
    ]

    for r_idx, row in enumerate(t_bud.rows):
        for c_idx, val in enumerate(bud_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = bud_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            elif r_idx == 5:
                run.font.bold = True
                set_cell_background(cell, "F2EAE1")
                run.font.color.rgb = RGBColor(178, 66, 45)
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    add_p(
        doc,
        "Monthly Operational Overhead (Fixed OPEX):\n"
        "Because MotionIQ operates 100% On-Device AI in the client's browser, server video streaming costs are eliminated. Fixed operating costs consist solely of "
        "Vercel Pro web application hosting, custom domain maintenance, and minimal cloud database telemetry sync, totaling approximately 1,000,000 VND / month."
    )

    add_h2(doc, "4.7. Revenue Growth Plan & Conversion Funnel KPIs")
    add_p(
        doc,
        "MotionIQ models its customer conversion through a structured 5-stage funnel over the initial four-month operational campaign:"
    )

    t_fun = doc.add_table(rows=6, cols=3)
    t_fun.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fun.autofit = False
    set_table_borders(t_fun, color="D4C5B9", sz="4")
    fun_widths = [Inches(3.3), Inches(1.5), Inches(1.5)]
    
    fun_data = [
        ("Conversion Funnel Stage", "Target Target Metric", "Stage Conversion Rate"),
        ("Stage 1: Awareness (Total Video Views & Ad Impressions)", "15,000 views / reaches", "Baseline Reach"),
        ("Stage 2: Consideration (Visits to Demo Web Application)", "1,500 visitors", "10.0% Click-Through Rate"),
        ("Stage 3: Trial Onboarding (Active Free Trial Registrations)", "60 family accounts", "4.0% Conversion from Visitors"),
        ("Stage 4: Paid Conversion (Early Access Subscribers @ 49k)", "18 paying subscribers", "30.0% Conversion from Trial"),
        ("Stage 5: Retention (Month-over-Month Renewal Rate)", "14 – 15 retained users", "80.0% Retention Rate")
    ]

    for r_idx, row in enumerate(t_fun.rows):
        for c_idx, val in enumerate(fun_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = fun_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 1 and "18 paying" in val:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(
        doc,
        "Customer Acquisition Cost (CAC) Analysis:\n"
        "At the conclusion of Month 4, with a cumulative marketing outlay of 10,000,000 VND and 15 to 20 converted paying subscribers, "
        "the nominal initial CAC is calculated as:\n"
        "CAC = 10,000,000 VND / (15 to 20 subscribers) = 500,000 – 666,667 VND per initial subscriber."
    )

    add_h2(doc, "4.8. Revenue Projections, Break-Even Analysis & Strategic Financial Callout")
    add_p(
        doc,
        "Initial Monthly Recurring Revenue (MRR) projections under the Early Access tier (49,000 VND/month):"
    )

    t_rev = doc.add_table(rows=4, cols=2)
    t_rev.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_rev.autofit = False
    set_table_borders(t_rev, color="D4C5B9", sz="4")
    rev_widths = [Inches(3.1), Inches(3.2)]
    
    rev_data = [
        ("Number of Active Paying Subscribers", "Projected Monthly Revenue (Gói 49,000 VND)"),
        ("10 paying subscribers", "490,000 VND / month"),
        ("15 paying subscribers", "735,000 VND / month"),
        ("20 paying subscribers", "980,000 VND / month")
    ]

    for r_idx, row in enumerate(t_rev.rows):
        for c_idx, val in enumerate(rev_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = rev_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    add_p(
        doc,
        "With a target of 15–20 paying subscribers by Month 4, MotionIQ generates 735,000 – 980,000 VND in Monthly Recurring Revenue (MRR). "
        "This level closely approaches full self-sufficiency for monthly fixed operating overhead (1,000,000 VND/month).\n\n"
        "Rigorous Break-Even Analysis (Phân tích Điểm hòa vốn):\n"
        "Break-even volume is determined by standard financial formulation:\n"
        "Q_BE = Fixed Costs / (Price - Variable Cost per Subscriber)\n\n"
        "Assuming Fixed Operating Overhead (FC) = 1,000,000 VND/month and Variable Cloud Sync Cost (VC) = 10,000 VND/subscriber/month:"
    )

    t_be = doc.add_table(rows=4, cols=3)
    t_be.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_be.autofit = False
    set_table_borders(t_be, color="D4C5B9", sz="4")
    be_widths = [Inches(3.3), Inches(1.5), Inches(1.5)]
    
    be_data = [
        ("Financial Break-Even Metric", "Early Access Tier (49,000 VND)", "Standard Tier (79,000 VND)"),
        ("Contribution Margin per Subscriber (P - VC)", "39,000 VND", "69,000 VND"),
        ("Subscribers for Monthly Operational Break-Even (FC = 1.0M/mo)", "26 subscribers", "15 subscribers"),
        ("Subscribers for Full Capital Recovery (Amortizing 10M Marketing over 4 mo)", "90 subscribers / month", "51 subscribers / month")
    ]

    for r_idx, row in enumerate(t_be.rows):
        for c_idx, val in enumerate(be_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = be_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if r_idx == 2:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(178, 66, 45)

    add_p(
        doc,
        "Financial Interpretation & Analytical Clarity:\n"
        "The financial modeling confirms that while 15–20 paying subscribers in Month 4 will not yet fully recoup the initial 10,000,000 VND marketing expenditure, "
        "this dynamic aligns perfectly with standard early-stage tech startup economics: the 10M capital serves as foundational market-entry equity to build "
        "brand awareness, validate conversion funnels, and prove user retention.\n\n"
        "Crucially, from an operational continuity perspective, achieving exactly 26 Early Access subscribers (or only 15 Standard subscribers) brings the project "
        "to complete Operational Self-Sufficiency. At this threshold, monthly subscription cash flow completely covers all server hosting and maintenance overhead, "
        "ensuring the platform survives indefinitely without requiring further capital infusions."
    )

    add_callout_box(
        doc,
        "• Strategic Dynamics of CAC vs. LTV: The initial nominal CAC (500,000 – 666,667 VND) represents capital spent to reach over 15,000 targeted people and establish early brand presence. Under our SaaS recurring subscription model, an elderly user who retains for 12 to 16 months yields a Customer Lifetime Value (LTV) of 588,000 to 790,000 VND (or 948,000 VND under Standard pricing), guaranteeing LTV > CAC and proving healthy long-term unit economics.\n"
        "• Strategic Value of Operational Break-Even: Reaching 26 active subscribers (or 15 Standard subscribers) is the vital tipping point. Beyond Month 4, monthly recurring cash flow of ~1,000,000 VND/month eliminates operational burn rate, securing financial self-reliance and establishing a robust platform for scalable regional expansion.",
        title="STRATEGIC FINANCIAL TAKEAWAY & OPERATIONAL SELF-SUFFICIENCY"
    )

    # ==========================================
    # CHAPTER 5
    # ==========================================
    doc.add_page_break()
    add_h1(doc, "CHAPTER 5: RISK MANAGEMENT, SUSTAINABILITY & FUTURE ROADMAP")
    add_p(doc, "[Lead Author & Editor: Hồ Tuyết Nghi — Chief Marketing Officer]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "5.1. Operational Risk Identification & Mitigation Framework")
    add_p(
        doc,
        "To ensure safe, ethical, and legally compliant operations, MotionIQ identifies seven primary operational risks and implements proactive mitigation strategies:"
    )

    t_risk = doc.add_table(rows=8, cols=2)
    t_risk.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_risk.autofit = False
    set_table_borders(t_risk, color="D4C5B9", sz="4")
    risk_widths = [Inches(2.3), Inches(4.0)]
    
    risk_data = [
        ("Identified Operational Risk", "Concrete Actionable Mitigation Strategy"),
        ("1. Elderly tech apprehension & UX barriers", "Minimalist Geriatric UX: high-contrast color palette, extra-large typography, zero complex menus, warm natural Vietnamese voice prompts with adjustable volume and repetition."),
        ("2. AI pose tracking ambiguity under varied lighting", "One-Euro Filter jitter smoothing, dynamic confidence thresholds, and explicit graphical camera placement guides (45°–90° diagonal, 2–3m distance)."),
        ("3. Consumer reluctance to pay monthly subscriptions", "Provide a permanent free tier with 1 core exercise, transparently communicate value additions for paid tiers, and validate the introductory 49,000 VND rate."),
        ("4. Inflation of Customer Acquisition Cost (CAC)", "Rigorously monitor acquisition channel ROAS, concentrate on high-conversion local community networks, and leverage organic short-form viral storytelling."),
        ("5. User drop-off & subscription churn after 1 month", "Incorporate daily exercise streak gamification with 'Bé Nấm', deliver bi-weekly progress milestone badges, and send automated summary alerts to children."),
        ("6. Regulatory classification & non-medical compliance", "Prominently display transparent non-medical disclaimers: MotionIQ is an assistive physical wellness support tool for home exercise, NOT a clinical diagnostic device, and never replaces physicians."),
        ("7. Personal visual data security & privacy concerns", "100% On-Device AI architecture processes video frames strictly in temporary volatile browser RAM; frames are immediately purged with zero cloud storage.")
    ]

    for r_idx, row in enumerate(t_risk.rows):
        for c_idx, val in enumerate(risk_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = risk_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
                if c_idx == 0:
                    run.font.bold = True

    add_h2(doc, "5.2. Multi-Stage Sustainability and Strategic Growth Plan")
    add_p(
        doc,
        "MotionIQ charts a structured, three-phase strategic growth roadmap to ensure sustained market development and technological excellence:\n\n"
        "1. Phase 1: Market Validation & Initial Traction (Months 1–4):\n"
        "• Finalize the production MVP web application and refine geriatric ergonomics.\n"
        "• Onboard 40–50 family beta trial accounts across Can Tho City.\n"
        "• Validate willingess-to-pay with the Early Access tier (49,000 VND/month).\n"
        "• Achieve 15–20 paying subscribers to prove commercial viability.\n\n"
        "2. Phase 2: Stabilization, Optimization & Feature Expansion (Months 5–6):\n"
        "• Enhance pose landmark robustness under dim lighting and varied room angles.\n"
        "• Evaluate customer retention rates and introduce the Standard tier (79,000 VND/month).\n"
        "• Deploy automated weekly exercise summaries delivered to adult children via Zalo.\n"
        "• Progress from operational break-even (26 subscribers) toward full capital recovery.\n\n"
        "3. Phase 3: Regional Scaling & Ecosystem Integration (Months 7–12+):\n"
        "• Expand the exercise library to include gentle mobility routines for wrists, ankles, and neck.\n"
        "• Deploy a Zalo Mini App, allowing users to launch MotionIQ instantly without browser logins.\n"
        "• Explore B2B partnerships with senior residential communities and retirement villages."
    )

    add_h2(doc, "5.3. Project Limitations and Future Technological Roadmap")
    add_p(
        doc,
        "In keeping with academic rigor and intellectual integrity, the founding team recognizes current project limitations and defines clear future technological enhancements:\n\n"
        "1. Current Project Limitations:\n"
        "• Ambient Lighting and Apparel Sensitivity: Monocular computer vision relies on visual contrast. In severely under-lit rooms or when users wear exceptionally loose, "
        "baggy traditional garments (e.g., traditional áo bà ba), MediaPipe landmark detection confidence may temporarily fluctuate.\n"
        "• 2D Monocular Camera Depth Perception: Operating on standard smartphone webcams restricts tracking to monocular 2D/pseudo-3D coordinates. While forward kinematics "
        "accurately calculate planar joint angles, subtle rotational plane deviations (e.g., hip internal rotation during squats) require careful camera angle alignment (45°–90°).\n"
        "• Geographic Scope of Initial Field Survey: Empirical survey data (N = 50) and prototype tests were centered in Can Tho City and the Mekong Delta. "
        "Expanding to Tier-1 metropolitan areas (Ho Chi Minh City, Hanoi) will capture diverse housing configurations and tech literacy levels.\n\n"
        "2. Future Technological Roadmap:\n"
        "• Zalo Mini App Deployment: Migrating the client application into the ubiquitous Zalo ecosystem will allow elderly users to launch daily exercises with a single tap, "
        "leveraging Zalo's built-in authentication and zero-install footprint.\n"
        "• Smart TV & Living Room Adaptation: Developing a WebOS / Android TV living-room app utilizing large television screens and wide-angle USB webcams, allowing seniors "
        "to exercise with crystal-clear visibility from their couch.\n"
        "• Multi-Generational Family Companion Dashboard: Implementing an automated notification system that alerts adult children via SMS/Zalo if their elderly parent "
        "misses scheduled exercises for 3 consecutive days or triggers an in-session fall/inactivity watchdog alert.\n"
        "• Multi-Modal Wearable Sensor Fusion: Exploring low-power Bluetooth Low Energy (BLE) integration with smartwatches (Apple Watch, Galaxy Watch) to fuse heart rate "
        "and inertial measurement unit (IMU) telemetry with on-device computer vision."
    )

    # ==========================================
    # CONCLUSION
    # ==========================================
    add_h1(doc, "CONCLUSION")
    add_p(doc, "[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]", italic=True, font_size=11, color=(140, 47, 30))
    add_p(
        doc,
        "The MotionIQ project addresses one of the most pressing socio-demographic challenges facing contemporary Vietnam: empowering an aging population "
        "to maintain physical vitality and exercise safely at home, while relieving the constant worry experienced by busy working adult children.\n\n"
        "Through an honest, methodical, and evidence-based approach—grounded in empirical field survey data from 50 local families, rigorous biomechanical "
        "prototype testing across 5 live sessions, and a disciplined 4-month communication strategy with a lean 10,000,000 VND budget—MotionIQ proves that "
        "cutting-edge artificial intelligence can be deployed ethically, securely, and affordably. By guaranteeing 100% on-device visual privacy, adopting intuitive "
        "geriatric UX, and establishing clear operational self-sufficiency at just 26 subscribers, MotionIQ demonstrates viable startup potential, "
        "sustainable business unit economics, and profound humanistic value."
    )

    # Save DOCX
    doc.save(out_path)
    print(f"Successfully compiled English DOCX report at: {out_path}")

def build_markdown(out_path):
    md_content = r"""# MINISTRY OF EDUCATION AND TRAINING
## FPT UNIVERSITY CAN THO CAMPUS
***
### FINAL ENTREPRENEURSHIP PROJECT REPORT
### COURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP

# MOTIONIQ — ON-DEVICE AI MOTION TRACKING PLATFORM FOR ELDERLY HOME CARE (100% ON-DEVICE AI)

> *"MotionIQ – Exercise at home, motion tracking made simpler."*  
> *(Consolidated Final Academic Report: Checkpoint 1 • Checkpoint 2 • Checkpoint 3 • Marketing & Financial Revenue Strategy)*

---

| Project Information | Details |
| :--- | :--- |
| **Academic Advisor** | Mr. Tran Ngoc Son |
| **Student Team** | MOTIONIQ — Cohort K19 |
| **Project Lead & CEO** | **Huỳnh Thị Yến Duy** — Student ID: **CE191522** |
| **Founding Members** | **Nguyễn Hải Hà** (CTO) • **Nguyễn Nhã Quân** (CPO)<br>**Mã Phú Tín** (Growth) • **Đặng Vĩnh Phúc** (Market) • **Hồ Tuyết Nghi** (CMO) |
| **Live Web MVP Demo** | [https://motion-iq-five.vercel.app](https://motion-iq-five.vercel.app) |
| **Empirical Fieldwork** | 50 Quantitative Field Surveys • 5 In-Person Physical Prototype Testing Sessions |
| **Location & Date** | Can Tho City, November 2026 |

---

# ACKNOWLEDGEMENTS

The MotionIQ project team wishes to express our deepest gratitude and sincerest appreciation to our instructor, **Mr. Tran Ngoc Son**, who has dedicated his profound expertise, innovative entrepreneurial thinking, and structured guidance to mentor our team throughout Checkpoint 1, Checkpoint 2, and Checkpoint 3 of Course EXE101 (Experiential Entrepreneurship).

We also extend our heartfelt thanks to the elderly citizens and families across Can Tho City and the Mekong Delta region who generously participated in our 50 quantitative field surveys and 5 in-person physical prototype testing sessions. Your authentic feedback, enthusiastic encouragement, and honest critiques have served as the guiding compass enabling us to develop an assistive technology platform that is not only technically robust but also deeply humane, empathetic, and culturally tailored.

---

# EXECUTIVE SUMMARY

**MotionIQ** is an assistive AI computer vision technology platform engineered to run 100% on-device (Edge AI) via standard web browsers. The solution is designed specifically to support elderly citizens in tracking their daily physical movement, functional mobility exercises, and balance routines at home through standard smartphone or laptop webcams—eliminating the need for expensive wearable hardware sensors or external devices.

By integrating an endearing virtual assistant mascot named **"Bé Nấm"** (Little Mushroom) with natural, real-time Vietnamese voice guidance, biomechanical kinematic models trained on published human movement datasets (UI-PRMD, KIMORE, EHE), and dynamic One-Euro Filter jitter smoothing, MotionIQ assists seniors in maintaining correct exercise postures, accurately counts repetitions, and delivers immediate supportive feedback. Empirical field research across N = 50 target respondents revealed that over 68% of adult children face severe scheduling constraints that prevent them from directly observing their aging parents' exercises, while 82.4% expressed high willingness to trial our home-based digital platform. Live testing across 5 prototype evaluation sessions demonstrated a **94.6% Range of Motion (ROM) angular measurement accuracy** relative to manual goniometric benchmarks and achieved an outstanding System Usability Scale (SUS) score of **84.5 / 100 (Grade A / Excellent)**.

From a commercial and financial perspective, MotionIQ adopts a customer-value-based and competitive parity pricing strategy with an Early Access introductory tier priced at **49,000 VND / month** (~1,600 VND/day), followed by a Standard tier at **79,000 VND / month**. The initiative operates on a lean 4-month marketing budget of **10,000,000 VND** and a fixed monthly operational overhead of **1,000,000 VND/month**. Break-even analysis proves that reaching just **26 active Early Access subscribers** (or 15 Standard subscribers) generates sufficient Monthly Recurring Revenue (MRR ~1,000,000 VND) to achieve complete **operational self-sufficiency** without requiring ongoing founder out-of-pocket subsidies.

---

# LIST OF ACRONYMS

| Acronym | Full English Term | Vietnamese Definition / Meaning |
| :--- | :--- | :--- |
| **AI** | Artificial Intelligence | Trí tuệ Nhân tạo |
| **BMC** | Business Model Canvas | Khung Mô hình Kinh doanh 9 Khối |
| **ROM** | Range of Motion | Biên độ góc vận động của khớp cơ thể |
| **CAC** | Customer Acquisition Cost | Chi phí thu hút một khách hàng mới |
| **MRR** | Monthly Recurring Revenue | Doanh thu định kỳ hằng tháng |
| **SUS** | System Usability Scale | Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế) |
| **On-Device AI** | On-Device Artificial Intelligence | Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị (Edge AI) |

---

# LIST OF TABLES

- **Table 1.1**: Founding Team Competency Profile & RACI Matrix
- **Table 2.1**: Quantitative Field Survey Findings & Statistical Breakdown (N = 50)
- **Table 2.2**: Competitive Landscape Analysis & Strategic Differentiation Matrix
- **Table 3.1**: 9-Block Business Model Canvas (BMC) Framework
- **Table 3.2**: 4 Standardized Functional Movement Exercises & Kinematic Thresholds
- **Table 3.3**: Empirical Prototype Testing Results across 5 Live Sessions
- **Table 4.1**: 4-Month Lean Marketing Budget Allocation (10,000,000 VND)
- **Table 4.2**: 5-Stage Customer Conversion Funnel & Target Performance KPIs
- **Table 4.3**: Early Access Tier Subscription Revenue Forecast
- **Table 4.4**: Operational Break-Even vs. Capital Recovery Analysis
- **Table 5.1**: Operational Risk Identification, Impact Assessment & Mitigation Framework
- **Table 5.2**: Multi-Stage Sustainability & Technological Evolution Roadmap

---

# TABLE OF CONTENTS

- **ACKNOWLEDGEMENTS**
- **EXECUTIVE SUMMARY**
- **LIST OF ACRONYMS**
- **LIST OF TABLES**
- **CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (Lead: Huỳnh Thị Yến Duy)**
  - 1.1. Demographic Context & Origin of the MotionIQ Initiative
  - 1.2. Organizational Mission, Vision, and Core Values
  - 1.3. Founding Team Competency Profiles & RACI Governance Matrix
- **CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (Leads: Nguyễn Nhã Quân, Đặng Vĩnh Phúc)**
  - 2.1. Empirical Survey Methodology & Sample Scope (N = 50)
  - 2.2. Quantitative Survey Findings from Google Sheets (N = 50)
  - 2.3. Dual Target Customer Personas & Empathy Mapping
  - 2.4. Competitive Landscape Analysis & Positioning Differentiation
- **CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (Leads: Nguyễn Hải Hà, Nguyễn Nhã Quân)**
  - 3.1. 9-Block Business Model Canvas (BMC) Framework
  - 3.2. Technical Architecture & 100% On-Device AI Biomechanical Pipeline
  - 3.3. 4 Standardized Functional Movement Exercises
  - 3.4. Empirical Validation across 5 Live Prototype Testing Sessions
- **CHAPTER 4: COMMUNICATION STRATEGY, FINANCIAL PLANNING & REVENUE GROWTH (Lead: Mã Phú Tín)**
  - 4.1. 4-Month Strategic Communication Objectives
  - 4.2. Dual Customer Segments & Core Value Messaging
  - 4.3. Marketing Channels & Community Engagement Tactics
  - 4.4. 4-Month Communication Implementation Roadmap
  - 4.5. Value-Based & Competitive Parity Pricing Strategy
  - 4.6. Lean Budget Estimation & Operational Cost Structure
  - 4.7. Revenue Growth Plan & Conversion Funnel KPIs
  - 4.8. Revenue Projections, Break-Even Analysis & Strategic Financial Callout
- **CHAPTER 5: RISK MANAGEMENT, SUSTAINABILITY & FUTURE ROADMAP (Lead: Hồ Tuyết Nghi)**
  - 5.1. Operational Risk Identification & Mitigation Framework
  - 5.2. Multi-Stage Sustainability and Strategic Growth Plan
  - 5.3. Project Limitations and Future Technological Roadmap
- **CONCLUSION (Lead: Huỳnh Thị Yến Duy)**

---

# CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (CHECKPOINT 1)
*[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]*

## 1.1. Demographic Context & Origin of the MotionIQ Initiative
Vietnam is undergoing one of the fastest demographic aging processes in the world. According to the General Statistics Office (GSO), the elderly population (aged 60 and older) has surpassed 13.5 million citizens, representing more than 13.5% of the national population. Forecasts indicate that Vietnam will officially transition from an "aging society" to an "aged society" by 2036. Alongside natural biological aging, elderly individuals face widespread musculoskeletal degeneration, sarcopenia (age-related muscle wasting), osteoarthritis, diminished joint mobility, and balance instability, which dramatically increases the risk of accidental falls.

In modern Vietnamese society, adult children in their 20s to 40s (the "sandwich generation") face immense workplace pressures and economic demands, leaving them with very limited time to directly supervise or assist their aging parents' daily physical exercises at home. Meanwhile, professional physical therapy or personalized wellness training centers charge between 150,000 and 300,000 VND per session—a cost that creates an unsustainable financial burden for ordinary households when sustained over months. Consequently, millions of elderly Vietnamese either abandon exercise altogether or practice unguided movements from memory, leading to improper joint postures, severe biomechanical compensations, and increased injury risk.

MotionIQ was conceived to solve this acute societal dilemma. By harnessing computer vision and artificial intelligence operating entirely within standard web browsers (100% On-Device AI), MotionIQ transforms any standard smartphone, tablet, or laptop camera into an intelligent, empathetic home exercise companion. MotionIQ provides immediate posture guidance and natural Vietnamese voice prompts without requiring wearable sensors or invasive hardware, empowering seniors to maintain regular physical activity with complete autonomy and offering peace of mind to working adult children.

## 1.2. Organizational Mission, Vision, and Core Values

### 1. Mission Statement
To empower elderly Vietnamese citizens to maintain daily functional mobility and exercise safely, autonomously, and joyfully at home through accessible, privacy-centric AI technology, while bridging the emotional and caregiving distance between generations in busy modern families.

### 2. Vision Statement
To become the most trusted and widespread digital motion tracking and physical wellness support platform for seniors in Vietnam and Southeast Asia, setting the industry benchmark for ethical, on-device edge AI in non-medical home care.

### 3. Core Values (4T Framework)
- **Thấu cảm (Deep Empathy):** Every product design decision originates from a profound understanding of geriatric physical limitations, psychological needs, and technological fears.
- **Tiện ích (Accessible Simplicity):** Designing a minimalist, intuitive geriatric user interface (Geriatric UX) with large touch targets, zero complex menus, and natural Vietnamese voice feedback.
- **Tin cậy (Absolute Trust & Privacy):** Zero camera streaming, zero cloud video retention. 100% on-device AI guarantees that personal visual data never leaves the user's living room.
- **Thực tiễn (Affordable Practicality):** High-performance assistive technology priced affordably for ordinary Vietnamese households (less than 2,000 VND per day).

## 1.3. Founding Team Competency Profiles & RACI Governance Matrix
The MotionIQ founding team unites six passionate students from FPT University Can Tho Campus, combining diverse skill sets across software engineering, artificial intelligence, product management, multimedia design, and market development:
1. **Huỳnh Thị Yến Duy (Project Lead & CEO — Student ID: CE191522):** Overall project leadership, strategic vision, resource allocation, investor relations, and external stakeholder management.
2. **Nguyễn Hải Hà (Chief Technology Officer — CTO):** Full-stack systems architecture, Next.js 14 engineering, MediaPipe Pose integration, WebGL/WASM acceleration, and One-Euro Filter algorithm development.
3. **Nguyễn Nhã Quân (Chief Product Officer — CPO):** Product requirements document (PRD) formulation, geriatric UX/UI design system, user testing protocols, and feedback engine logic.
4. **Đặng Vĩnh Phúc (Market Research & Language Specialist):** Quantitative survey execution, bilingual localization, academic terminology compliance, and persona empathy mapping.
5. **Mã Phú Tín (Growth & Media Lead):** Omni-channel communication execution, short-form video production (TikTok/Reels), community engagement, and digital conversion funnels.
6. **Hồ Tuyết Nghi (Chief Marketing Officer — CMO):** Marketing positioning, risk governance frameworks, B2C subscription pricing strategies, and customer retention programs.

### Table 1.1: Founding Team Competency Profile & RACI Governance Matrix
| Project Task / Functional Domain | Yến Duy | Hải Hà | Nhã Quân | Vĩnh Phúc | Phú Tín | Tuyết Nghi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Project Ideation & Milestone Management | **A / R** | C | C | I | I | C |
| Software Architecture & AI Pipeline | I | **A / R** | C | I | I | I |
| Product PRD & Geriatric UX/UI Design | C | C | **A / R** | I | C | C |
| Field Survey & Market Research Analysis | C | I | C | **A / R** | I | C |
| Communication Plan & Content Creation | I | I | I | I | **A / R** | C |
| Pricing Strategy & Financial Modeling | **A** | I | C | I | C | **A / R** |
| Risk Governance & Legal Compliance | **A** | C | I | I | I | **A / R** |
| Prototype Testing & User Evaluation | C | C | **A / R** | C | I | I |

*(Note: R = Responsible; A = Accountable; C = Consulted; I = Informed)*

---

# CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)
*[Lead Authors & Editors: Nguyễn Nhã Quân — CPO & Đặng Vĩnh Phúc — Market Specialist]*

## 2.1. Empirical Survey Methodology & Sample Scope (N = 50)
To establish a rigorous, evidence-based foundation for product development, the MotionIQ team conducted an extensive empirical field survey across Can Tho City (Ninh Kieu, Cai Rang, Binh Thuy districts) and neighboring Southwestern provinces during October 2026. Data was collected via a standardized Google Form questionnaire combined with direct in-person interviews with elderly residents at local community centers, senior citizen clubs, and residential neighborhoods. A total of 50 fully validated, high-quality responses were recorded (**N = 50**), comprising 32 adult children (aged 22–45) caring for aging parents and 18 elderly individuals (aged 60–78).

## 2.2. Quantitative Survey Findings from Google Sheets (N = 50)

### Table 2.1: Quantitative Field Survey Findings & Statistical Breakdown (N = 50)
| Survey Indicator / Survey Question | Percentage | Quantitative Count |
| :--- | :---: | :---: |
| Difficulty supervising parents' home exercises due to busy work schedules | **68.0%** | 34 / 50 respondents |
| Seniors experiencing fear of improper posture, joint strain, or falling | **74.0%** | 37 / 50 respondents |
| Willingness to trial an AI camera-based exercise support web application | **82.4%** | 41 / 50 respondents |
| Preference for simple web/app interface requiring zero hardware purchase | **88.0%** | 44 / 50 respondents |
| Strong demand for real-time Vietnamese voice encouragement & counting | **92.0%** | 46 / 50 respondents |
| Willingness to pay: 30,000 – 50,000 VND / month (Introductory Price Range) | **50.0%** | 25 / 50 respondents |
| Willingness to pay: 50,000 – 100,000 VND / month (Standard Price Range) | **28.0%** | 14 / 50 respondents |
| Willingness to pay: Greater than 100,000 VND / month (Premium Range) | **6.0%** | 3 / 50 respondents |

### Key Research Takeaways:
1. **The Core Societal Pain Point is Proven:** Nearly 7 out of 10 working adult children feel guilty and anxious about being unable to supervise their parents' daily physical movement. Concurrently, 74% of seniors experience hesitation and fear of injury when exercising unassisted.
2. **Overwhelming Trial Intent:** 82.4% readiness to trial confirms strong product-market resonance for an accessible home motion tracking solution.
3. **Optimal Commercial Sweet Spot:** Exactly 78.0% of respondents endorsed subscription pricing within the 30,000 to 100,000 VND/month band, directly validating our Early Access pricing at 49,000 VND/month and Standard tier at 79,000 VND/month.

## 2.3. Dual Target Customer Personas & Empathy Mapping

### 1. Economic Buyer Persona — "Trần Minh Triết" (Age: 32)
- **Demographics:** Senior IT Project Manager, living in Ninh Kieu, Can Tho. Monthly income: 25,000,000 VND. Married, caring for 67-year-old mother living separately.
- **Psychographics & Pains:** Works 10 hours daily. Constantly worries that his mother will slip, trip, or strain her knee joints while exercising alone at home. Feels guilty about his busy schedule. Cannot afford 200,000 VND/session for home physical therapy.
- **Desired Gains:** An automated, non-invasive platform that guides his mother to exercise accurately and sends transparent weekly activity summaries to his phone.

### 2. End-User Persona — "Bà Tư" (Nguyễn Thị Mai, Age: 67)
- **Demographics:** Retired primary school teacher, residing in Binh Thuy, Can Tho. Suffers from mild bilateral knee osteoarthritis and mild balance degradation.
- **Psychographics & Pains:** Anxious about becoming a physical or financial burden to her children. Enjoys gentle morning movement but forgets proper posture cues. Intimidated by complex modern apps, tiny text, and English tech jargon. Afraid of camera hacking or privacy violations.
- **Desired Gains:** An inviting, easy-to-read app with large buttons, warm Vietnamese spoken words ("Bác làm rất tốt!"), and zero hardware setup hassles.

## 2.4. Competitive Landscape Analysis & Positioning Differentiation

### Table 2.2: Competitive Landscape Analysis & Strategic Differentiation Matrix
| Evaluation Dimension | MotionIQ (Our Platform) | Freeletics / Nike App | Kaia Health / Sword | Physical Therapy Centers |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Target Demographic** | **Elderly (Aged 60+) & Families** | Young Fitness Enthusiasts | Post-op Clinical Patients | General Medical Patients |
| **Hardware / Sensor Requirements** | **Zero (Standard WebCam)** | Zero (Smartphone) | Wearable Sensors Required | In-Clinic Machinery |
| **AI Processing Location** | **100% On-Device (Zero Cloud)** | Server-side / Cloud | Proprietary Cloud Portal | N/A (Manual Inspection) |
| **Audio Feedback Language** | **Natural Vietnamese Voice** | English / Pre-recorded | English / US Clinicians | In-person Vietnamese |
| **User Privacy Architecture** | **Absolute (RAM purged immediately)** | Cloud Video Streaming | Medical Cloud HIPAA | In-person Observation |
| **Price Point / Affordability** | **49,000 – 79,000 VND / month** | 250,000 – 350,000 VND / mo | $100+ USD / month | 150k – 300k VND / session |

---

# CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)
*[Lead Authors & Editors: Nguyễn Hải Hà — CTO & Nguyễn Nhã Quân — CPO]*

## 3.1. 9-Block Business Model Canvas (BMC) Framework

### Table 3.1: 9-Block Business Model Canvas (BMC) Framework
| BMC Block | Strategic Content & Operational Implementation |
| :--- | :--- |
| **1. Customer Segments (CS)** | • **Dual Segments:**<br>- Economic Buyer: Adult children (aged 22–45) caring for aging parents.<br>- Primary End-User: Elderly citizens (aged 60+) needing daily home functional exercise. |
| **2. Value Propositions (VP)** | • For Seniors: Safe, autonomous exercise tracking with natural Vietnamese voice feedback; zero hardware required; non-intrusive 100% on-device AI privacy.<br>• For Children: Peace of mind regarding parental safety; transparent weekly progress sync. |
| **3. Channels (CH)** | • TikTok & Facebook Reels short-form storytelling; Facebook elderly care communities; Senior Citizen Clubs & Pagoda activations in Can Tho; Direct Web App ([motion-iq-five.vercel.app](https://motion-iq-five.vercel.app)). |
| **4. Customer Relationships (CR)** | • Warm, encouraging virtual assistant mascot "Bé Nấm"; automated daily exercise reminders; responsive Zalo customer support; community wellness challenges. |
| **5. Revenue Streams (RS)** | • B2C Subscriptions: Early Access (49,000 VND/month), Standard (79,000 VND/month), Annual Pass (790,000 VND/year).<br>• Future B2B Licensing: Senior community centers and private nursing residences. |
| **6. Key Resources (KR)** | • Proprietary On-Device AI computer vision algorithms; UI-PRMD / KIMORE benchmark dataset mapping; Next.js 14 web codebase; Multi-disciplinary founding team. |
| **7. Key Activities (KA)** | • Web platform development & UX refinement; On-device model optimization; Short-form video production; Direct community workshops and field testing. |
| **8. Key Partnerships (KP)** | • Local elderly associations and senior physical culture clubs in Can Tho; FPT University entrepreneurial mentorship; Cloud infrastructure providers (Vercel, Supabase). |
| **9. Cost Structure (CS)** | • Fixed OPEX: Web hosting & cloud telemetry (1,000,000 VND/month).<br>• 4-Month Marketing Launch Budget: 10,000,000 VND (digital media ads, printing, offline activations). |

## 3.2. Technical Architecture & 100% On-Device AI Biomechanical Pipeline
MotionIQ is built on modern web technologies including Next.js 14 (App Router), TypeScript, and Tailwind CSS. The computer vision pipeline operates entirely within client-side WebAssembly (WASM) and WebGL contexts via Google MediaPipe Pose, ensuring 100% On-Device execution without streaming video frames to any remote server.

### 1. Mathematical Formulation of Joint Kinematics
To calculate anatomical joint angles (e.g., knee flexion, hip angle, shoulder abduction), MotionIQ computes the 3D forward kinematic vector angle between three sequential skeletal landmarks A, B (the joint vertex), and C using vector dot products and Euclidean norms:

$$\mathbf{u} = \mathbf{x}_A - \mathbf{x}_B, \quad \mathbf{v} = \mathbf{x}_C - \mathbf{x}_B$$

$$\theta = \arccos\left(\frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}\right)$$

### 2. Anthropometric Scale Normalization
Because user distance from the camera and physical height vary across households, coordinates are normalized relative to the torso length:

$$L_{\text{torso}} = \|\mathbf{x}_{\text{hip\_mid}} - \mathbf{x}_{\text{shoulder\_mid}}\|$$

$$d_{\text{norm}} = \frac{d}{L_{\text{torso}}}$$

### 3. Feature Vector Extraction & Classification
For each incoming video frame at 30 FPS, MotionIQ constructs a 132-dimensional feature vector (33 pose landmarks $\times$ $[x, y, z, \text{visibility}]$). This vector is evaluated against an L2-Ridge Regularized Logistic Regression classifier trained on open standardized movement datasets (UI-PRMD, KIMORE):

$$\min_{\mathbf{w}} \sum_{i=1}^N \log\left(1 + e^{-y_i \mathbf{w}^T \mathbf{x}_i}\right) + \lambda \|\mathbf{w}\|_2^2$$

### 4. Dynamic Jitter Smoothing via One-Euro Filter
To prevent frame-to-frame landmark jitter caused by camera noise or ambient lighting changes, MotionIQ implements the adaptive One-Euro Filter. The filter automatically adjusts its cutoff frequency $f_c$ based on the instantaneous velocity of skeletal movement:

$$f_c = f_{c,\min} + \beta \left|\frac{dx}{dt}\right|$$

### 5. Architectural Privacy Safeguards
MotionIQ decodes raw WebCam frames directly into temporary WebGL GPU texture buffers. Once landmark coordinates are extracted by MediaPipe in browser RAM, the raw pixel buffers are immediately discarded by browser garbage collection. No visual images or video recordings are ever written to disk or transmitted over the network.

## 3.3. 4 Standardized Functional Movement Exercises

### Table 3.2: 4 Standardized Functional Movement Exercises & Kinematic Thresholds
| Exercise Name | Primary Functional Objective | Key Kinematic Angles | Recommended Camera Placement |
| :--- | :--- | :--- | :--- |
| **1. Đứng lên – Ngồi xuống (Sit-to-Stand)** | Lower limb power, quadriceps strength & independent mobility | Knee angle: Standing $\ge 150^\circ$, Fully seated $\le 105^\circ$ | Diagonal 45°–90° side view, waist height, 2–3m |
| **2. Đứng thẳng nâng tay (Shoulder Abduction)** | Shoulder joint range of motion, upper body posture & breathing | Arm-torso angle: Neutral $\sim 20^\circ$, Abduction $\ge 85^\circ$ | Direct frontal view (0°), chest height, 2–3m |
| **3. Đứng dang chân (Side Leg Raise)** | Hip abductor strength, lateral pelvic balance & fall prevention | Hip abduction angle: Standing $\sim 15^\circ$, Extended $\ge 35^\circ$ | Direct frontal view (0°), waist height, 2–3m |
| **4. Đứng tấn cơ bản (Assisted Squat)** | Core stability, gluteal activation & knee joint stabilization | Knee angle: Standing $\sim 165^\circ$, Squat depth $\le 115^\circ$ | Diagonal 45° side view, waist height, 2–3m |

## 3.4. Empirical Validation across 5 Live Prototype Testing Sessions

### Table 3.3: Empirical Prototype Testing Results across 5 Live Sessions
| Session # | Target Exercises Tested | ROM Measurement Accuracy | Rep Counting Accuracy | Mean SUS Usability Score |
| :---: | :--- | :---: | :---: | :---: |
| **Session 1** | Sit-to-Stand (Chair) | 92.4% (vs Goniometer) | 96.0% (48/50 reps) | 80.0 / 100 (Grade B) |
| **Session 2** | Shoulder Abduction | 95.1% (vs Goniometer) | 98.0% (49/50 reps) | 82.5 / 100 (Grade A-) |
| **Session 3** | Side Leg Raise | 93.8% (vs Goniometer) | 94.0% (47/50 reps) | 85.0 / 100 (Grade A) |
| **Session 4** | Assisted Squat | 95.5% (vs Goniometer) | 96.0% (48/50 reps) | 86.0 / 100 (Grade A) |
| **Session 5 (Consolidated)** | **All 4 Exercises** | **96.2% (vs Goniometer)** | **98.0% (49/50 reps)** | **89.0 / 100 (Grade A+)** |

- **Overall Mean ROM Accuracy:** 94.6% relative to manual goniometric reference measurements.
- **Mean Repetition Counting Accuracy:** 96.4% across all sessions.
- **Overall System Usability Scale (SUS):** **84.5 / 100** (Grade A / Excellent tier).

---

# CHAPTER 4: COMMUNICATION STRATEGY, FINANCIAL PLANNING & REVENUE GROWTH
*[Lead Author & Editor: Mã Phú Tín — Growth & Media Lead]*

## 4.1. 4-Month Strategic Communication Objectives
1. **Brand Awareness:** Reach 15,000+ views and impressions across Southwestern Vietnam via short-form video and social channels.
2. **Platform Engagement:** Drive 1,500+ web visits to the live interactive MVP web application.
3. **Trial Onboarding:** Acquire 40 to 50 active family trial accounts with direct parent-child participation.
4. **Paid Customer Conversion:** Convert 15 to 20 paying subscribers by Month 4 under the Early Access tier (49,000 VND/month).

## 4.2. Dual Customer Segments & Core Value Messaging
- **For Adult Children (The Economic Buyer):** *"Gửi trọn hiếu tâm, đồng hành cùng sức khỏe cha mẹ mỗi ngày"* (A Gift of Filial Love: Empowering Your Parents' Daily Vitality). Emphasizes peace of mind, automated posture safety, and loving care without intruding on busy working hours.
- **For Elderly Users (The Primary End-User):** *"Tập vui, tập đúng, sống khỏe mỗi ngày cùng Bé Nấm"* (Exercise Joyfully, Move Correctly, Live Vibrantly with Bé Nấm). Emphasizes warm Vietnamese companionship, large readable text, zero tech anxiety, and absolute visual privacy.

## 4.3. Marketing Channels & Community Engagement Tactics
1. **Short-Form Video Marketing (TikTok, Facebook Reels, YouTube Shorts):** Emotional storytelling on caring for aging parents, side-by-side exercise demos with "Bé Nấm".
2. **Facebook Community Groups:** Active engagement in Can Tho family groups and retirement communities.
3. **Direct Community Activations:** Live weekend demonstration booths at senior citizen clubs and pagodas in Can Tho.
4. **Word-of-Mouth & Family Referral Program:** 1 bonus month of access for each successful family referral.

## 4.4. 4-Month Communication Implementation Roadmap
- **Month 1 (Awareness & Emotional Hook):** Launch short-form video series on filial care.
- **Month 2 (Interactive Demos & Community Workshops):** Host demonstration workshops at senior clubs in Ninh Kieu; distribute printed brochures with QR codes.
- **Month 3 (Early Access Launch & Social Proof):** Roll out the Early Access subscription tier (49,000 VND/month) and share authentic user testimonials.
- **Month 4 (Conversion Optimization & Retention Analysis):** Consolidate user feedback, track renewal rates, and optimize high-converting channels.

## 4.5. Value-Based & Competitive Parity Pricing Strategy
- **Free Tier (Trải nghiệm):** 1 core exercise (Sit-to-Stand), 5 sessions/week, full Vietnamese voice guidance. Free forever.
- **Early Access Tier (Tiên phong):** **49,000 VNĐ / month** (~1,600 VNĐ/day). Unlocks all 4 exercises, unlimited workouts, personalized rep targets.
- **Standard Tier (Tiêu chuẩn):** **79,000 VNĐ / month** (~2,600 VNĐ/day). Unlocks all exercises, weekly Zalo summary reports sent to children.
- **Annual Loyalty Pass (Đồng hành Trọn năm):** **790,000 VNĐ / year** (saves 17%, equivalent to ~2,100 VNĐ/day).

## 4.6. Lean Budget Estimation & Operational Cost Structure

### Table 4.1: 4-Month Lean Marketing Budget Allocation (10,000,000 VND)
| Marketing Expenditure Category | Allocated Budget (VND) | Percentage (%) |
| :--- | :---: | :---: |
| Short-Form Video Production & Digital Ads (TikTok / Reels) | 3,500,000 VND | 35.0% |
| Community Outreach & Digital Community Engagement | 2,500,000 VND | 25.0% |
| Direct Community Activations & Senior Clubs Workshops | 2,000,000 VND | 20.0% |
| Printed Materials (Brochures / Standees / Trial Incentives) | 2,000,000 VND | 20.0% |
| **TOTAL 4-MONTH MARKETING BUDGET** | **10,000,000 VND** | **100.0%** |

*Monthly Fixed Operational Overhead (Fixed OPEX):* Approximately **1,000,000 VND / month** (Vercel Pro web application hosting, custom domain, and cloud telemetry sync).

## 4.7. Revenue Growth Plan & Conversion Funnel KPIs

### Table 4.2: 5-Stage Customer Conversion Funnel & Target Performance KPIs
| Conversion Funnel Stage | Target Performance Metric | Stage Conversion Rate |
| :--- | :---: | :---: |
| **Stage 1: Awareness (Total Video Views & Ad Reach)** | 15,000 views / reaches | Baseline Reach |
| **Stage 2: Consideration (Visits to Demo Web Application)** | 1,500 visitors | 10.0% Click-Through Rate |
| **Stage 3: Trial Onboarding (Active Free Trial Registrations)** | 60 family accounts | 4.0% Conversion from Visitors |
| **Stage 4: Paid Conversion (Early Access Subscribers @ 49k)** | **18 paying subscribers** | 30.0% Conversion from Trial |
| **Stage 5: Retention (Month-over-Month Renewal Rate)** | 14 – 15 retained users | 80.0% Retention Rate |

*Customer Acquisition Cost (CAC) Evaluation:*
$$\text{CAC} = \frac{10,000,000\text{ VND}}{15 \text{ to } 20\text{ subscribers}} = 500,000 \text{ – } 666,667\text{ VND per initial subscriber}$$

## 4.8. Revenue Projections, Break-Even Analysis & Strategic Financial Callout

### Table 4.3: Early Access Tier Subscription Revenue Forecast
| Number of Active Paying Subscribers | Projected Monthly Revenue (Gói 49,000 VND) |
| :---: | :---: |
| 10 paying subscribers | 490,000 VND / month |
| 15 paying subscribers | 735,000 VND / month |
| 20 paying subscribers | 980,000 VND / month |

### Break-Even Analysis (Phân tích Điểm hòa vốn):
$$Q_{\text{BE}} = \frac{\text{Fixed Costs}}{\text{Price} - \text{Variable Cost per Subscriber}}$$

Assuming Fixed Operational Costs ($\text{FC}$) = 1,000,000 VND/month and Variable Cloud Sync Cost ($\text{VC}$) = 10,000 VND/subscriber/month:

### Table 4.4: Operational Break-Even vs. Capital Recovery Analysis
| Financial Break-Even Metric | Early Access Tier (49,000 VND) | Standard Tier (79,000 VND) |
| :--- | :---: | :---: |
| Contribution Margin per Subscriber ($P - \text{VC}$) | 39,000 VND | 69,000 VND |
| **Subscribers for Monthly Operational Break-Even (FC = 1.0M/mo)** | **26 subscribers** | **15 subscribers** |
| Subscribers for Full Capital Recovery (Amortizing 10M Marketing over 4 mo) | 90 subscribers / month | 51 subscribers / month |

> ### 📌 STRATEGIC FINANCIAL TAKEAWAY & OPERATIONAL SELF-SUFFICIENCY
> - **Strategic Dynamics of CAC vs. LTV:** The initial nominal CAC (500,000 – 666,667 VND) represents capital spent to reach over 15,000 targeted people and establish early brand presence. Under our SaaS recurring subscription model, an elderly user who retains for 12 to 16 months yields a Customer Lifetime Value (LTV) of 588,000 to 790,000 VND (or 948,000 VND under Standard pricing), guaranteeing **LTV > CAC** and proving healthy long-term unit economics.
> - **Strategic Value of Operational Break-Even:** Reaching **26 active subscribers** (or 15 Standard subscribers) is the vital tipping point. Beyond Month 4, monthly recurring cash flow of ~1,000,000 VND/month eliminates operational burn rate, securing financial self-reliance and establishing a robust platform for scalable regional expansion.

---

# CHAPTER 5: RISK MANAGEMENT, SUSTAINABILITY & FUTURE ROADMAP
*[Lead Author & Editor: Hồ Tuyết Nghi — Chief Marketing Officer]*

## 5.1. Operational Risk Identification & Mitigation Framework

### Table 5.1: Operational Risk Identification, Impact Assessment & Mitigation Framework
| Identified Operational Risk | Concrete Actionable Mitigation Strategy |
| :--- | :--- |
| **1. Elderly tech apprehension & UX barriers** | Minimalist Geriatric UX: high-contrast color palette, extra-large typography, zero complex menus, warm natural Vietnamese voice prompts with adjustable volume and repetition. |
| **2. AI pose tracking ambiguity under varied lighting** | One-Euro Filter jitter smoothing, dynamic confidence thresholds, and explicit graphical camera placement guides (45°–90° diagonal, 2–3m distance). |
| **3. Consumer reluctance to pay monthly subscriptions** | Provide a permanent free tier with 1 core exercise, transparently communicate value additions for paid tiers, and validate the introductory 49,000 VND rate. |
| **4. Inflation of Customer Acquisition Cost (CAC)** | Rigorously monitor acquisition channel ROAS, concentrate on high-conversion local community networks, and leverage organic short-form viral storytelling. |
| **5. User drop-off & subscription churn after 1 month** | Incorporate daily exercise streak gamification with "Bé Nấm", deliver bi-weekly progress milestone badges, and send automated summary alerts to children. |
| **6. Regulatory classification & non-medical compliance** | Prominently display transparent non-medical disclaimers: MotionIQ is an assistive physical wellness support tool for home exercise, NOT a clinical diagnostic device, and never replaces physicians. |
| **7. Personal visual data security & privacy concerns** | 100% On-Device AI architecture processes video frames strictly in temporary volatile browser RAM; frames are immediately purged with zero cloud storage. |

## 5.2. Multi-Stage Sustainability and Strategic Growth Plan
1. **Phase 1: Market Validation & Initial Traction (Months 1–4):**
   - Finalize the production MVP web application and refine geriatric ergonomics.
   - Onboard 40–50 family beta trial accounts across Can Tho City.
   - Validate willingess-to-pay with the Early Access tier (49,000 VND/month).
   - Achieve 15–20 paying subscribers to prove commercial viability.
2. **Phase 2: Stabilization, Optimization & Feature Expansion (Months 5–6):**
   - Enhance pose landmark robustness under dim lighting and varied room angles.
   - Evaluate customer retention rates and introduce the Standard tier (79,000 VND/month).
   - Deploy automated weekly exercise summaries delivered to adult children via Zalo.
   - Progress from operational break-even (26 subscribers) toward full capital recovery.
3. **Phase 3: Regional Scaling & Ecosystem Integration (Months 7–12+):**
   - Expand the exercise library to include gentle mobility routines for wrists, ankles, and neck.
   - Deploy a Zalo Mini App, allowing users to launch MotionIQ instantly without browser logins.
   - Explore B2B partnerships with senior residential communities and retirement villages.

## 5.3. Project Limitations and Future Technological Roadmap

### 1. Current Project Limitations:
- **Ambient Lighting and Apparel Sensitivity:** Monocular computer vision relies on visual contrast. In severely under-lit rooms or when users wear exceptionally loose, baggy traditional garments (e.g., traditional *áo bà ba*), MediaPipe landmark detection confidence may temporarily fluctuate.
- **2D Monocular Camera Depth Perception:** Operating on standard smartphone webcams restricts tracking to monocular 2D/pseudo-3D coordinates. While forward kinematics accurately calculate planar joint angles, subtle rotational plane deviations (e.g., hip internal rotation during squats) require careful camera angle alignment (45°–90°).
- **Geographic Scope of Initial Field Survey:** Empirical survey data (N = 50) and prototype tests were centered in Can Tho City and the Mekong Delta. Expanding to Tier-1 metropolitan areas (Ho Chi Minh City, Hanoi) will capture diverse housing configurations and tech literacy levels.

### 2. Future Technological Roadmap:
- **Zalo Mini App Deployment:** Migrating the client application into the ubiquitous Zalo ecosystem will allow elderly users to launch daily exercises with a single tap, leveraging Zalo's built-in authentication and zero-install footprint.
- **Smart TV & Living Room Adaptation:** Developing a WebOS / Android TV living-room app utilizing large television screens and wide-angle USB webcams, allowing seniors to exercise with crystal-clear visibility from their couch.
- **Multi-Generational Family Companion Dashboard:** Implementing an automated notification system that alerts adult children via SMS/Zalo if their elderly parent misses scheduled exercises for 3 consecutive days or triggers an in-session fall/inactivity watchdog alert.
- **Multi-Modal Wearable Sensor Fusion:** Exploring low-power Bluetooth Low Energy (BLE) integration with smartwatches (Apple Watch, Galaxy Watch) to fuse heart rate and inertial measurement unit (IMU) telemetry with on-device computer vision.

---

# CONCLUSION
*[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]*

The MotionIQ project addresses one of the most pressing socio-demographic challenges facing contemporary Vietnam: empowering an aging population to maintain physical vitality and exercise safely at home, while relieving the constant worry experienced by busy working adult children.

Through an honest, methodical, and evidence-based approach—grounded in empirical field survey data from 50 local families, rigorous biomechanical prototype testing across 5 live sessions, and a disciplined 4-month communication strategy with a lean 10,000,000 VND budget—MotionIQ proves that cutting-edge artificial intelligence can be deployed ethically, securely, and affordably. By guaranteeing 100% on-device visual privacy, adopting intuitive geriatric UX, and establishing clear operational self-sufficiency at just 26 subscribers, MotionIQ demonstrates viable startup potential, sustainable business unit economics, and profound humanistic value.
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Successfully compiled English Markdown report at: {out_path}")

def main():
    base_dir = r"c:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq"
    artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a"
    downloads_dir = r"c:\Users\PC\Downloads"
    public_dir = os.path.join(base_dir, "public")

    docx_filename = "MotionIQ_Final_Report_EXE101_EN.docx"
    md_filename = "MotionIQ_Final_Report_EXE101_EN.md"

    # 1. Generate DOCX in project directory
    docx_project_path = os.path.join(base_dir, docx_filename)
    build_docx(docx_project_path)

    # 2. Generate Markdown in project directory
    md_project_path = os.path.join(base_dir, md_filename)
    build_markdown(md_project_path)

    # 3. Copy to public directory for direct browser download
    os.makedirs(public_dir, exist_ok=True)
    shutil.copy2(docx_project_path, os.path.join(public_dir, docx_filename))
    shutil.copy2(md_project_path, os.path.join(public_dir, md_filename))
    print(f"Copied to public directory: {public_dir}")

    # 4. Copy to Downloads folder for immediate user access
    if os.path.exists(downloads_dir):
        shutil.copy2(docx_project_path, os.path.join(downloads_dir, docx_filename))
        shutil.copy2(md_project_path, os.path.join(downloads_dir, md_filename))
        print(f"Copied to Downloads directory: {downloads_dir}")

    # 5. Copy to Artifact directory
    if os.path.exists(artifact_dir):
        shutil.copy2(docx_project_path, os.path.join(artifact_dir, docx_filename))
        shutil.copy2(md_project_path, os.path.join(artifact_dir, md_filename))
        print(f"Copied to Artifact directory: {artifact_dir}")

    print("\n=======================================================")
    print("ALL DELIVERABLES SUCCESSFULLY GENERATED AND REPLICATED!")
    print("=======================================================")

if __name__ == "__main__":
    main()
