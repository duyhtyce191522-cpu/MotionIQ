import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_full_report(page_dict=None):
    if page_dict is None:
        # Initial estimate / fallback
        page_dict = {
            "ack": "2", "exec": "2", "acro": "3", "tbls": "4", "toc": "5",
            "ch1": "6", "s11": "6", "s12": "6", "s13": "7",
            "ch2": "9", "s21": "9", "s22": "9", "s23": "10", "s24": "11",
            "ch3": "12", "s31": "12", "s32": "13", "s321": "15", "s322": "15",
            "s323": "17", "s324": "18", "s325": "19", "s33": "24", "s331": "24",
            "s332": "25", "s333": "28", "s34": "30",
            "ch4": "31", "s41": "31", "s42": "31", "s43": "31", "s44": "32",
            "s45": "32", "s46": "33", "s47": "34", "s48": "35",
            "ch5": "37", "s51": "37", "s52": "38", "s53": "38", "concl": "39",
            # Tables
            "t11": "Page 7", "t21": "Page 9", "t22": "Page 11",
            "t31": "Page 12", "t32": "Page 13", "t32joints": "Page 20",
            "t32a": "Page 23", "t33": "Page 28", "t34": "Page 30",
            "t41": "Page 31", "t42": "Page 32", "t43": "Page 33",
            "t44": "Page 33", "t45": "Page 34", "t46": "Page 35",
            "t47": "Page 36", "t51": "Page 37"
        }

    doc = docx.Document()

    # Page Margins: Standard Academic 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)   # A4
        section.page_height = Inches(11.69)
        section.different_first_page_header_footer = True

        header = section.header
        hp = header.paragraphs[0]
        hp.text = "MOTIONIQ — Startup Project Final Report (EXE101 Course)"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.paragraph_format.space_after = Pt(4)
        for r in hp.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(128, 128, 128)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "FPT University Can Tho Campus  |  Page "
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fp.paragraph_format.space_before = Pt(4)
        for r in fp.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(128, 128, 128)
        
        # Add page number field to footer
        run_pg = fp.add_run()
        run_pg.font.name = "Times New Roman"
        run_pg.font.size = Pt(9)
        run_pg.font.color.rgb = RGBColor(128, 128, 128)
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        run_pg._r.append(fldSimple)

    def set_cell_background(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def format_table(table, col_widths, data, header_bg="EAE0D5", zebra=True, font_size=9.5, bold_col0=False):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            if r_idx == 0:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

            for c_idx, cell in enumerate(row.cells):
                cell.width = col_widths[c_idx]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

                if r_idx == 0:
                    set_cell_background(cell, header_bg)
                elif zebra and r_idx % 2 == 1:
                    set_cell_background(cell, "FAFAFA")
                else:
                    set_cell_background(cell, "FFFFFF")

                tcPr = cell._tc.get_or_add_tcPr()
                borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="D5C4B3"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="D5C4B3"/><w:left w:val="none"/><w:right w:val="none"/></w:tcBorders>')
                tcPr.append(borders)

                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (r_idx == 0 or c_idx in [1, 2, 4, 5]) else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15

                text_content = str(data[r_idx][c_idx])
                lines = text_content.split("\n")
                for l_idx, line in enumerate(lines):
                    if l_idx > 0:
                        p = cell.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (r_idx == 0 or c_idx in [1, 2, 4, 5]) else WD_ALIGN_PARAGRAPH.LEFT
                        p.paragraph_format.space_before = Pt(1)
                        p.paragraph_format.space_after = Pt(1)
                        p.paragraph_format.line_spacing = 1.15
                    run = p.add_run(line)
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(font_size)
                    if r_idx == 0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(140, 47, 30)
                    elif c_idx == 0 and bold_col0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(40, 40, 40)
                    else:
                        run.font.color.rgb = RGBColor(40, 40, 40)

    def add_p(doc, text="", space_before=0, space_after=6, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=13, color=(30, 30, 30)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
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
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.27)
        row = tbl.rows[0]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        set_cell_background(cell, "FBF8F5")
        set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="B2422D"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        r = p.add_run(equation_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = RGBColor(140, 47, 30)

        if explanation_text:
            p2 = cell.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(4)
            p2.paragraph_format.line_spacing = 1.15
            r2 = p2.add_run(explanation_text)
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(9.5)
            r2.font.italic = True
            r2.font.color.rgb = RGBColor(80, 80, 80)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    def add_callout(doc, title, items):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.27)
        row = tbl.rows[0]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        set_cell_background(cell, "FAF5EE")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="B2422D"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"📌 {title}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(140, 47, 30)

        for item in items:
            pi = cell.add_paragraph()
            pi.paragraph_format.space_before = Pt(2)
            pi.paragraph_format.space_after = Pt(2)
            pi.paragraph_format.line_spacing = 1.15
            ri = pi.add_run(f"• {item}")
            ri.font.name = "Times New Roman"
            ri.font.size = Pt(10)
            ri.font.italic = True
            ri.font.color.rgb = RGBColor(40, 40, 40)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    def add_toc_line(doc, title, page_no, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2 if level == 1 else 1)
        p.paragraph_format.space_after = Pt(2 if level == 1 else 1)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        if level == 2:
            p.paragraph_format.left_indent = Inches(0.25)
        elif level == 3:
            p.paragraph_format.left_indent = Inches(0.45)

        r1 = p.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5 if level == 1 else 10)
        if level == 1:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(140, 47, 30)
        else:
            r1.font.color.rgb = RGBColor(40, 40, 40)

        r2 = p.add_run(f"\t{page_no}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5 if level == 1 else 10)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(80, 80, 80)

    # ==========================================
    # 1. COVER PAGE (PAGE 1)
    # ==========================================
    p_inst = add_p(doc, "MINISTRY OF EDUCATION AND TRAINING\nFPT UNIVERSITY CAN THO", space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, color=(40, 40, 40))
    p_stars = add_p(doc, "———————————————***———————————————", space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=10, color=(140, 47, 30))

    p_course = add_p(doc, "STARTUP PROJECT FINAL REPORT (FINAL REPORT) COURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP", space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=12, color=(178, 66, 45))

    p_proj = add_p(
        doc,
        "MOTIONIQ — AI ASSISTANT PLATFORM SUPPORTING HOME EXERCISE TRACKING FOR THE ELDERLY (100% ON-DEVICE AI)",
        space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14, color=(140, 47, 30)
    )

    p_slogan = add_p(doc, "\"MotionIQ – Home exercise, movement tracking made easier.\"", space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=10.5, color=(100, 100, 100))
    p_slogan_en = add_p(doc, "MotionIQ — Home exercise support platform. AI application supporting the elderly in practicing at home via smartphone camera. Posture tracking, repetition counting, and real-time audio feedback.", space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=9.5, color=(120, 120, 120))

    p_meta = add_p(
        doc,
        "Instructor: Mr. Tran Ngoc Son\n"
        "Student Group Name: MOTIONIQ — Group K19\n"
        "Website Demo MVP: https://motion-iq-five.vercel.app",
        space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=10, color=(50, 50, 50)
    )

    # 3-Column Founding Team Table matching official template
    t_team = doc.add_table(rows=7, cols=3)
    team_widths = [Inches(2.5), Inches(1.8), Inches(1.97)]
    team_data = [
        ("NAME", "STUDENT ID", "CONTRIBUTION"),
        ("Huỳnh Thị Yến Duy", "CE191522", "100%"),
        ("Nguyễn Hải Hà", "CE200298", "100%"),
        ("Nguyễn Nhã Quân", "CE200197", "100%"),
        ("Đặng Vĩnh Phúc", "CE190510", "100%"),
        ("Mã Phú Tín", "CS191066", "100%"),
        ("Hồ Tuyết Nghi", "CS180758", "100%")
    ]
    format_table(t_team, team_widths, team_data, font_size=9.5, bold_col0=True)

    p_loc = add_p(doc, "CAN THO CITY, NOVEMBER 2026", space_before=14, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=10.5, color=(140, 47, 30))

    doc.add_page_break()

    # ==========================================
    # 2. ACKNOWLEDGEMENTS & EXECUTIVE SUMMARY (PAGE 2)
    # ==========================================
    add_h1(doc, "ACKNOWLEDGEMENTS")
    add_p(
        doc,
        "The MotionIQ project team would like to express our deepest gratitude and most sincere thanks to Mr. Tran Ngoc Son, "
        "who has dedicatedly imparted knowledge on innovative startup thinking, business model methodologies, and patiently guided us, "
        "providing invaluable professional feedback through each milestone: Checkpoint 1, Checkpoint 2, and Checkpoint 3 of the EXE101 "
        "course (Startup Experience)."
    )
    add_p(
        doc,
        "The team also wants to sincerely thank the elderly individuals and relatives who enthusiastically participated in 50 survey "
        "responses as well as 5 direct prototype testing sessions of the application. Practical feedback from actual users is the guiding "
        "light that helps the team perfect the MotionIQ product to be the most useful and humane."
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
        "By flexibly combining the virtual assistant character \"Be Nam\" with Vietnamese voice count reminders, a pose recognition "
        "model based on published benchmark motion datasets (UI-PRMD, KIMORE, EHE) and the One-Euro Filter noise reduction filter, "
        "MotionIQ helps seniors maintain proper workout habits, count repetitions, and provide basic feedback. Actual survey results "
        "on 50 subjects show that more than 68% of children face difficulties when directly observing their parents working out, and "
        "82.4% are ready to let their relatives try the application. Practical testing through 5 sessions achieved a range of motion "
        "(ROM) angle measurement index of 94.6% compared to the reference measurement angle and a SUS system usability score of "
        "84.5/100 (Excellent level)."
    )
    add_p(
        doc,
        "Regarding business and financial strategy, the team applies a value-based pricing method and competitor comparison "
        "with an Early Access trial package of 49,000 VND / month (~1,600 VND/day), combined with a concise 4-month communication "
        "plan with a student budget of 10,000,000 VND. Break-even analysis shows that with 26 paying customers for the Early Access "
        "package or 15 customers for the Standard package (79,000 VND/month), the project will self-cover its fixed monthly operating "
        "costs (1,000,000 VND/month), achieving operational self-sufficiency without requiring founder out-of-pocket subsidies."
    )

    doc.add_page_break()

    # ==========================================
    # 3. LIST OF ABBREVIATIONS (PAGE 3)
    # ==========================================
    add_h1(doc, "LIST OF ABBREVIATIONS")
    t_acro = doc.add_table(rows=8, cols=3)
    acro_widths = [Inches(1.5), Inches(2.37), Inches(2.4)]
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

    doc.add_page_break()

    # ==========================================
    # 4. LIST OF TABLES (PAGE 4)
    # ==========================================
    add_h1(doc, "LIST OF TABLES")
    add_p(doc, "List of tables summarizing experimental data, source code algorithms, financials, and operational plans in the report:", italic=True, font_size=10.5, color=(100, 100, 100))
    
    list_tables = [
        ("Table 1.1", "Founding Team Competency Profiles & RACI Governance Matrix", page_dict["t11"]),
        ("Table 2.1", "Quantitative Field Survey Findings & Statistical Breakdown (N = 50)", page_dict["t21"]),
        ("Table 2.2", "Competitive Landscape Analysis & Strategic Positioning Differentiation", page_dict["t22"]),
        ("Table 3.1", "9-Block Business Model Canvas (BMC) Framework", page_dict["t31"]),
        ("Table 3.2", "Profile of Model Files and Core Algorithms in Project Source Code", page_dict["t32"]),
        ("Table 3.2-Joints", "22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics", page_dict["t32joints"]),
        ("Table 3.2a", "Actual Parameters Extracted from Weights File uiprmdQualityModel.json", page_dict["t32a"]),
        ("Table 3.3", "Summary Table of 4 Standardized Functional Exercises in MotionIQ", page_dict["t33"]),
        ("Table 3.4", "Results of 5 Actual MVP Prototype Testing Sessions", page_dict["t34"]),
        ("Table 4.1", "Communication Channels & Operational Implementation Methods", page_dict["t41"]),
        ("Table 4.2", "4-Month Communication Implementation Roadmap", page_dict["t42"]),
        ("Table 4.3", "Proposed Pricing Structure of MotionIQ", page_dict["t43"]),
        ("Table 4.4", "4-Month Lean Student Media Budget Allocation (10,000,000 VND)", page_dict["t44"]),
        ("Table 4.5", "Target Customer Segments & 4-Month Conversion Funnel KPIs", page_dict["t45"]),
        ("Table 4.6", "Early Access Tier Subscription Monthly Revenue Forecast", page_dict["t46"]),
        ("Table 4.7", "Operational Break-Even vs. Full Capital Recovery Analysis", page_dict["t47"]),
        ("Table 5.1", "Identified Operational Risk Matrix & Concrete Mitigation Strategies", page_dict["t51"])
    ]

    for tb_id, tb_title, tb_pg in list_tables:
        p_tb = doc.add_paragraph()
        p_tb.paragraph_format.space_before = Pt(2)
        p_tb.paragraph_format.space_after = Pt(2)
        p_tb.paragraph_format.tab_stops.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_tb.add_run(f"{tb_id}: {tb_title}")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10)
        
        r2 = p_tb.add_run(f"\t{tb_pg}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # 5. TABLE OF CONTENTS (PAGE 5)
    # ==========================================
    add_h1(doc, "TABLE OF CONTENTS")
    add_p(doc, "(Hierarchical Table of Contents with Academic Chapter Structure and Section Lead Authors)", italic=True, font_size=10, color=(100, 100, 100))

    toc_items = [
        ("ACKNOWLEDGEMENTS", page_dict["ack"], 1),
        ("EXECUTIVE SUMMARY", page_dict["exec"], 1),
        ("LIST OF ABBREVIATIONS", page_dict["acro"], 1),
        ("LIST OF TABLES", page_dict["tbls"], 1),
        ("CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (Lead: Huỳnh Thị Yến Duy)", page_dict["ch1"], 1),
        ("1.1. Context of MotionIQ Idea Formation", page_dict["s11"], 2),
        ("1.2. Mission, Vision, and Core Values", page_dict["s12"], 2),
        ("1.3. Founding Team Capability Profiles & RACI Governance Matrix", page_dict["s13"], 2),
        ("CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (Leads: Nguyễn Nhã Quân, Đặng Vĩnh Phúc)", page_dict["ch2"], 1),
        ("2.1. Methodology and Field Survey Scale (N = 50)", page_dict["s21"], 2),
        ("2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)", page_dict["s22"], 2),
        ("2.3. Target Customer Persona & Empathy Mapping", page_dict["s23"], 2),
        ("2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation", page_dict["s24"], 2),
        ("CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (Leads: Nguyễn Hải Hà, Nguyễn Nhã Quân)", page_dict["ch3"], 1),
        ("3.1. 9-Block Business Model Canvas (BMC) Framework", page_dict["s31"], 2),
        ("3.2. Profile of Model Files and Algorithms in Project Source Code", page_dict["s32"], 2),
        ("3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline", page_dict["s321"], 2),
        ("3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)", page_dict["s322"], 2),
        ("3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer", page_dict["s323"], 2),
        ("3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine", page_dict["s324"], 2),
        ("3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset", page_dict["s325"], 2),
        ("3.3. 4 Standardized Functional Exercise Movements", page_dict["s33"], 2),
        ("3.3.1. Principles of Exercise Standardization Based on 3 International Datasets", page_dict["s331"], 2),
        ("3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises", page_dict["s332"], 2),
        ("3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ", page_dict["s333"], 2),
        ("3.4. Results of 5 Actual MVP Prototype Testing Sessions", page_dict["s34"], 2),
        ("CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (Lead: Mã Phú Tín)", page_dict["ch4"], 1),
        ("4.1. 04-Month Media Objectives", page_dict["s41"], 2),
        ("4.2. Target Customers & Key Message", page_dict["s42"], 2),
        ("4.3. Communication Channels & Methods", page_dict["s43"], 2),
        ("4.4. 04-Month Media Implementation Roadmap", page_dict["s44"], 2),
        ("4.5. Value-Based & Competitive Parity Pricing Strategy", page_dict["s45"], 2),
        ("4.6. Budget Estimation and Operating Costs", page_dict["s46"], 2),
        ("4.7. Revenue Development Plan & KPI Targets after 04 Months", page_dict["s47"], 2),
        ("4.8. Revenue Forecast and Break-Even Analysis", page_dict["s48"], 2),
        ("CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY (Lead: Hồ Tuyết Nghi)", page_dict["ch5"], 1),
        ("5.1. Identification of Practical Risks & Mitigation Measures", page_dict["s51"], 2),
        ("5.2. Development and Sustainability Plan by Phase", page_dict["s52"], 2),
        ("5.3. Project Limitations and Future Technological Roadmap", page_dict["s53"], 2),
        ("CONCLUSION (Lead: Huỳnh Thị Yến Duy)", page_dict["concl"], 1)
    ]

    for title, pg, lvl in toc_items:
        add_toc_line(doc, title, pg, lvl)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY
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
        "Maintaining gentle, regular physical activity habits at home plays a vital role in slowing functional decline and sustaining "
        "independent physical mobility. However, in reality, most seniors exercise spontaneously based on unverified habits without knowing "
        "whether their joint angles and spinal alignments are anatomically correct. Meanwhile, busy working adult children cannot constantly "
        "supervise or remind their parents in person. Stemming from the urgent need to care for our own families, the founding team developed "
        "the MotionIQ project — an AI-powered home exercise tracking platform utilizing standard smartphone and laptop cameras to provide "
        "real-time repetition counting, posture verification, and gentle audio encouragement right in the living room."
    )

    add_h2(doc, "1.2. Mission, Vision, and Core Values")
    add_p(
        doc,
        "• Mission: \"Democratizing quality, evidence-based physical exercise support for every Vietnamese household\" — safeguarding "
        "autonomous mobility, minimizing fall risks among the elderly, and providing working children complete peace of mind."
    )
    add_p(
        doc,
        "• Vision: Establishing MotionIQ as Vietnam's premier, widely adopted digital motion-tracking platform for elderly home wellness by 2027."
    )
    add_p(
        doc,
        "• Core Values:\n"
        "1. Safety & Evidence-Based: All movement protocols are grounded in validated geriatric biomechanics and benchmarked against "
        "prestigious public datasets (UI-PRMD, KIMORE, EHE).\n"
        "2. Privacy by Design: 100% On-Device AI processing directly in browser RAM, strictly saying NO to recording or transmitting video "
        "streams to external cloud servers.\n"
        "3. Geriatric Empathy: High-contrast interface, extra-large touch targets (≥ 56px), and warm Vietnamese voice coaching through the \"Bé Nấm\" companion."
    )

    add_h2(doc, "1.3. Founding Team Capability Profiles & RACI Governance Matrix")
    add_p(
        doc,
        "The MotionIQ founding team (Group K19) represents an interdisciplinary synergy combining Information Security, Graphic Design / UI-UX, "
        "Multimedia Communication, Foreign Languages, and Service Management from FPT University Can Tho Campus:"
    )

    # Table 1.1: RACI Matrix
    add_p(doc, "Table 1.1: Founding Team Competency Profiles & RACI Governance Matrix:", bold=True, font_size=11, color=(140, 47, 30))
    t_raci = doc.add_table(rows=7, cols=5)
    raci_widths = [Inches(1.2), Inches(0.9), Inches(1.1), Inches(1.3), Inches(1.77)]
    raci_data = [
        ("Full Name", "Role", "Major", "Assigned Chapter", "RACI Core Responsibilities"),
        ("Huỳnh Thị Yến Duy", "Team Lead / CEO", "Information Security", "Chapter 1, Intro, Conclusion & Review", "Overall project governance, Web architecture, MediaPipe integration, Quality control."),
        ("Nguyễn Nhã Quân", "Product / CPO", "UI-UX Design", "Chapter 2 (2.1, 2.2) & Chapter 3 (3.4)", "Survey data analysis (N=50), Geriatric UI/UX, Prototype usability testing (ROM 94.6%, SUS 84.5)."),
        ("Đặng Vĩnh Phúc", "Market Lead", "Language", "Chapter 2 (2.3, 2.4)", "Competitor landscape benchmark, English academic terminology, Can Tho community elderly outreach."),
        ("Nguyễn Hải Hà", "Tech Lead / CTO", "Information Security", "Chapter 3 (3.2, 3.3)", "Computer vision pipeline, UI-PRMD ML model weights, One-Euro signal filter, RAM privacy."),
        ("Mã Phú Tín", "Growth Lead", "Communication", "Chapter 4 (4.1 – 4.8)", "4-month multi-channel media strategy, TikTok/FB campaigns, 49k pricing model, break-even unit economics."),
        ("Hồ Tuyết Nghi", "Service Lead / CMO", "Service Management", "Chapter 5 (5.1 – 5.3)", "Operational risk matrix, Zalo Mini App expansion roadmap, customer retention framework.")
    ]
    format_table(t_raci, raci_widths, raci_data, font_size=9, bold_col0=True)

    add_callout(
        doc,
        "TEAM STRENGTHS & OPERATIONAL PRINCIPLES",
        [
            "Synergy between AI Technical Expertise and Geriatric Empathy enables low-friction home adoption without specialized sensor hardware.",
            "NON-MEDICAL DISCLAIMER: MotionIQ serves strictly as an assistive physical wellness support tool for home movement tracking, not a medical diagnostic device or clinical replacement for licensed physical therapists."
        ]
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS
    # ==========================================
    add_h1(doc, "CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Nhã Quân — Head of Product; Đặng Vĩnh Phúc — Market Research Lead]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "2.1. Methodology and Field Survey Scale (N = 50)")
    add_p(
        doc,
        "To rigorously validate problem hypotheses and quantify market demand during Checkpoint 2, the team administered a comprehensive "
        "field survey across 50 independent respondents via Google Forms (publicly auditable dataset: "
        "https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM):\n"
        "• Respondent Demographics: 81.6% aged 18–23 and 18.4% aged 23–30, representing working children and grandchildren directly responsible for elderly family care.\n"
        "• Elder Care Experience: 65.3% reported actively assisting elderly parents or grandparents with daily functional mobility over the past 12 months.\n"
        "• Target Age Cohort of Relatives: 28.6% aged 60–69, 24.5% aged 70–79, and 10.2% aged 80+ (totaling 63.3% aged 60 and above; 24.5% aged 50–59; 12.2% under 50)."
    )

    add_h2(doc, "2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)")
    add_p(doc, "Table 2.1: Quantitative Field Survey Findings & Statistical Breakdown (N = 50):", bold=True, font_size=11, color=(140, 47, 30))

    # Table 2.1: Survey Data
    t_survey = doc.add_table(rows=8, cols=3)
    survey_widths = [Inches(2.8), Inches(1.2), Inches(2.27)]
    survey_data = [
        ("Actual Survey Metric (Google Sheets N = 50)", "Observed Rate", "MotionIQ Architectural Implication"),
        ("Children unable to regularly observe and correct parental exercise", "68.6%", "High demand for automated, autonomous home exercise assistant."),
        ("Relatives exercise daily or 3–5 times per week", "51.0%", "Substantial, habitual usage demand requiring daily digital tool availability."),
        ("Primary Pain Point: Unsure of movement accuracy, lack of real-time feedback", "82.4%", "Essential need for real-time auditory posture corrections and rep counting."),
        ("Top Priorities: Ease of use, correct/incorrect feedback, movement coaching", "88.2%", "Mandatory Geriatric UI design: high-contrast text, 56px buttons, 1-touch start."),
        ("MotionIQ concept suitability with family needs (Rated 4–5 Stars)", "66.7%", "Strong product-market fit validation across surveyed households."),
        ("Willingness to let relatives experience MotionIQ (Rated 4–5 Stars)", "82.4%", "Exceptionally high trial readiness and organic customer acquisition potential."),
        ("Acceptance of monthly subscription pricing (50,000 – 149,000 VND / month)", "64.7%", "Confirms Early Access tier (49,000 VND) and Standard tier (79,000 VND) as optimal.")
    ]
    format_table(t_survey, survey_widths, survey_data, font_size=9, bold_col0=True)

    add_p(
        doc,
        "When investigating primary user apprehensions regarding camera-based AI tools (Question 14):\n"
        "1. Image Privacy & Security: 45% expressed privacy concerns regarding living room camera feeds.\n"
        "2. Technological Intimidation: 50% noted that elderly parents struggle with complicated mobile software.\n"
        "3. AI Accuracy on Tremors: 40% questioned whether AI can accurately assess slow, shaky geriatric movements.\n\n"
        "These empirical survey findings directly established MotionIQ's core architectural pillars: 100% On-Device RAM processing to eliminate "
        "privacy fears, Geriatric UI with one-touch navigation and Vietnamese voice coaching to eliminate friction, and the One-Euro Filter "
        "to eradicate joint tremor noise."
    )

    add_h2(doc, "2.3. Target Customer Persona & Empathy Mapping")
    add_p(
        doc,
        "MotionIQ serves a dual-customer profile comprising the Direct User (Elderly) and the Primary Payer (Adult Children):\n"
        "• Persona 1 — Direct User: Mr. Nguyen Van An, 68 years old, retired civil servant living in Can Tho City. Suffers from early-stage knee "
        "osteoarthritis and mild balance loss. Desires daily gentle mobility routines to walk steadily and play with grandchildren. Struggles with small "
        "touchscreens, fears burdening his busy children, and feels unmotivated when practicing alone without feedback.\n"
        "• Persona 2 — Primary Payer: Ms. Thu Hang, 36 years old, corporate office worker in Can Tho. Deeply loves her father but works 9–10 hours "
        "daily, feeling persistent guilt and anxiety over his sedentary isolation. Willing to pay 50,000 – 100,000 VND/month for a dependable "
        "wellness application that tracks her father's exercise safely and provides structured progress transparency."
    )

    add_h2(doc, "2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation")
    add_p(doc, "Table 2.2: Competitive Landscape Analysis & Strategic Positioning Differentiation:", bold=True, font_size=11, color=(140, 47, 30))

    # Table 2.2: Competitive Matrix
    t_comp = doc.add_table(rows=5, cols=4)
    comp_widths = [Inches(1.5), Inches(1.3), Inches(1.8), Inches(1.67)]
    comp_data = [
        ("Competitive Solution", "Key Strengths", "Critical Real-World Limitations", "MotionIQ Positioning Advantage"),
        ("Self-practice via YouTube / TV", "Free, limitless exercise video library.", "Zero real-time feedback, no posture checking, high risk of harmful movements.", "Real-time AI posture verification, rep counting, and immediate spoken guidance."),
        ("In-home Personal Physical Trainer", "1-on-1 personalized supervision and encouragement.", "Very expensive (200k–400k VND/session, 2–4M VND/month), rigid scheduling.", "Extremely affordable (49k–79k VND/month), practice on-demand anytime at home."),
        ("Senior Citizen Community Clubs", "Rich social interaction and peer camaraderie.", "Requires travel, weather-dependent, difficult for seniors with reduced mobility.", "Zero travel required; safe, convenient practice in family living room."),
        ("International Fitness Apps (Freeletics, etc.)", "Modern graphics, extensive workout database.", "English interface, intense routines for youth, high subscription cost (>150k/mo).", "100% localized in Vietnamese, tailored exclusively for elderly gentle mobility.")
    ]
    format_table(t_comp, comp_widths, comp_data, font_size=9, bold_col0=True)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE
    # ==========================================
    add_h1(doc, "CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)")
    add_p(doc, "[Lead Authors & Editors: Nguyễn Hải Hà — Chief Technology Officer; Nguyễn Nhã Quân — Head of Product]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "3.1. 9-Block Business Model Canvas (BMC) Framework")
    add_p(doc, "Table 3.1: 9-Block Business Model Canvas (BMC) Framework:", bold=True, font_size=11, color=(140, 47, 30))

    # Table 3.1: BMC
    t_bmc = doc.add_table(rows=10, cols=2)
    bmc_widths = [Inches(2.0), Inches(4.27)]
    bmc_data = [
        ("BMC Building Block", "MotionIQ Strategic Implementation"),
        ("1. Customer Segments", "Primary Payers: Working adult children aged 25–40 caring for parents.\nDirect Users: Elderly individuals aged 60+ in need of home mobility tracking."),
        ("2. Value Propositions", "Effortless home exercise tracking without sensor hardware.\nAffordable pricing (49,000 – 79,000 VND/month).\nAbsolute image privacy (100% On-Device AI).\nGeriatric empathy UI with Vietnamese voice feedback."),
        ("3. Distribution Channels", "Digital marketing (TikTok, Facebook Fanpage, Zalo Official Account).\nCommunity outreach through Can Tho senior clubs and neighborhood associations."),
        ("4. Customer Relationships", "Friendly \"Bé Nấm\" companion mascot building warm daily habits.\nAutomated exercise reminders and direct technical support via Zalo hotline."),
        ("5. Revenue Streams", "Freemium model (unlimited basic exercise counting).\nEarly Access tier (49,000 VND/month) and Standard tier (79,000 VND/month)."),
        ("6. Key Activities", "Continuous refinement of vision AI and UI-PRMD movement quality models.\nDesigning accessible Geriatric UI/UX.\nProducing short-form elder care educational content.\nCustomer onboarding support."),
        ("7. Key Resources", "Proprietary browser-based pose estimation source code.\nEmpirical One-Euro Filter and UI-PRMD machine learning weights.\nInterdisciplinary student team and \"Bé Nấm\" brand intellectual property."),
        ("8. Key Partnerships", "Can Tho geriatric clubs and residential community associations.\nFPT University academic advisors.\nFamily health online caregiver groups."),
        ("9. Cost Structure", "Lean student operational costs: lightweight web hosting, targeted social media ads, and printed community QR Code guidance brochures.")
    ]
    format_table(t_bmc, bmc_widths, bmc_data, font_size=9, bold_col0=True)

    add_h2(doc, "3.2. Profile of Model Files and Core Algorithms in Project Source Code")
    add_p(
        doc,
        "All technical architecture details presented below are directly extracted from the live MotionIQ production codebase "
        "(src/features/pose/ and scripts/uiprmd/):"
    )

    # Table 3.2: Model Files
    add_p(doc, "Table 3.2: Profile of Model Files and Core Algorithms in Project Source Code:", bold=True, font_size=11, color=(140, 47, 30))
    t_models = doc.add_table(rows=8, cols=3)
    models_widths = [Inches(1.8), Inches(2.2), Inches(2.27)]
    models_data = [
        ("Module / File Name", "Repository Path", "Technical Role & Algorithmic Purpose"),
        ("1. uiprmdQualityModel.json", "src/features/pose/uiprmdQualityModel.json", "Production ML weights file (1,680 JSON lines) storing Z-score normalization parameters (mean, scale), weights, and biases for 132 kinematic features across 4 UI-PRMD exercises."),
        ("2. uiprmdQualityModel.ts", "src/features/pose/uiprmdQualityModel.ts", "Client-side movement quality inference engine: maps 33 MediaPipe landmarks to 22 UI-PRMD joints, normalizes by Torso-Length, pools 132 features, and computes Sigmoid probability."),
        ("3. train_quality_model.mjs", "scripts/uiprmd/train_quality_model.mjs", "Model training pipeline: reconstructs 3D skeleton from Euler rotations via Forward Kinematics, enforces Subject-Separated splitting, and optimizes L2-regularized Logistic Regression."),
        ("4. fetch_uiprmd.py", "scripts/uiprmd/fetch_uiprmd.py", "Data ingestion utility: selectively downloads Kinect joint positions and Euler angles for 4 exercises from Zenodo using HTTP Range Requests without downloading the 400MB full archive."),
        ("5. poseService.ts", "src/features/pose/poseService.ts", "MediaPipe Pose Landmarker orchestrator (WASM & WebGL), background prewarming, automatic GPU/CPU fallback, and adaptive frame-skipping for low-spec mobile chipsets."),
        ("6. landmarkValidator.ts", "src/features/pose/landmarkValidator.ts", "Environmental calibration: measures ambient illuminance (ITU-R BT.601) on 32×24 OffscreenCanvas, estimates standing distance ratio, and validates 5 body regions."),
        ("7. angleCalculator.ts & signalSmoother.ts", "src/features/pose/angleCalculator.ts", "Computes 3D joint angles via vector dot products; filters tremor noise via Exponential Moving Average (EMA), 45° Jump Gate, and One-Euro Filter.")
    ]
    format_table(t_models, models_widths, models_data, font_size=8.5, bold_col0=True)

    add_h3(doc, "3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline")
    add_p(
        doc,
        "To eliminate user privacy apprehensions and guarantee real-time latency without expensive GPU servers, MotionIQ operates "
        "a 100% On-Device AI architecture executed entirely within the client's web browser across four closed-loop layers:\n"
        "1. Computer Vision Layer: MediaPipe Pose Landmarker Lite running via WASM/WebGL extracts 33 body landmarks at 25–30 FPS.\n"
        "2. Environmental Calibration Layer: Continuously monitors room lighting, standing distance, and landmark visibility before allowing workouts to start.\n"
        "3. Mathematical Kinematics Layer: Computes 3D joint angles, filters noise via One-Euro Filter, and drives a 7-state repetition state machine.\n"
        "4. Machine Learning Movement Quality Layer: Normalizes skeletal coordinates and applies Logistic Regression trained on UI-PRMD to detect compensatory errors."
    )

    add_h3(doc, "3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)")
    add_p(
        doc,
        "The computer vision engine (poseService.ts) integrates @mediapipe/tasks-vision (version 0.10.18):\n"
        "• 33-Landmark Skeleton Tracking: Employs pose_landmarker_lite.task (16-bit Float16 quantization) in continuous video stream mode. "
        "Simultaneously outputs normalized 2D/3D screen coordinates and metric 3D world coordinates centered at the pelvis origin.\n"
        "• Background Prewarming: In the static method PoseService.prewarm(), the application pre-initializes the WASM FilesetResolver "
        "as soon as the user opens the web app, ensuring the camera starts instantly without loading delay.\n"
        "• Hardware Fallback: Defaults to GPU WebGL delegate. If WebGL context creation fails on older devices, it automatically falls back to CPU WASM.\n"
        "• Adaptive Frame Skipping: Monitors FPS over 1,000ms intervals. If frame rate drops below 18 FPS for 2 consecutive cycles, it processes only "
        "alternate frames (even frames), prioritizing audio coaching responsiveness until FPS recovers to ≥ 26.\n"
        "• Absolute Image Privacy (Privacy by Design): Video frames are read from HTMLVideoElement strictly into volatile local RAM to compute coordinates, "
        "then immediately garbage-collected. No image or video stream is ever saved or transmitted externally."
    )

    add_h3(doc, "3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer")
    add_p(
        doc,
        "To ensure reliable tracking before rep counting begins, landmarkValidator.ts evaluates three conditions on every video frame:"
    )
    add_p(
        doc,
        "• Step 1 — Ambient Lighting Measurement: Draws video frames to an OffscreenCanvas (32×24 pixels) and computes perceived luminance (Y) "
        "using standard ITU-R BT.601 coefficients:"
    )
    add_equation_box(
        doc,
        "Y = (1 / 768) × Σ_{i=1..768} [ 0.299 × R_i + 0.587 × G_i + 0.114 × B_i ]",
        "Where R_i, G_i, B_i ∈ [0, 255]. Thresholds: Y < 48 → 'too_dark'; Y > 225 → 'too_bright'; 48 ≤ Y ≤ 225 → 'good' (Lighting standard met)."
    )
    add_p(
        doc,
        "• Step 2 — Standing Distance Estimation: Evaluates the bounding ratio of visible landmarks (visibility > 0.35) relative to frame height:"
    )
    add_equation_box(
        doc,
        "bodyHeightRatio = max(y_i) - min(y_i)     (with visibility_i > 0.35)",
        "Thresholds: bodyHeightRatio > 0.90 → 'too_close' (step back); bodyHeightRatio < 0.35 → 'too_far' (step closer); 0.35 ≤ ratio ≤ 0.90 → 'ideal' (2–3 meters)."
    )
    add_p(
        doc,
        "• Step 3 — Anatomical Region Visibility: Verifies visibility across 5 key body segments: Head (0, 7, 8), Hands (15, 16), Hips (23, 24), "
        "Knees (25, 26), and Feet (27–30). Tracking begins only when all regions exceed visibility ≥ 0.40 and overall confidence > 0.30."
    )

    add_h3(doc, "3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine")
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

    add_h3(doc, "3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset")
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
    add_p(doc, "Table 3.2-Joints: 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics:", bold=True, font_size=11, color=(140, 47, 30))
    t_joints = doc.add_table(rows=10, cols=3)
    joints_widths = [Inches(1.8), Inches(2.2), Inches(2.27)]
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
    weights_widths = [Inches(1.2), Inches(0.8), Inches(0.7), Inches(0.9), Inches(1.1), Inches(0.9), Inches(0.67)]
    weights_data = [
        ("Motion Name", "Code", "Dims", "Bias", "Weight Range", "Validation Split", "Accuracy"),
        ("Sit-to-Stand", "m05", "132", "-0.9520", "[-0.7312, +0.4409]", "40 samples (20C/20I)", "95.0%"),
        ("Functional Squat", "m01", "132", "-0.3258", "[-0.5929, +0.8224]", "40 samples (20C/20I)", "72.5%"),
        ("Shoulder Raise", "m07", "132", "-0.8338", "[-0.5428, +0.8700]", "40 samples (20C/20I)", "97.5%"),
        ("Side Leg Raise", "m06", "132", "-0.9935", "[-0.7763, +0.6137]", "40 samples (20C/20I)", "97.5%"),
        ("SYSTEM AVERAGE", "4 Acts", "132", "—", "—", "160 samples (Sub 9,10)", "90.62%")
    ]
    format_table(t_weights, weights_widths, weights_data, font_size=8.5, bold_col0=True)

    add_h2(doc, "3.3. 4 Standardized Functional Exercise Movements")
    add_h3(doc, "3.3.1. Principles of Exercise Standardization Based on 3 International Datasets")
    add_p(
        doc,
        "To ensure scientific rigor, safety, and physical appropriateness for Vietnamese seniors, MotionIQ strictly restricts its exercise "
        "library to functional movements verified across three established public motion research corpora (excluding unsuitable high-impact exercises):\n"
        "1. UI-PRMD Dataset (University of Idaho, DOI: 10.5281/zenodo.23104965): Provides 3D skeletal data across 10 subjects with clinical annotation "
        "of correct and compensatory movement executions. Used directly to train uiprmdQualityModel.json.\n"
        "2. KIMORE Dataset (Kinematic Assessment of Movement and Clinical Scores for Remote Monitoring): Comprises kinematic recordings from 78 subjects "
        "(healthy and motor-impaired), serving as the empirical baseline for target Range of Motion (Target ROM) boundaries in KinematicsLineChart.tsx.\n"
        "3. EHE Dataset (Elderly Home Exercise Dataset): Encompasses 869 repetitions from 25 elderly individuals via home Kinect sensors, providing "
        "empirical calibration for repetition pacing, holding delays (minHoldFrames), and geriatric velocity thresholds."
    )

    add_h3(doc, "3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises")
    add_p(doc, "1. Exercise 1: Sit-to-Stand (System Code: sit-to-stand)", bold=True, color=(140, 47, 30))
    add_p(doc, "• Dataset Mapping Code: UI-PRMD: m05 (Sit-to-stand) | KIMORE: Es4 (Pelvis rotation / Sit-to-stand).")
    add_p(doc, "• Physical Activity Benefits for Older Adults: Transitioning from sitting to standing is one of the most critical functional activities for maintaining independence in daily living for older adults. The exercise directly targets the quadriceps, gluteus maximus, and trains the ability to control the body's center of gravity vertically.")
    add_p(doc, "• Anatomical Landmarks & Tracked Kinematic Angles: The system measures bilateral knee flexion angles via 3 landmarks: Hip (LEFT_HIP 23 / RIGHT_HIP 24) – Knee (LEFT_KNEE 25 / RIGHT_KNEE 26, vertex) – Ankle (LEFT_ANKLE 27 / RIGHT_ANKLE 28), while tracking hip flexion angle (Shoulder 11/12 – Hip 23/24 – Knee 25/26). Target Range of Motion (Target ROM): Transitioning from a seated position on a backed chair (knee angle 90°–125°) to a fully upright standing posture (knee angle reaching 165°–180°).")
    add_p(doc, "• Model Parameter Analysis from Model File (m05 in uiprmdQualityModel.json): The model has a bias coefficient = -0.9520. In the mean (µ) and standard deviation (σ) vectors, variation is strongly concentrated in the vertical Y-axis coordinate of the left/right knee joint (mean σ_Y reaching 0.7586 and 0.7287 times the torso length), along with anterior-posterior Z-axis displacement of the chest and head regions (mean µ_Z of chest = 0.3265, head = 0.3966) as the practitioner leans slightly forward to gain momentum to stand up. The model effectively detects compensatory errors such as: excessive forward trunk leaning, standing up without full knee extension, or shifting weight to one leg. Validation accuracy on Subjects 9 & 10 reached 95.0% (38/40 correct samples).")

    add_p(doc, "2. Exercise 2: Controlled Functional Squat (System Code: squat)", bold=True, color=(140, 47, 30))
    add_p(doc, "• Dataset Mapping Code: UI-PRMD: m01 (Deep squat) | KIMORE: Es5 (Squatting) | EHE Dataset: Squatting.")
    add_p(doc, "• Physical Activity Benefits for Older Adults: Comprehensive strengthening for the lower limb muscle group (quadriceps, hamstrings, glutes) and enhancing knee-ankle ligament stability, helping elderly people walk firmly and reducing the risk of knee buckling when climbing stairs.")
    add_p(doc, "• Anatomical Landmarks & Tracked Kinematic Angles: Simultaneously measures knee flexion angle (Hip 23/24 – Knee 25/26 – Ankle 27/28) and trunk inclination angle (Shoulder 11/12 – Hip 23/24 – Knee 25/26). Target Range of Motion (Target ROM): Lowering the center of gravity under control so that knee flexion stays within the safe zone of 90°–125° (avoiding deep squats that put stress on elderly knee cartilage), maintaining a straight spine, then pushing back up to a standing posture.")
    add_p(doc, "• Model Parameter Analysis from Model File (m01 in uiprmdQualityModel.json): The model has a bias coefficient = -0.3258. Weights with large magnitudes are located in the lower limb joint chain (knee joint displacement weights reach +0.7587 on the left and +0.7320 on the right; Y-axis standard deviation of knee and ankle reach 0.6962–0.7441). The model helps identify common technical errors such as: knee valgus (knees caving inward), shallow squat depth failing to reach muscle activation thresholds, or leaning the head and back too far forward. Validation accuracy on Subjects 9 & 10 reached 72.5% (29/40 correct samples).")

    add_p(doc, "3. Exercise 3: Standing Shoulder Abduction (System Code: shoulder-raise)", bold=True, color=(140, 47, 30))
    add_p(doc, "• Dataset Mapping Code: UI-PRMD: m07 (Standing shoulder abduction) | KIMORE: Es1 (Lifting of the arms) | EHE Dataset: LA (Lifting of arms).")
    add_p(doc, "• Physical Activity Benefits for Older Adults: Improves shoulder joint Range of Motion (Shoulder ROM), prevents frozen shoulder in old age, expands the ribcage to support respiratory function, and maintains upper limb flexibility for daily tasks (such as dressing, combing hair, reaching for items on shelves).")
    add_p(doc, "• Anatomical Landmarks & Tracked Kinematic Angles: Tracks shoulder abduction angle via 3 landmarks: Hip (23/24) – Shoulder (LEFT_SHOULDER 11 / RIGHT_SHOULDER 12, vertex) – Elbow (LEFT_ELBOW 13 / RIGHT_ELBOW 14), combined with checking elbow extension (Shoulder 11/12 – Elbow 13/14 – Wrist 15/16). Target Range of Motion (Target ROM): Raising arms laterally from a resting position alongside the body (0°–20°) to the target angle zone of 90°–150° (maximum 180° depending on individual flexibility) and then lowering them slowly.")
    add_p(doc, "• Model Parameter Analysis from Model File (m07 in uiprmdQualityModel.json): The model has a bias coefficient = -0.8338. Statistical data in the model clearly reflects the kinematic features of upper-limb exercises: standard deviations across all lower-limb joints (hip, knee, ankle) are near zero (mean σ ranging from 0.002 to 0.044 - indicating the legs remain stationary as a base), while standard deviations are highly concentrated at the wrist and hand joints (mean σ_Y reaching 0.3458–0.6225; weights at the wrist and hand reach +0.6867 to +0.8700). The model accurately detects errors such as shoulder shrugging/neck retraction, elbow flexing, or tilting the spine to the opposite side to compensate when the shoulder joint is stiff. Validation accuracy on Subjects 9 & 10 reached 97.5% (39/40 correct samples).")

    add_p(doc, "4. Exercise 4: Standing Side Leg Raise (System Code: side-leg-raise)", bold=True, color=(140, 47, 30))
    add_p(doc, "• Dataset Mapping Code: UI-PRMD: m06 (Standing active straight leg raise / Hip abduction).")
    add_p(doc, "• Physical Activity Benefits for Older Adults: Directly strengthens the gluteus medius and tensor fasciae latae - muscle groups responsible for maintaining lateral pelvic balance during single-leg stance. This is a key exercise helping elderly individuals correct a wobbly gait, prevent staggering, and minimize the risk of sideways falls.")
    add_p(doc, "• Anatomical Landmarks & Tracked Kinematic Angles: Measures hip abduction angle via 3 landmarks: Ipsilateral Shoulder (11/12) or Contralateral Hip – Exercising Hip (23/24, vertex) – Knee (25/26) / Ankle (27/28), while monitoring the knee angle of the lifting leg (Hip 23/24 – Knee 25/26 – Ankle 27/28) to ensure it stays straight (≥ 165°). Target Range of Motion (Target ROM): Lightly holding onto a secure support, lifting the leg straight out to the side to achieve a hip opening angle of 30°–45° while keeping the torso upright.")
    add_p(doc, "• Model Parameter Analysis from Model File (m06 in uiprmdQualityModel.json): The model has a bias coefficient = -0.9935. Prominent features in the model are the sharp contrast in amplitude between the stance leg (low standard deviation σ ≈ 0.05–0.12) and the active leg performing the movement (very high standard deviation at the knee, ankle, and foot: mean σ_X reaching 0.3987–0.4336, mean σ_Y reaching 0.7249–0.7970; weights along the active leg joint chain reach +0.4774 to +0.6137). The model keenly detects two common compensatory errors in elderly individuals with weak hip abductors: (1) Knee flexion when lifting the leg, and (2) Leaning the entire upper body toward the stance leg to create the illusion of lifting the leg higher. Validation accuracy on Subjects 9 & 10 reached 97.5% (39/40 correct samples).")

    # Table 3.3: 4 Exercises Summary
    add_h3(doc, "3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ")
    add_p(doc, "Table 3.3: Summary Table of 4 Standardized Functional Exercises in MotionIQ:", bold=True, font_size=11, color=(140, 47, 30))
    t_ex_sum = doc.add_table(rows=5, cols=6)
    ex_sum_widths = [Inches(1.1), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.2), Inches(0.87)]
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

    # Table 3.4
    add_p(doc, "Table 3.4: Results of 5 Actual MVP Prototype Testing Sessions:", bold=True, font_size=11, color=(140, 47, 30))
    t_proto = doc.add_table(rows=4, cols=3)
    proto_widths = [Inches(2.4), Inches(1.6), Inches(2.27)]
    proto_data = [
        ("Experimental Measurement Metric", "Actual Result", "Evaluation Notes"),
        ("Range of Motion (ROM) Measurement Accuracy", "94.6%", "Compared with standard manual goniometric reference angles."),
        ("Algorithmic Response Latency", "38 ms / frame", "Meets real-time 25–30 FPS standard; voice prompts and rep counts are not delayed."),
        ("System Usability Scale (SUS) Usability Score", "84.5 / 100 points", "Exceptional user satisfaction and geriatric accessibility (Grade A / Excellent).")
    ]
    format_table(t_proto, proto_widths, proto_data, font_size=9.5, bold_col0=True)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT
    # ==========================================
    add_h1(doc, "CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (CHECKPOINT 3)")
    add_p(doc, "[Lead Author & Editor: Mã Phú Tín — Growth & Media Lead]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "4.1. 04-Month Media Objectives")
    add_p(
        doc,
        "Throughout the 4-month initial launch period, MotionIQ focuses on establishing localized brand awareness, driving targeted organic "
        "trials, and converting active trial users into recurring subscribers within a disciplined student budget:\n"
        "1. Brand Awareness: Establish the \"Bé Nấm\" companion image as a warm, reliable exercise supporter for Vietnamese seniors across TikTok and Facebook.\n"
        "2. Targeted Reach: Connect with 150–180 working adult children seeking autonomous mobility solutions for their parents.\n"
        "3. User Activation: Guide 40–50 households to register and complete trial sessions, capturing empirical usability feedback.\n"
        "4. Paying Conversion: Convert 15–20 households into paying subscribers, generating initial recurring operational revenue."
    )

    add_h2(doc, "4.2. Target Customers & Key Message")
    add_p(
        doc,
        "• Primary Payer: Adult children aged 25–40 who work long hours away from home but hold deep concern for their elderly parents' physical health.\n"
        "• Direct User: Seniors aged 60+ requiring simple, gentle, guided movements with clear Vietnamese voice prompts.\n"
        "• Core Slogan: \"MotionIQ – Home exercise, movement tracking made easier.\""
    )

    add_h2(doc, "4.3. Communication Channels & Methods")
    add_p(doc, "Table 4.1: Communication Channels & Operational Implementation Methods:", bold=True, font_size=11, color=(140, 47, 30))

    # Table 4.1: Media Channels
    t_chan = doc.add_table(rows=5, cols=2)
    chan_widths = [Inches(2.0), Inches(4.27)]
    chan_data = [
        ("Media Channel", "Operational Implementation Method"),
        ("TikTok (@motioniq_care)", "Publish short demonstration videos showing the \"Bé Nấm\" companion, real-time rep counting, and heartwarming family care scenarios."),
        ("Facebook Fanpage", "Share geriatric mobility knowledge, infographics on knee and back care, product release updates, and testimonials from early users."),
        ("Zalo Community & Mini App", "Provide 1-on-1 caregiver onboarding support, automated workout reminder notifications, and direct feedback collection."),
        ("Community Outreach", "Conduct live trial workshops at Can Tho senior activity centers and local residential neighborhood clubs.")
    ]
    format_table(t_chan, chan_widths, chan_data, font_size=9, bold_col0=True)

    add_h2(doc, "4.4. 04-Month Media Implementation Roadmap")
    add_p(doc, "Table 4.2: 4-Month Communication Implementation Roadmap:", bold=True, font_size=11, color=(140, 47, 30))

    # Table 4.2: Roadmap
    t_road = doc.add_table(rows=5, cols=3)
    road_widths = [Inches(1.5), Inches(2.6), Inches(2.17)]
    road_data = [
        ("Implementation Stage", "Key Strategic Activities", "Milestone Target Deliverables"),
        ("Month 1: Brand Foundation", "Establish TikTok channel, Facebook Fanpage, and \"Bé Nấm\" brand mascot identity; produce 6 introductory guidance videos.", "Brand launch, reach 2,000 video views, establish core brand positioning."),
        ("Month 2: Awareness & Leads", "Launch targeted content highlighting geriatric fall prevention; initiate community outreach in Can Tho residential clubs.", "Attract 150–180 leads, achieve 6,000 views across platforms."),
        ("Month 3: Trial Activation", "Distribute free 14-day trials to 40–50 households; provide live Zalo coaching; gather SUS feedback and testimonials.", "40–50 trial users onboarded, achieve 80%+ positive trial feedback."),
        ("Month 4: Paid Conversion", "Introduce Early Access package (49,000 VND/month); run referral promotion (refer a friend, get 1 month free).", "Convert 15–20 paying subscribers, generate initial recurring cash flow.")
    ]
    format_table(t_road, road_widths, road_data, font_size=9, bold_col0=True)

    add_h2(doc, "4.5. Value-Based & Competitive Parity Pricing Strategy")
    add_p(
        doc,
        "MotionIQ applies a Value-Based Pricing strategy benchmarked against prevailing alternatives in Vietnam:\n"
        "• In-home personal training costs 200,000 – 400,000 VND per session (2–4M VND/month), making it unaffordable for average families.\n"
        "• YouTube fitness videos are free but offer zero posture validation, creating safety risks for elderly practitioners.\n"
        "• Survey data shows 64.7% of surveyed families readily accept 50,000 – 149,000 VND/month. MotionIQ introduces a highly competitive tier structure:"
    )

    # Table 4.3: Pricing
    add_p(doc, "Table 4.3: Proposed Pricing Structure of MotionIQ:", bold=True, font_size=11, color=(140, 47, 30))
    t_price = doc.add_table(rows=5, cols=3)
    price_widths = [Inches(1.8), Inches(1.8), Inches(2.67)]
    price_data = [
        ("Service Package", "Subscription Price", "Included Features & Customer Value"),
        ("MotionIQ Free", "0 VND (Forever Free)", "Basic repetition counting, 2 introductory exercises, visual pose skeleton feedback."),
        ("Early Access Tier", "49,000 VND / month", "Full access to all 4 UI-PRMD exercises, real-time voice coaching, limited to first 20 subscribers (~1,600 VND/day)."),
        ("Standard Tier", "79,000 VND / month", "Full 4-exercise library, detailed progress charts, automated weekly PDF summaries sent to adult children via Zalo."),
        ("Annual Tier", "790,000 VND / year", "12 months access for the price of 10 months (saves 2 months), priority technical support, personalized routine customization.")
    ]
    format_table(t_price, price_widths, price_data, font_size=9, bold_col0=True)

    add_h2(doc, "4.6. Budget Estimation and Operating Costs")
    add_p(
        doc,
        "To execute the 4-month launch plan, the team established a lean student marketing budget of 10,000,000 VND:"
    )

    # Table 4.4: Budget
    add_p(doc, "Table 4.4: 4-Month Lean Student Media Budget Allocation (10,000,000 VND):", bold=True, font_size=11, color=(140, 47, 30))
    t_bud = doc.add_table(rows=7, cols=3)
    bud_widths = [Inches(2.8), Inches(1.6), Inches(1.87)]
    bud_data = [
        ("04-Month Media Budget Item", "Estimated Cost (VND)", "Budget Allocation Ratio"),
        ("Short-form video production (equipment, props, voiceover)", "3,000,000 VND", "30.0%"),
        ("Targeted Facebook / TikTok advertisements", "3,000,000 VND", "30.0%"),
        ("Community workshop organization & elderly gifts", "2,000,000 VND", "20.0%"),
        ("Local travel and outreach transportation", "700,000 VND", "7.0%"),
        ("QR Code flyers, instructional brochures & banners", "300,000 VND", "3.0%"),
        ("Contingency operating reserve", "1,000,000 VND", "10.0%"),
    ]
    format_table(t_bud, bud_widths, bud_data, font_size=9, bold_col0=True)

    add_p(
        doc,
        "In addition to the media budget, baseline operating costs are maintained lean:\n"
        "• Fixed Costs (FC): 1,000,000 VND / month (lightweight cloud database, domain registration, software licenses).\n"
        "• Variable Costs (VC): 10,000 VND / subscriber / month (payment gateway processing fees via PayOS/MoMo and cloud notification messaging)."
    )

    add_h2(doc, "4.7. Revenue Development Plan & KPI Targets after 04 Months")
    add_p(
        doc,
        "MotionIQ deploys a 5-stage conversion funnel (Reach → Interest → Trial → Conversion → Retention):"
    )

    # Table 4.5: Conversion Funnel
    add_p(doc, "Table 4.5: Target Customer Segments & 4-Month Conversion Funnel KPIs:", bold=True, font_size=11, color=(140, 47, 30))
    t_fun = doc.add_table(rows=6, cols=3)
    fun_widths = [Inches(2.5), Inches(1.8), Inches(1.97)]
    fun_data = [
        ("Funnel Stage & Performance Metric", "4-Month KPI Target", "Conversion Efficiency Analysis"),
        ("Top-of-Funnel Reach (Video views, posts)", "13,000 – 15,000 views", "Baseline organic and sponsored brand impressions across Can Tho."),
        ("Interested Caregivers (Leads)", "150 – 180 leads", "1.1% – 1.2% inquiry rate from total impressions."),
        ("Trial Registrations (Free 14-day trials)", "40 – 50 households", "27% trial signup conversion from interested leads."),
        ("Completed Trial Period (≥ 5 workout sessions)", "30 – 35 households", "70% – 75% retention and habit-forming completion rate."),
        ("Paid Tier Conversions (Paying Subscribers)", "15 – 20 subscribers", "50% paid conversion rate from highly engaged trial households.")
    ]
    format_table(t_fun, fun_widths, fun_data, font_size=9, bold_col0=True)

    add_h2(doc, "4.8. Revenue Forecast and Break-Even Analysis")
    add_p(
        doc,
        "Monthly recurring revenue projections across customer adoption levels on the Early Access plan (49,000 VND/month):"
    )

    # Table 4.6: Revenue Forecast
    add_p(doc, "Table 4.6: Early Access Tier Subscription Monthly Revenue Forecast:", bold=True, font_size=11, color=(140, 47, 30))
    t_rev = doc.add_table(rows=4, cols=3)
    rev_widths = [Inches(2.2), Inches(2.0), Inches(2.07)]
    rev_data = [
        ("Number of Active Paying Customers", "Monthly Gross Revenue", "Net Contribution Margin (after VC)"),
        ("10 Subscribers", "490,000 VND / month", "390,000 VND / month"),
        ("15 Subscribers", "735,000 VND / month", "585,000 VND / month"),
        ("20 Subscribers", "980,000 VND / month", "780,000 VND / month")
    ]
    format_table(t_rev, rev_widths, rev_data, font_size=9.5, bold_col0=True)

    add_p(
        doc,
        "Break-Even Analysis is computed using standard entrepreneurial unit economics formulas:\n"
        "Break-Even Volume: Q_BE = FC / (P - VC)"
    )
    add_equation_box(
        doc,
        "Q_BE = FC / ( P - VC )",
        "Assuming Fixed Costs (FC) = 1,000,000 VND/month and Variable Cost (VC) = 10,000 VND/subscription/month."
    )

    # Table 4.7: Break-Even
    add_p(doc, "Table 4.7: Operational Break-Even vs. Full Capital Recovery Analysis:", bold=True, font_size=11, color=(140, 47, 30))
    t_be = doc.add_table(rows=5, cols=3)
    be_widths = [Inches(2.8), Inches(1.7), Inches(1.77)]
    be_data = [
        ("Break-Even Analysis Metric", "Early Access Tier (49,000 VND)", "Standard Tier (79,000 VND)"),
        ("Unit Contribution Margin (P - VC)", "39,000 VND / subscriber", "69,000 VND / subscriber"),
        ("Subscribers to cover Monthly Operations (FC = 1.0M)", "26 subscribers", "15 subscribers"),
        ("Subscribers to recover 10M Marketing Budget (4 mo.)", "90 subscribers / month", "51 subscribers / month"),
        ("Projected Month 4 Operating Status", "Near Operational Break-Even (20 subs generate 780k net)", "Full Operational Self-Sufficiency Achieved at 15 subs")
    ]
    format_table(t_be, be_widths, be_data, font_size=9, bold_col0=True)

    add_callout(
        doc,
        "FINANCIAL STRATEGY HIGHLIGHTS & OPERATIONAL AUTONOMY",
        [
            "Nature of CAC vs. LTV: The initial CAC (500,000 – 666,667 VND) represents an upfront investment to reach 13,000–15,000 views. Under our subscription model, Customer Lifetime Value (LTV) reaches 588,000 – 790,000 VND when subscribers retain for 12 months or more, guaranteeing LTV > CAC and sustainable unit economics.",
            "Operational Self-Sufficiency: Reaching 26 Early Access subscribers proves operational survival, generating sufficient recurring cash flow to maintain server infrastructure indefinitely while expanding organically through family word-of-mouth."
        ]
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY
    # ==========================================
    add_h1(doc, "CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY (CHECKPOINT 3)")
    add_p(doc, "[Lead Author & Editor: Hồ Tuyết Nghi — Customer Experience & Quality Lead]", italic=True, font_size=11, color=(140, 47, 30))

    add_h2(doc, "5.1. Identification of Practical Risks & Mitigation Measures")
    add_p(
        doc,
        "To ensure safe, sustainable, and legally compliant operation, the team identified seven operational risks and designed targeted mitigations:"
    )

    # Table 5.1: Risks
    add_p(doc, "Table 5.1: Identified Operational Risk Matrix & Concrete Mitigation Strategies:", bold=True, font_size=11, color=(140, 47, 30))
    t_risk = doc.add_table(rows=8, cols=3)
    risk_widths = [Inches(1.8), Inches(1.1), Inches(3.37)]
    risk_data = [
        ("Identified Operational Risk", "Risk Level", "Concrete Engineering & Operational Mitigation Strategy"),
        ("1. Elderly tech apprehension & navigation difficulty", "Medium", "Ultra-simplified Geriatric UI: high-contrast text, 56px touch targets, warm Vietnamese audio instructions, 1-touch workout start."),
        ("2. False rep counts caused by hand/leg tremors", "Medium", "Adaptive One-Euro Filter, 45° Jump Gate noise rejection, and 7-state repetition state machine requiring hysteresis hold frames."),
        ("3. Customer unwillingness to pay after trial", "High", "Value-priced 49,000 VND Early Access tier (~1,600 VND/day); automated weekly progress reports sent to adult children demonstrating value."),
        ("4. High initial Customer Acquisition Cost (CAC)", "Medium", "Prioritize organic community workshops, senior club partnerships, word-of-mouth referral discounts, and engaging short-form TikTok care tips."),
        ("5. User churn after initial novelty fades", "Medium", "Gamified exercise streak calendar, gentle daily habit reminders via Zalo, milestone badges, and encouraging mascot voice lines."),
        ("6. Risk of classification as medical / clinical device", "High", "Strict Non-Medical Disclaimer: position MotionIQ exclusively as home physical wellness support; avoid diagnostic clinical claims."),
        ("7. User privacy and camera surveillance concerns", "High", "100% On-Device AI architecture: video frames are processed exclusively in local RAM and discarded immediately; zero cloud video storage.")
    ]
    format_table(t_risk, risk_widths, risk_data, font_size=8.5, bold_col0=True)

    add_h2(doc, "5.2. Development and Sustainability Plan by Phase")
    add_p(
        doc,
        "The project follows a disciplined three-phase growth trajectory:\n"
        "• Phase 1 — Validation & Launch (Months 1–4): Finalize MVP web prototype, onboard 40–50 trial households, convert 15–20 paying subscribers, validate 49k pricing.\n"
        "• Phase 2 — Stabilization & Optimization (Months 5–6): Optimize AI inference speed, measure 3-month subscriber retention rate, introduce 79k Standard tier, reach operational break-even (26 subscribers).\n"
        "• Phase 3 — Expansion & Community Scaling (Months 7–12): Expand exercise catalog with wrist/ankle routines, deploy Zalo Mini App for zero-install access, pilot B2B partnerships with senior day-care centers in the Mekong Delta."
    )

    add_h2(doc, "5.3. Project Limitations and Future Technological Roadmap")
    add_p(
        doc,
        "While achieving high accuracy and usability, the team candidly recognizes current MVP constraints and outlines future engineering upgrades:\n"
        "• Lighting & Clothing Sensitivity: Extreme backlight or loose, flowing clothing can occasionally impair landmark visibility. Future work will integrate adaptive contrast auto-tuning and multi-frame silhouette estimation.\n"
        "• Single-Angle Monocular Tracking: Relying on a single smartphone camera limits full 360° rotational depth. The roadmap includes multi-view synchronization when users possess both a phone and laptop.\n"
        "• Expanded Exercise Library: Current ML weights cover 4 core functional movements. The team plans to incorporate sitting balance drills, gentle neck stretches, and ankle mobility routines trained on specialized geriatric datasets."
    )

    doc.add_page_break()

    # ==========================================
    # CONCLUSION
    # ==========================================
    add_h1(doc, "CONCLUSION")
    add_p(doc, "[Lead Author & Editor: Huỳnh Thị Yến Duy — Chief Executive Officer (Team Lead)]", italic=True, font_size=11, color=(140, 47, 30))
    add_p(
        doc,
        "The MotionIQ project addresses a pressing, heartfelt societal challenge in contemporary Vietnam: assisting elderly parents in maintaining "
        "regular physical activity and preserving independent mobility while granting busy working children peace of mind."
    )
    add_p(
        doc,
        "Through an authentic, disciplined, and evidence-based approach — supported by an empirical survey of 50 families, 100% On-Device AI "
        "biomechanical tracking, published international datasets (UI-PRMD, KIMORE, EHE), and a balanced 4-month media and financial strategy "
        "with a 10,000,000 VND budget — MotionIQ proves that student-led innovation can create meaningful, accessible, and compassionate "
        "healthcare technology for the community."
    )
    add_p(
        doc,
        "The founding team expresses deep gratitude to the course instructors, academic advisors, and family participants whose mentorship "
        "and candid feedback brought MotionIQ from an initial concept to a validated, working prototype ready for real-world impact.",
        italic=True, font_size=12, color=(100, 100, 100)
    )

    return doc

if __name__ == "__main__":
    doc = create_full_report()
    doc.save("Final_MOTIONIQ.docx")
    print("Initial document generated successfully.")

