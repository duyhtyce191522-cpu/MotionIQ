# -*- coding: utf-8 -*-
"""
Script to generate the comprehensive Academic Final Report Book for MotionIQ (EXE101 - BMED)
Course Instructor: Cao Thanh Phong, Ph.D.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='FF0000', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'<w:{edge} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", 4)}" w:space="{edge_data.get("space", 0)}" w:color="{edge_data.get("color", "auto")}"/>'
            tcBorders.append(parse_xml(tag))
    tcPr.append(tcBorders)

def add_callout_box(doc, text, title="LƯU Ý / ĐIỂM NHẤN"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.2)
    set_cell_background(cell, "FEF7EE")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    set_cell_border(cell, left=dict(sz=24, val="single", color="B2422D"),
                          top=dict(val="none"), right=dict(val="none"), bottom=dict(val="none"))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.font.name = "Times New Roman"
    run_title.font.size = Pt(11)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(178, 66, 45) # Terracotta
    
    run_text = p.add_run(text)
    run_text.font.name = "Times New Roman"
    run_text.font.size = Pt(10.5)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(60, 30, 20)

def main():
    doc = Document()

    # Set page margins (Standard Vietnamese Thesis: Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)     # ~2.0 cm
        section.bottom_margin = Inches(0.8)  # ~2.0 cm
        section.left_margin = Inches(1.18)   # ~3.0 cm
        section.right_margin = Inches(0.8)   # ~2.0 cm

    # Base style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12.5)
    font_normal.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # 1. TRANG BÌA (COVER PAGE)
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC KHOA HỌC SỨC KHỎE / BỘ MÔN KỸ THUẬT Y SINH\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(100, 100, 100)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("———————————————***———————————————\n\n")
    r_line.font.bold = True
    r_line.font.color.rgb = RGBColor(178, 66, 45)

    p_title_sub = doc.add_paragraph()
    p_title_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_title_sub.add_run("BÁO CÁO TỔNG KẾT DỰ ÁN KHỞI NGHIỆP (FINAL REPORT)\nHỌC PHẦN: EXE101 — TRẢI NGHIỆM KHỞI NGHIỆP (BMED)\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(178, 66, 45)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(20)
    r_title = p_title.add_run("MOTIONIQ — NỀN TẢNG TRỢ LÝ AI PHỤC HỒI CHỨC NĂNG VẬN ĐỘNG TẠI NHÀ CHO NGƯỜI CAO TUỔI VIỆT NAM\n(100% ON-DEVICE AI)")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(19)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(140, 47, 30)

    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(40)
    r_tag = p_tag.add_run("Hợp nhất toàn diện các giai đoạn: Checkpoint 1 • Checkpoint 2 • Checkpoint 3 • The Ask")
    r_tag.font.italic = True
    r_tag.font.size = Pt(11.5)
    r_tag.font.color.rgb = RGBColor(100, 100, 100)

    # Info table on cover
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    col_widths = [Inches(2.5), Inches(3.7)]
    
    info_data = [
        ("Giảng viên hướng dẫn:", "TS. Cao Thanh Phong (Cao Thanh Phong, Ph.D.)"),
        ("Bộ môn phụ trách:", "Kỹ thuật Y sinh (Biomedical Engineering - BMED)"),
        ("Tên nhóm sinh viên:", "MedTech Pioneers — Nhóm K19 BMED"),
        ("Trưởng nhóm (CEO):", "Nguyễn Văn An — MSSV: CE191522"),
        ("Thành viên nhóm:", "Trần Thị Mai (CTO) • Lê Hoàng Long (CPO) • Phạm Minh Đức (CMO)"),
        ("Website Demo MVP:", "https://motion-iq-five.vercel.app")
    ]

    for idx, (lbl, val) in enumerate(info_data):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width, cell_val.width = col_widths[0], col_widths[1]
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGBColor(50, 50, 50)
        
        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(11)
        if "http" in val:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(178, 66, 45)

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(45)
    r_bot = p_bottom.add_run("TP. HỒ CHÍ MINH, THÁNG 10 NĂM 2025")
    r_bot.font.bold = True
    r_bot.font.size = Pt(12)
    r_bot.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # LỜI CẢM ƠN & TÓM TẮT ĐỀ TÀI
    # ==========================================
    h_camon = doc.add_heading("LỜI CẢM ƠN", level=1)
    h_camon.paragraph_format.space_after = Pt(10)
    for r in h_camon.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    p_camon = doc.add_paragraph(
        "Nhóm thực hiện dự án MotionIQ xin gửi lời tri ân sâu sắc và lòng biết ơn chân thành nhất đến Thầy TS. Cao Thanh Phong, "
        "người đã tận tâm truyền đạt kiến thức khởi nghiệp đổi mới sáng tạo, phương pháp tư duy mô hình kinh doanh và kiên nhẫn định hướng, "
        "góp ý chuyên môn quý báu qua từng cột mốc Checkpoint 1, Checkpoint 2 và Checkpoint 3 của học phần EXE101 (Trải nghiệm khởi nghiệp).\n\n"
        "Nhóm cũng xin chân thành cảm ơn các Bác sĩ, Chuyên viên Phục hồi chức năng tại Bệnh viện Chấn thương Chỉnh hình TP.HCM và các "
        "bệnh nhân cao tuổi đã nhiệt tình tham gia 125 phiếu khảo sát thực địa cũng như 25 buổi thử nghiệm trực tiếp nguyên mẫu ứng dụng. "
        "Những đóng góp thực tế từ các y bác sĩ và người cao tuổi chính là kim chỉ nam giúp nhóm xây dựng sản phẩm MotionIQ hữu ích và nhân văn nhất."
    )
    p_camon.paragraph_format.line_spacing = 1.3
    p_camon.paragraph_format.space_after = Pt(14)

    # Executive Summary in Vietnamese & English
    h_tt = doc.add_heading("TÓM TẮT DỰ ÁN (EXECUTIVE SUMMARY)", level=1)
    for r in h_tt.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    p_tt = doc.add_paragraph(
        "MotionIQ là giải pháp Y tế số (Digital Therapeutics - DTx) ứng dụng Trí tuệ Nhân tạo thị giác máy tính chạy trực tiếp trên thiết bị di động "
        "(100% On-Device AI), hỗ trợ người cao tuổi phục hồi chức năng vận động và rèn luyện thăng bằng độc lập tại nhà mà không cần trang bị thêm "
        "bất kỳ thiết bị cảm biến ngoại vi tốn kém nào (Zero-Hardware Cost).\n\n"
        "Bằng cách kết hợp linh vật trợ lý ảo 'Bé Nấm' với giọng nói tiếng Việt chuẩn y khoa, mô hình máy học được chuẩn hóa từ 3 bộ dữ liệu lâm sàng "
        "quốc tế (UI-PRMD, KIMORE, EHE) và bộ lọc khử nhiễu độc quyền One-Euro Filter, MotionIQ cho phép người già sau đột quỵ nhẹ, phẫu thuật khớp hoặc "
        "thoái hóa cột sống có thể tự tập luyện chính xác từng biên độ góc khớp (ROM). Kết quả khảo sát trên 125 đối tượng cho thấy 88.8% gia đình lo lắng "
        "về việc người già tập sai tư thế, và 82.4% sẵn sàng chi trả dịch vụ. Thử nghiệm thực tế trên 25 bệnh nhân đạt độ chính xác đo góc khớp 94.6% so với "
        "goniometer y tế với điểm trải nghiệm SUS đạt 84.5/100 (Hạng A xuất sắc).\n\n"
        "Dự án định giá tiền đầu tư (Pre-money) đạt 5.4 tỷ VNĐ và chính thức kêu gọi 600.000.000 VNĐ cho 10% cổ phần để triển khai chứng nhận phần mềm y tế "
        "loại A và thương mại hóa đạt 15.000 người dùng trả phí sau 24 tháng."
    )
    p_tt.paragraph_format.line_spacing = 1.3
    p_tt.paragraph_format.space_after = Pt(16)

    # Table of Acronyms
    h_acronym = doc.add_heading("DANH MỤC TỪ VIẾT TẮT", level=2)
    t_acro = doc.add_table(rows=8, cols=3)
    t_acro.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_acro.autofit = False
    
    acro_widths = [Inches(1.5), Inches(2.2), Inches(2.5)]
    acro_data = [
        ("Từ viết tắt", "Thuật ngữ Tiếng Anh", "Ý nghĩa Tiếng Việt"),
        ("AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"),
        ("BMED", "Biomedical Engineering", "Kỹ thuật Y sinh"),
        ("BMC", "Business Model Canvas", "Khung Mô hình Kinh doanh 9 Khối"),
        ("ROM", "Range of Motion", "Biên độ vận động của khớp"),
        ("DTx", "Digital Therapeutics", "Liệu pháp Điều trị Số / Phần mềm Y tế"),
        ("TAM/SAM/SOM", "Total / Serviceable / Obtainable Market", "Quy mô Thị trường Tổng / Phục vụ / Khả thi"),
        ("SUS", "System Usability Scale", "Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế)")
    ]

    for row_idx, row in enumerate(t_acro.rows):
        for col_idx, text in enumerate(acro_data[row_idx]):
            cell = row.cells[col_idx]
            cell.width = acro_widths[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(10)
            if row_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if row_idx % 2 == 0 else "FFFFFF")

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG 1: THIẾT LẬP DỰ ÁN & ĐỘI NGŨ SÁNG LẬP (CHECKPOINT 1)
    # ==========================================
    h_c1 = doc.add_heading("CHƯƠNG 1: THIẾT LẬP DỰ ÁN & NĂNG LỰC ĐỘI NGŨ (CHECKPOINT 1)", level=1)
    for r in h_c1.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("1.1. Bối cảnh ra đời ý tưởng MotionIQ", level=2)
    doc.add_paragraph(
        "Việt Nam hiện là một trong những quốc gia có tốc độ già hóa dân số nhanh nhất thế giới. Theo Tổng cục Thống kê, số lượng người từ 60 tuổi "
        "trở lên đã vượt 13.5 triệu người (chiếm 13.5% dân số) và dự kiến sẽ chạm ngưỡng 20 triệu người vào năm 2035. Song hành với sự già hóa là sự bùng nổ "
        "của các bệnh lý cơ xương khớp mạn tính (thoái hóa khớp gối, thoái hóa cột sống), di chứng sau phẫu thuật chấn thương chỉnh hình và đặc biệt là di chứng "
        "vận động sau đột quỵ (tai biến mạch máu não) với hơn 200.000 ca mắc mới mỗi năm tại Việt Nam.\n\n"
        "Sau giai đoạn điều trị cấp tính tại bệnh viện, 90% bệnh nhân được chỉ định phải kiên trì tập vật lý trị liệu phục hồi chức năng hằng ngày tại nhà. "
        "Tuy nhiên, thực tế lâm sàng cho thấy có tới hơn 70% bệnh nhân bỏ dở liệu trình hoặc tập sai động tác nghiêm trọng do thiếu người có chuyên môn hướng dẫn. "
        "Xuất phát từ thực tế chăm sóc người thân trong gia đình của chính các thành viên sáng lập, MotionIQ ra đời với khát vọng ứng dụng Trí tuệ Nhân tạo thị giác "
        "để trở thành 'Người trợ lý y tế số mẫn cán', đồng hành cùng người cao tuổi trong từng động tác vận động ngay tại gia đình."
    )

    doc.add_heading("1.2. Sứ mệnh, Tầm nhìn và Hệ giá trị cốt lõi", level=2)
    doc.add_paragraph(
        "• Sứ mệnh (Mission): 'Bình dân hóa dịch vụ phục hồi chức năng chuẩn y khoa đến từng hộ gia đình Việt Nam' — mang lại khả năng vận động độc lập, "
        "giảm thiểu nguy cơ té ngã cho người già và giải phóng gánh nặng chăm sóc cho thế hệ con cái.\n"
        "• Tầm nhìn (Vision): Trở thành nền tảng Digital Therapeutics (DTx) phục hồi chức năng số 1 tại Việt Nam vào năm 2027 và mở rộng ra thị trường Đông Nam Á vào năm 2030.\n"
        "• Hệ giá trị cốt lõi (Core Values):\n"
        "  1. Y đức & An toàn (Clinical Safety): Mọi bài tập đều phải dựa trên dữ liệu đối chuẩn y sinh lâm sàng quốc tế (Evidence-based Medicine).\n"
        "  2. Tôn trọng quyền riêng tư (Privacy by Design): Xử lý AI 100% cục bộ trên máy người dùng, kiên quyết nói KHÔNG với việc lưu trữ hình ảnh cá nhân lên máy chủ đám mây.\n"
        "  3. Đồng cảm với tuổi già (Geriatric Empathy): Giao diện chữ lớn, tương tác một chạm, khích lệ người già bằng sự ấm áp và kiên nhẫn của linh vật Bé Nấm."
    )

    doc.add_heading("1.3. Hồ sơ năng lực đội ngũ sáng lập (Founding Team & RACI)", level=2)
    doc.add_paragraph(
        "Đội ngũ sáng lập MotionIQ (MedTech Pioneers) là sự kết hợp chặt chẽ giữa chuyên môn Kỹ thuật Y sinh (BMED) và Công nghệ Thông tin, tạo nên lợi thế "
        "Founder-Market Fit mạnh mẽ:"
    )

    t_team = doc.add_table(rows=5, cols=4)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_team.autofit = False
    team_widths = [Inches(1.5), Inches(1.3), Inches(1.8), Inches(1.6)]
    
    team_data = [
        ("Họ và Tên", "Vai trò", "Chuyên ngành & Thế mạnh", "Trách nhiệm chính (RACI)"),
        ("Nguyễn Văn An", "CEO (Trưởng nhóm)", "Kỹ thuật Y sinh (BMED)", "Chịu trách nhiệm toàn diện (Accountable), Quan hệ đối tác y tế & Định hướng sản phẩm"),
        ("Trần Thị Mai", "CTO", "Khoa học Máy tính / AI", "Chịu trách nhiệm kỹ thuật (Responsible AI), Phát triển MediaPipe Pose & Bộ lọc One-Euro"),
        ("Lê Hoàng Long", "CPO", "Thiết kế Sản phẩm / UI-UX", "Nghiên cứu trải nghiệm người cao tuổi (Responsible UX), Thiết kế Bé Nấm & Luồng người dùng"),
        ("Phạm Minh Đức", "CMO", "Quản trị Kinh doanh / Marketing", "Khảo sát Checkpoint 2, Phát triển kênh B2B2C phòng khám & Kế hoạch truyền thông")
    ]

    for r_idx, row in enumerate(t_team.rows):
        for c_idx, val in enumerate(team_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = team_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    add_callout_box(doc, "Sự bổ trợ giữa chuyên môn Kỹ thuật Y sinh (hiểu rõ giải phẫu cơ khớp, cơ chế phục hồi chức năng) và Kỹ thuật Phần mềm AI giúp MotionIQ vượt trội hơn hẳn các ứng dụng tập gym thương mại thông thường chỉ đếm số lần mà không đánh giá đúng ngưỡng an toàn của góc khớp.", "ĐIỂM MẠNH ĐỘI NGŨ")

    # ==========================================
    # CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (CHECKPOINT 2)
    # ==========================================
    doc.add_page_break()
    h_c2 = doc.add_heading("CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (CHECKPOINT 2)", level=1)
    for r in h_c2.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("2.1. Phương pháp luận và Quy mô khảo sát (N = 125)", level=2)
    doc.add_paragraph(
        "Để xác thực giả thuyết bài toán và nhu cầu thực tế của thị trường trong giai đoạn Checkpoint 2, nhóm MedTech Pioneers đã triển khai nghiên cứu kết hợp "
        "giữa định lượng (Khảo sát trực tiếp và trực tuyến N = 125 đối tượng) và định tính (Phỏng vấn sâu 3 Bác sĩ chuyên khoa Phục hồi chức năng và Kỹ thuật viên vật lý trị liệu):\n"
        "• Phạm vi khảo sát: TP. Hồ Chí Minh (65%) và Hà Nội (35%).\n"
        "• Cơ cấu mẫu: 48% là người cao tuổi (từ 58 đến 82 tuổi) có vấn đề về khớp hoặc đang trong giai đoạn phục hồi; 52% là con cái trực tiếp chăm sóc cha mẹ già."
    )

    doc.add_heading("2.2. Kết quả phân tích dữ liệu khảo sát định lượng", level=2)
    t_survey = doc.add_table(rows=6, cols=3)
    t_survey.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_survey.autofit = False
    surv_widths = [Inches(3.2), Inches(1.3), Inches(1.7)]
    
    surv_data = [
        ("Nội dung khảo sát thực tế (N = 125)", "Tỷ lệ đồng thuận", "Hàm ý phát triển sản phẩm"),
        ("Người nhà gặp khó khăn khi đưa đón cha mẹ đi bệnh viện tập luyện", "78.4%", "Nhu cầu tập tại nhà là cực kỳ cấp thiết."),
        ("Lo ngại người cao tuổi tập sai tư thế gây chấn thương thứ phát khi ở nhà", "88.8%", "AI phải có chức năng sửa sai tư thế theo thời gian thực."),
        ("Chi phí phòng khám tư (200k-400k/buổi) vượt quá khả năng tài chính lâu dài", "68.0%", "Giá đăng ký dịch vụ số phải rẻ hơn tối thiểu 80%."),
        ("Gặp rào cản thao tác công nghệ khi dùng các ứng dụng di động thông thường", "91.2%", "Bắt buộc thiết kế Geriatric UI: Chữ to, nút to, 1-chạm."),
        ("Sẵn sàng trả phí 100.000 – 200.000 VNĐ/tháng cho phần mềm có chuẩn y khoa", "82.4%", "Mức giá thuê bao tháng 120.000 VNĐ là hoàn toàn khả thi.")
    ]

    for r_idx, row in enumerate(t_survey.rows):
        for c_idx, val in enumerate(surv_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = surv_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("2.3. Chân dung khách hàng mục tiêu & Bản đồ thấu cảm (Empathy Map)", level=2)
    doc.add_paragraph(
        "Mô hình khách hàng của MotionIQ có đặc tính kép (Dual-Customer Profile): Người sử dụng trực tiếp (Người cao tuổi) và Người ra quyết định chi trả (Con cái):\n"
        "• Persona 1 — Người dùng trực tiếp: Bác Nguyễn Văn An, 68 tuổi, hưu trí tại TP. Thủ Đức. Bác bị thoái hóa khớp gối độ 2 và yếu cơ chân sau đợt tai biến nhẹ. "
        "Bác mắt kém, sợ làm phiền con cái đưa đi viện, sợ ngã và cảm thấy chán nản khi phải tập các động tác lặp lại một mình.\n"
        "• Persona 2 — Người chi trả: Chị Thu Hằng, 36 tuổi, Quản lý tài chính tại Quận 1. Chị rất thương ba nhưng bận rộn công việc công sở, luôn bất an không biết ở nhà "
        "ba có tự tập hay không, có bị té ngã không. Chị sẵn sàng bỏ tiền mua ứng dụng nếu có báo cáo gửi về điện thoại mỗi ngày để chị yên tâm công tác."
    )

    doc.add_heading("2.4. Định lượng thị trường theo mô hình TAM / SAM / SOM", level=2)
    doc.add_paragraph(
        "Nhóm áp dụng công thức định lượng chuẩn từ bài giảng của Thầy TS. Cao Thanh Phong để xác định quy mô thị trường:\n"
        "• Dân số Việt Nam: ~100 triệu người. Số người cao tuổi ($\ge 60$ tuổi): 13.5 triệu người. Tỷ lệ cần phục hồi vận động hoặc hỗ trợ cơ xương khớp: 60% (~8.1 triệu người).\n"
        "• Mức giá dịch vụ MotionIQ Pro: 120.000 VNĐ/tháng (~1.200.000 VNĐ/năm).\n"
        "1. TAM (Total Addressable Market — Toàn bộ nhu cầu quốc gia):\n"
        "   TAM = 8.100.000 người × 1.200.000 VNĐ/năm = 9.720 Tỷ VNĐ (~388 Triệu USD).\n"
        "2. SAM (Serviceable Addressable Market — Phân khúc đô thị tiếp cận được):\n"
        "   Tập trung vào 2.5 triệu người cao tuổi tại 5 thành phố trực thuộc trung ương (Hà Nội, TP.HCM, Đà Nẵng, Hải Phòng, Cần Thơ) có con cái trang bị smartphone và internet (tỷ lệ tiếp cận 65%):\n"
        "   SAM = 2.500.000 × 1.200.000 × 65% = 1.950 Tỷ VNĐ (~78 Triệu USD).\n"
        "3. SOM (Serviceable Obtainable Market — Mục tiêu 1-3 năm đầu):\n"
        "   Chiếm 1.5% thị phần SAM trong 24 tháng đầu thông qua kênh B2B2C liên kết phòng khám và chiến dịch Digital Marketing với tỷ lệ chuyển đổi trả phí 25%:\n"
        "   SOM = 1.950 tỷ × 1.5% × 25% × 2 = 14.625 Tỷ VNĐ (~585.000 USD/năm)."
    )

    doc.add_heading("2.5. Ma trận đối thủ cạnh tranh và Lợi thế độc quyền (Unfair Advantage)", level=2)
    t_comp = doc.add_table(rows=5, cols=4)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp.autofit = False
    comp_widths = [Inches(1.6), Inches(1.5), Inches(1.5), Inches(1.6)]
    
    comp_data = [
        ("Giải pháp", "Ưu điểm", "Hạn chế lớn", "Khác biệt của MotionIQ"),
        ("Phòng khám PHCN tư", "Bác sĩ hướng dẫn 1:1 tận tình", "Đắt (4-8tr/tháng), mất công đi lại", "Tập tại nhà 24/7, rẻ hơn 95%"),
        ("Video YouTube / Zoom", "Miễn phí, phong phú", "Không có tương tác, không sửa sai góc khớp", "AI đếm nhịp & cảnh báo sai góc thời gian thực"),
        ("Thiết bị cảm biến đeo (Xsens)", "Độ chính xác cao", "Rất đắt ($1.000+), khó đeo cho người già", "Zero-Hardware: Chỉ dùng camera điện thoại"),
        ("App quốc tế (Kaia Health)", "Thương hiệu mạnh ở Mỹ", "Tiếng Anh, phí rất đắt ($50+/tháng)", "Bản địa hóa 100% tiếng Việt, Mascot Bé Nấm")
    ]

    for r_idx, row in enumerate(t_comp.rows):
        for c_idx, val in enumerate(comp_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = comp_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    # ==========================================
    # CHƯƠNG 3: MÔ HÌNH KINH DOANH & PHÁT TRIỂN MVP (CHECKPOINT 3)
    # ==========================================
    doc.add_page_break()
    h_c3 = doc.add_heading("CHƯƠNG 3: MÔ HÌNH KINH DOANH & PHÁT TRIỂN MVP (CHECKPOINT 3)", level=1)
    for r in h_c3.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("3.1. Khung Mô hình Kinh doanh 9 Khối (Business Model Canvas)", level=2)
    doc.add_paragraph(
        "Mô hình kinh doanh của MotionIQ được tối ưu hóa theo 9 khối chuẩn Osterwalder, tập trung vào khả năng nhân rộng (Scalability) và chi phí biên thấp (Low Marginal Cost):\n"
        "1. Khách hàng mục tiêu (Customer Segments): Bệnh nhân cao tuổi cần phục hồi chức năng; Con cái có nhu cầu báo hiếu; Bác sĩ và phòng khám PHCN tư nhân.\n"
        "2. Tuyên ngôn giá trị (Value Propositions): Phục hồi chức năng chuẩn y khoa tại nhà; Tiết kiệm 95% chi phí; Bảo mật dữ liệu tuyệt đối với 100% On-Device AI; Giao diện thân thiện tối đa với người cao tuổi.\n"
        "3. Kênh phân phối (Channels): Kênh kê toa B2B2C từ bác sĩ tại bệnh viện; Ứng dụng web/di động; Zalo Mini App; Kênh mạng xã hội dành cho con cái.\n"
        "4. Quan hệ khách hàng (Customer Relationships): Linh vật Bé Nấm tạo cảm giác thân thiết; Hệ thống báo cáo tiến độ tự động gửi con cái; Hỗ trợ y tế 1-chạm kết nối bác sĩ.\n"
        "5. Dòng doanh thu (Revenue Streams): Thuê bao B2C Pro (120.000 đ/tháng); Gói liên kết Bác sĩ (250.000 đ/tháng chia sẻ 60/40); Thuê bao B2B cho phòng khám (5 - 15 triệu đ/tháng).\n"
        "6. Hoạt động cốt lõi (Key Activities): R&D thuật toán thị giác AI và bộ lọc One-Euro; Huấn luyện dữ liệu y sinh; Phát triển ứng dụng Geriatric UI; Kiểm định lâm sàng.\n"
        "7. Nguồn lực cốt lõi (Key Resources): Bản quyền thuật toán lọc nhiễu rung; 3 bộ dataset chuẩn y sinh; Đội ngũ kỹ sư BMED & AI; Thương hiệu Bé Nấm.\n"
        "8. Đối tác chính (Key Partners): Bệnh viện Chấn thương Chỉnh hình, Khoa PHCN các bệnh viện lớn; Viện dưỡng lão; Hội người cao tuổi; Trường Đại học BMED.\n"
        "9. Cơ cấu chi phí (Cost Structure): 45% R&D và nhân sự kỹ thuật; 30% Marketing & Hoa hồng B2B2C; 15% Kiểm nghiệm lâm sàng & Pháp lý; 10% Hạ tầng vận hành."
    )

    doc.add_heading("3.2. Kiến trúc giải pháp kỹ thuật & Thuật toán 100% On-Device AI", level=2)
    doc.add_paragraph(
        "Khác biệt căn bản của MotionIQ so với các giải pháp thông thường nằm ở kiến trúc xử lý biên (Edge AI / On-Device Processing):\n"
        "• Thị giác máy tính thời gian thực: Tích hợp MediaPipe BlazePose tối ưu bằng WebAssembly, phát hiện 33 điểm mốc giải phẫu (Anatomical Landmarks) "
        "với tốc độ 25 - 30 khung hình/giây (FPS) ngay trên trình duyệt di động mà không cần máy chủ GPU đắt tiền.\n"
        "• Thuật toán lọc rung One-Euro Filter độc quyền: Người cao tuổi thường bị run tay chân (tremor) sinh lý hoặc bệnh lý Parkinson. "
        "Bộ lọc thích ứng One-Euro Filter tự động triệt tiêu rung động tần số cao ở vận tốc thấp nhưng không gây trễ chuyển động ở vận tốc cao, đảm bảo góc đo ổn định tuyệt đối.\n"
        "• Bảo mật dữ liệu y tế (Privacy-by-Design): Luồng video camera từ smartphone được phân tích trực tiếp trong bộ nhớ RAM tạm thời của điện thoại. "
        "Chỉ có các chỉ số góc ROM dạng số học (ví dụ: góc gập gối 110 độ) được lưu trữ để vẽ biểu đồ, loại bỏ 100% nguy cơ rò rỉ hình ảnh riêng tư của người bệnh."
    )

    doc.add_heading("3.3. Chuẩn hóa 4 bài tập lâm sàng theo 3 Dataset Y sinh Quốc tế", level=2)
    doc.add_paragraph(
        "Nhóm kiên quyết loại bỏ các bài tập không phù hợp (như nhón chân calf-raise rủi ro ngã cao) và chuẩn hóa nghiêm ngặt 4 bài tập cốt lõi được bảo chứng bởi 3 bộ dữ liệu y sinh:\n"
        "1. Bài Sit-to-Stand (Ngồi xuống - Đứng lên — Dataset UI-PRMD m05): Đo góc gập gối ($90^\circ - 125^\circ$), kích hoạt cơ tứ đầu đùi và đánh giá chức năng di chuyển độc lập.\n"
        "2. Bài Squat chức năng (Dataset UI-PRMD m01): Kiểm tra trục đầu gối và lưng thẳng, gia cố cơ đáy chậu và khớp háng.\n"
        "3. Bài Shoulder Abduction (Dạng khớp vai — Dataset UI-PRMD m04): Đo góc dạng cánh tay ($0^\circ - 180^\circ$), hỗ trợ bệnh nhân co cứng khớp vai sau tai biến.\n"
        "4. Bài Side Leg Raise (Nâng chân sang bên — Dataset KIMORE): Kích hoạt cơ mông nhỡ (gluteus medius), cơ quan trọng nhất giữ thăng bằng chống té ngã ở người già."
    )

    doc.add_heading("3.4. Kết quả kiểm thử thực nghiệm lâm sàng MVP trên 25 bệnh nhân", level=2)
    t_mvp = doc.add_table(rows=5, cols=3)
    t_mvp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_mvp.autofit = False
    mvp_widths = [Inches(2.5), Inches(1.8), Inches(1.9)]
    
    mvp_data = [
        ("Chỉ số đo lường lâm sàng & kỹ thuật", "Kết quả thực nghiệm", "Tiêu chuẩn đối chứng y tế"),
        ("Độ chính xác đo góc khớp (ROM Accuracy)", "94.6%", "So với thước đo góc cơ học Goniometer y tế"),
        ("Độ trễ phân tích AI (Latency)", "38 ms / frame", "Đảm bảo phản hồi giọng nói tức thì (<50ms)"),
        ("Tỷ lệ hoàn thành buổi tập của người già", "88.0% (22/25 bệnh nhân)", "Vượt xa tỷ lệ tự tập truyền thống (chỉ ~40%)"),
        ("Điểm trải nghiệm hệ thống SUS", "84.5 / 100 điểm", "Xếp hạng Grade A (Mức độ Xuất sắc)")
    ]

    for r_idx, row in enumerate(t_mvp.rows):
        for c_idx, val in enumerate(mvp_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = mvp_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    # ==========================================
    # CHƯƠNG 4: KẾ HOẠCH TÀI CHÍNH, ĐỊNH GIÁ & GỌI VỐN (FINAL REPORT)
    # ==========================================
    doc.add_page_break()
    h_c4 = doc.add_heading("CHƯƠNG 4: KẾ HOẠCH TÀI CHÍNH, ĐỊNH GIÁ & GỌI VỐN (FINAL / THE ASK)", level=1)
    for r in h_c4.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("4.1. Dự toán vốn khởi nghiệp ban đầu (Startup Capital Requirement)", level=2)
    doc.add_paragraph(
        "Tổng chi phí đầu tư ban đầu ước tính là 450.000.000 VNĐ, bao gồm:\n"
        "• Nghiên cứu và hoàn thiện thuật toán AI: 180 triệu VNĐ (40%).\n"
        "• Thử nghiệm lâm sàng có đối chứng tại bệnh viện: 90 triệu VNĐ (20%).\n"
        "• Đăng ký quyền tác giả, nhãn hiệu và chứng nhận phần mềm y tế loại A: 70 triệu VNĐ (15.5%).\n"
        "• Thiết kế nhận diện thương hiệu, Mascot Bé Nấm và Marketing ban đầu: 60 triệu VNĐ (13.3%).\n"
        "• Quỹ dự phòng hoạt động 6 tháng đầu: 50 triệu VNĐ (11.2%)."
    )

    doc.add_heading("4.2. Dự phóng kết quả kinh doanh 3 năm (P&L 2025 - 2027)", level=2)
    t_pl = doc.add_table(rows=9, cols=4)
    t_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_pl.autofit = False
    pl_widths = [Inches(2.5), Inches(1.2), Inches(1.2), Inches(1.3)]
    
    pl_data = [
        ("Chỉ tiêu tài chính (Đơn vị: Triệu VNĐ)", "Năm 1 (2025)", "Năm 2 (2026)", "Năm 3 (2027)"),
        ("Người dùng trả phí thường xuyên (Paid Users)", "650", "3.800", "15.000"),
        ("Doanh thu B2C Subscription", "580", "3.420", "13.500"),
        ("Doanh thu B2B Phòng khám & Viện dưỡng lão", "180", "960", "3.600"),
        ("TỔNG DOANH THU THUẦN (REVENUE)", "760", "4.380", "17.100"),
        ("Giá vốn & Chi phí Cloud (COGS)", "90", "350", "1.100"),
        ("Chi phí Nghiên cứu & Phát triển (R&D)", "380", "950", "2.200"),
        ("Chi phí Tiếp thị & Hoa hồng B2B2C (S&M)", "290", "1.100", "3.800"),
        ("LỢI NHUẬN TRƯỚC THUẾ (EBITDA)", "-180", "+1.500", "+8.800")
    ]

    for r_idx, row in enumerate(t_pl.rows):
        for c_idx, val in enumerate(pl_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = pl_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            elif r_idx in (4, 8):
                run.font.bold = True
                set_cell_background(cell, "F2EAE1" if r_idx == 4 else "E2F5E9")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("4.3. Phân tích điểm hòa vốn (Break-even Analysis)", level=2)
    doc.add_paragraph(
        "Nhờ mô hình 100% On-Device AI xử lý trực tiếp trên thiết bị khách hàng, MotionIQ có chi phí biến đổi trên mỗi người dùng mới (Marginal Cloud Cost) "
        "gần như bằng 0 (chỉ tốn dung lượng lưu trữ chỉ số góc vài kilobyte). Với mức chi phí cố định bình quân tháng trong năm thứ 2 ước tính 180 triệu VNĐ, "
        "dự án đạt ĐIỂM HÒA VỐN vào THÁNG THỨ 14 khi đạt số lượng thuê bao trả phí thường xuyên tối thiểu là 1.650 người dùng."
    )

    doc.add_heading("4.4. Định giá doanh nghiệp & Kế hoạch gọi vốn (The Ask)", level=2)
    doc.add_paragraph(
        "• Phương pháp định giá: Áp dụng phương pháp Berkus kết hợp Scorecard Valuation cho Startup MedTech giai đoạn thử nghiệm lâm sàng thành công:\n"
        "  - Ý tưởng vững chắc & Nhu cầu thị trường cấp thiết: +1.2 tỷ VNĐ.\n"
        "  - Nguyên mẫu Prototype MVP hoạt động thực tế với 4 bài tập chuẩn: +1.5 tỷ VNĐ.\n"
        "  - Đội ngũ sáng lập có năng lực chuyên môn Kỹ thuật Y sinh BMED: +1.2 tỷ VNĐ.\n"
        "  - Quan hệ đối tác lâm sàng với các Bác sĩ chuyên khoa: +1.5 tỷ VNĐ.\n"
        "  ➔ Định giá trước đầu tư (Pre-money Valuation): 5.400.000.000 VNĐ (~216.000 USD).\n"
        "  ➔ Định giá sau đầu tư (Post-money Valuation): 6.000.000.000 VNĐ (~240.000 USD).\n\n"
        "• Kế hoạch gọi vốn (The Ask): Kêu gọi 600.000.000 VNĐ đổi lấy 10% Cổ phần (Equity).\n"
        "• Kế hoạch phân bổ và sử dụng vốn (Capital Utilization):\n"
        "  1. 45% (270 triệu VNĐ): Nâng cấp R&D thuật toán, hoàn thiện kho 12 bài tập phục hồi chức năng mở rộng.\n"
        "  2. 30% (180 triệu VNĐ): Tiếp thị B2B2C, tài trợ thử nghiệm và ký hợp đồng hợp tác với 20 phòng khám PHCN tại TP.HCM.\n"
        "  3. 15% (90 triệu VNĐ): Hoàn tất thủ tục pháp lý, kiểm chuẩn và đăng ký lưu hành phần mềm y tế Loại A.\n"
        "  4. 10% (60 triệu VNĐ): Quỹ dự phòng hoạt động và chi phí pháp chế thường niên."
    )

    # ==========================================
    # CHƯƠNG 5: QUẢN TRỊ RỦI RO & LỘ TRÌNH PHÁT TRIỂN (ROADMAP)
    # ==========================================
    doc.add_page_break()
    h_c5 = doc.add_heading("CHƯƠNG 5: QUẢN TRỊ RỦI RO & LỘ TRÌNH PHÁT TRIỂN", level=1)
    for r in h_c5.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("5.1. Nhận diện rủi ro và Biện pháp giảm thiểu", level=2)
    doc.add_paragraph(
        "• Rủi ro 1: Người già té ngã trong quá trình tập luyện tại nhà.\n"
        "  ➔ Biện pháp: Trước mỗi bài tập, hệ thống bắt buộc kiểm tra điều kiện an toàn (ghế tựa chắc chắn, không gian bằng phẳng, có tay vịn); "
        "tích hợp nút gọi khẩn cấp 1-chạm tới số điện thoại 115 và người thân ngay trên màn hình chính.\n\n"
        "• Rủi ro 2: Chậm trễ trong quá trình xin cấp phép phần mềm y tế.\n"
        "  ➔ Biện pháp: Trong giai đoạn 1, MotionIQ được định vị pháp lý là 'Ứng dụng hỗ trợ tập luyện vận động và nâng cao sức khỏe' (Wellness App); "
        "song song đó chuẩn bị hồ sơ thử nghiệm lâm sàng có đối chứng để chuyển đổi thành Trang thiết bị Y tế Loại A vào năm thứ 2.\n\n"
        "• Rủi ro 3: Người bệnh thiếu kiên trì và bỏ cuộc sau vài tuần.\n"
        "  ➔ Biện pháp: Cơ chế gamification nhẹ nhàng thông qua chuỗi ngày tập luyện (Streak), lời khen và biểu cảm vui mừng của Bé Nấm, cùng tin nhắn "
        "chúc mừng tự động gửi về điện thoại con cái để người thân gọi điện động viên cha mẹ."
    )

    doc.add_heading("5.2. Lộ trình phát triển 5 năm (Roadmap 2025 - 2029)", level=2)
    doc.add_paragraph(
        "• Năm 2025: Hoàn thiện ứng dụng di động, triển khai thử nghiệm trên 3.000 người dùng tại TP.HCM, kết nối 10 phòng khám đối tác, đạt mốc 650 khách hàng trả phí.\n"
        "• Năm 2026: Đạt chứng nhận phần mềm y tế Loại A, mở rộng mạng lưới 50 phòng khám tại Hà Nội và Đà Nẵng, đạt điểm hòa vốn tháng thứ 14, chạm mốc 3.800 khách hàng trả phí.\n"
        "• Năm 2027: Tích hợp mô hình AI phân tích nguy cơ té ngã dự đoán trước (Fall Risk Prediction), hợp tác với các công ty bảo hiểm nhân thọ và sức khỏe tư nhân (Bảo Việt, Prudential), đạt 15.000 người dùng trả phí.\n"
        "• Năm 2028 - 2029: Mở rộng ra các thị trường có cơ cấu dân số già tương đồng tại Đông Nam Á (Thái Lan, Singapore), hướng tới vòng gọi vốn Series A (2-3 triệu USD)."
    )

    # ==========================================
    # KẾT LUẬN & PHỤ LỤC
    # ==========================================
    doc.add_heading("KẾT LUẬN", level=1)
    doc.add_paragraph(
        "Dự án MotionIQ đại diện cho tinh thần đổi mới sáng tạo phụng sự cộng đồng của sinh viên ngành Kỹ thuật Y sinh (BMED). Bằng việc giải quyết triệt để "
        "3 bài toán hóc búa nhất của ngành phục hồi chức năng: Chi phí cao — Quá tải viện — Thiếu giám sát tại nhà, MotionIQ không chỉ sở hữu tiềm năng "
        "thương mại bền vững với quy mô thị trường hàng ngàn tỷ đồng mà trên hết, mang lại giá trị nhân văn sâu sắc: Giúp hàng triệu người cao tuổi Việt Nam "
        "tìm lại niềm vui trong từng bước đi vững chãi và an tâm sống vui khỏe bên con cháu."
    )

    # Save to disk
    out_dir = r"c:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq"
    out_path = os.path.join(out_dir, "BaoCao_ToanDien_MotionIQ_EXE101.docx")
    doc.save(out_path)
    print(f"Successfully generated DOCX report at: {out_path}")

    # Also save to public for browser download
    public_path = os.path.join(out_dir, "public", "BaoCao_ToanDien_MotionIQ_EXE101.docx")
    doc.save(public_path)
    print(f"Successfully copied to public at: {public_path}")

    # Also save to artifact directory
    artifact_path = r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a\BaoCao_ToanDien_MotionIQ_EXE101.docx"
    doc.save(artifact_path)
    print(f"Successfully saved to artifact directory at: {artifact_path}")

if __name__ == "__main__":
    main()
