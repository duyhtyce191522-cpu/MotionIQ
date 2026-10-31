# -*- coding: utf-8 -*-
"""
Script to generate the refined Academic Final Report Book for MotionIQ (EXE101)
Course Instructor: Thầy Trần Ngọc Sơn
Student Leader / CEO: Huỳnh Thị Yến Duy (MSSV: CE191522)
Location & Date: TP. Cần Thơ, Tháng 11 NĂM 2026

UPDATED GUIDELINES APPLIED:
1. Rà soát ngôn từ nghiêm ngặt:
   - Loại bỏ hoàn toàn các từ: 'y tế', 'y sinh', 'bệnh án', 'kiểm định', 'tuyệt đối', 'Hội đồng cố vấn/Bác sĩ cố vấn'.
   - Định vị trung thực: MotionIQ là "nền tảng công nghệ hỗ trợ theo dõi tập luyện vận động tại nhà qua camera smartphone".
   - Tuyên bố an toàn: Công cụ hỗ trợ tập luyện, không thay thế chuyên viên hay bác sĩ.
2. Mô hình doanh thu & Định giá:
   - Định giá dựa trên Giá trị Khách hàng & Cạnh tranh (Customer Value & Competition-based Pricing).
   - Nghiên cứu kỹ đối thủ cạnh tranh (Tự tập YouTube, Huấn luyện viên tại nhà, Phòng tập, App ngoại).
   - Gói Early Access: 49.000 VNĐ/tháng; Gói Tiêu chuẩn: 79.000 VNĐ/tháng.
3. Tích hợp 100% Kế hoạch Truyền thông 04 tháng & Ngân sách 10.000.000 VNĐ:
   - Mục tiêu, thông điệp, 4 kênh (TikTok, Facebook, Zalo, Trực tiếp), ngân sách chi tiết và bảng KPIs.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout_box(doc, text, title="LƯU Ý / ĐIỂM NHẤN"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.2)
    set_cell_background(cell, "FEF7EE")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="B2422D"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)
    
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
    run_text.font.size = Pt(10)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(60, 30, 20)

def main():
    doc = Document()

    # Standard Page Margins (Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)     # ~2.0 cm
        section.bottom_margin = Inches(0.8)  # ~2.0 cm
        section.left_margin = Inches(1.18)   # ~3.0 cm
        section.right_margin = Inches(0.8)   # ~2.0 cm

    # Base Typography
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # 1. TRANG BÌA CHÍNH (COVER PAGE)
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC FPT CẦN THƠ\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(90, 90, 90)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("———————————————***———————————————\n\n")
    r_line.font.bold = True
    r_line.font.color.rgb = RGBColor(178, 66, 45)

    p_title_sub = doc.add_paragraph()
    p_title_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_title_sub.add_run("BÁO CÁO TỔNG KẾT DỰ ÁN KHỞI NGHIỆP (FINAL REPORT)\nHỌC PHẦN: EXE101 — TRẢI NGHIỆM KHỞI NGHIỆP\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(178, 66, 45)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(14)
    r_title = p_title.add_run("MOTIONIQ — NỀN TẢNG TRỢ LÝ AI HỖ TRỢ THEO DÕI TẬP LUYỆN VẬN ĐỘNG TẠI NHÀ CHO NGƯỜI CAO TUỔI\n(100% ON-DEVICE AI)")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(140, 47, 30)

    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(32)
    r_tag = p_tag.add_run('"MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn."\n(Hợp nhất: Checkpoint 1 • Checkpoint 2 • Checkpoint 3 • Kế hoạch truyền thông & phát triển doanh thu)')
    r_tag.font.italic = True
    r_tag.font.size = Pt(10.5)
    r_tag.font.color.rgb = RGBColor(100, 100, 100)

    # Info table on cover
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    col_widths = [Inches(2.4), Inches(3.8)]
    
    info_data = [
        ("Giảng viên hướng dẫn:", "Thầy Trần Ngọc Sơn"),
        ("Tên nhóm sinh viên:", "MOTIONIQ — Nhóm K19"),
        ("Trưởng nhóm (CEO):", "Huỳnh Thị Yến Duy — MSSV: CE191522"),
        ("Thành viên nhóm:", "Nguyễn Hải Hà (CTO) • Nguyễn Nhã Quân (CPO)\nMã Phú Tín • Đặng Vĩnh Phúc • Hồ Tuyết Nghi (CMO)"),
        ("Website Demo MVP:", "https://motion-iq-five.vercel.app"),
        ("Thực nghiệm & Khảo sát:", "50 phiếu khảo sát thực tế • 5 buổi thử nghiệm nguyên mẫu")
    ]

    for idx, (lbl, val) in enumerate(info_data):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width, cell_val.width = col_widths[0], col_widths[1]
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        r0.font.color.rgb = RGBColor(50, 50, 50)
        
        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(10.5)
        if "http" in val:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(178, 66, 45)

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(36)
    r_bot = p_bottom.add_run("TP. CẦN THƠ, THÁNG 11 NĂM 2026")
    r_bot.font.bold = True
    r_bot.font.size = Pt(12)
    r_bot.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ==========================================
    # LỜI CẢM ƠN
    # ==========================================
    h_camon = doc.add_heading("LỜI CẢM ƠN", level=1)
    h_camon.paragraph_format.space_after = Pt(10)
    for r in h_camon.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    p_camon = doc.add_paragraph(
        "Nhóm thực hiện dự án MotionIQ xin gửi lời tri ân sâu sắc và lòng biết ơn chân thành nhất đến Thầy Trần Ngọc Sơn, "
        "người đã tận tâm truyền đạt kiến thức khởi nghiệp đổi mới sáng tạo, phương pháp tư duy mô hình kinh doanh và kiên nhẫn định hướng, "
        "góp ý chuyên môn quý báu qua từng cột mốc Checkpoint 1, Checkpoint 2 và Checkpoint 3 của học phần EXE101 (Trải nghiệm khởi nghiệp).\n\n"
        "Nhóm cũng xin chân thành cảm ơn các cô bác lớn tuổi và người thân đã nhiệt tình tham gia 50 phiếu khảo sát thực địa cũng như 5 buổi thử nghiệm "
        "trực tiếp nguyên mẫu ứng dụng. Những đóng góp thực tế từ người dùng chính là kim chỉ nam giúp nhóm hoàn thiện sản phẩm MotionIQ hữu ích và nhân văn nhất."
    )
    p_camon.paragraph_format.line_spacing = 1.3
    p_camon.paragraph_format.space_after = Pt(14)

    # Executive Summary
    h_tt = doc.add_heading("TÓM TẮT DỰ ÁN (EXECUTIVE SUMMARY)", level=1)
    for r in h_tt.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    p_tt = doc.add_paragraph(
        "MotionIQ là giải pháp công nghệ ứng dụng Trí tuệ Nhân tạo thị giác máy tính chạy trực tiếp trên thiết bị di động (100% On-Device AI), "
        "hỗ trợ người cao tuổi theo dõi quá trình tập luyện vận động và rèn luyện thăng bằng tại nhà thông qua camera smartphone hoặc laptop "
        "mà không cần đầu tư thêm các thiết bị cảm biến phần cứng tốn kém.\n\n"
        "Bằng cách kết hợp linh vật trợ lý ảo 'Bé Nấm' với lời nhắc nhở đếm nhịp bằng tiếng Việt, mô hình nhận diện tư thế dựa trên các bộ dữ liệu "
        "chuyển động mẫu đã công bố (UI-PRMD, KIMORE, EHE) và bộ lọc khử nhiễu One-Euro Filter, MotionIQ giúp người lớn tuổi duy trì thói quen vận động "
        "đúng tư thế, đếm số lần tập và đưa ra phản hồi cơ bản. Kết quả khảo sát thực tế trên 50 đối tượng cho thấy hơn 68% con cái gặp khó khăn khi trực tiếp "
        "quan sát cha mẹ tập luyện, và 82.4% sẵn sàng cho người thân dùng thử ứng dụng. Thử nghiệm thực tế qua 5 buổi đạt chỉ số đo góc vận động (ROM) đạt 94.6% "
        "so với góc đo đối chiếu và điểm khả dụng hệ thống SUS đạt 84.5/100 (Mức xuất sắc).\n\n"
        "Về chiến lược kinh doanh, nhóm áp dụng phương pháp định giá dựa trên giá trị khách hàng và so sánh đối thủ cạnh tranh với gói thử nghiệm Early Access "
        "49.000 VNĐ/tháng, kết hợp kế hoạch truyền thông 04 tháng tinh gọn với ngân sách sinh viên 10.000.000 VNĐ nhằm đạt mốc 15–20 khách hàng trả phí đầu tiên."
    )
    p_tt.paragraph_format.line_spacing = 1.3
    p_tt.paragraph_format.space_after = Pt(16)

    # Table of Acronyms
    h_acronym = doc.add_heading("DANH MỤC TỪ VIẾT TẮT", level=2)
    t_acro = doc.add_table(rows=7, cols=3)
    t_acro.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_acro.autofit = False
    
    acro_widths = [Inches(1.5), Inches(2.3), Inches(2.4)]
    acro_data = [
        ("Từ viết tắt", "Thuật ngữ Tiếng Anh", "Ý nghĩa Tiếng Việt"),
        ("AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"),
        ("BMC", "Business Model Canvas", "Khung Mô hình Kinh doanh 9 Khối"),
        ("ROM", "Range of Motion", "Biên độ góc vận động của khớp"),
        ("TAM/SAM/SOM", "Total / Serviceable / Obtainable Market", "Quy mô Thị trường Tổng / Phục vụ / Khả thi"),
        ("SUS", "System Usability Scale", "Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế)"),
        ("On-Device AI", "On-Device Artificial Intelligence", "Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị")
    ]

    for row_idx, row in enumerate(t_acro.rows):
        for col_idx, text in enumerate(acro_data[row_idx]):
            cell = row.cells[col_idx]
            cell.width = acro_widths[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(9.5)
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
        "trở lên đã vượt 13.5 triệu người (chiếm 13.5% dân số). Cùng với quá trình lão hóa tự nhiên, người cao tuổi thường gặp các vấn đề về suy giảm sức mạnh "
        "cơ bắp, thoái hóa khớp gối, cột sống và giảm khả năng giữ thăng bằng, dẫn đến nguy cơ té ngã và hạn chế sinh hoạt hàng ngày.\n\n"
        "Việc duy trì thói quen tập luyện vận động nhẹ nhàng tại nhà đóng vai trò quan trọng trong việc cải thiện sự dẻo dai và nâng cao thể trạng. Tuy nhiên, "
        "đa số người lớn tuổi tự tập theo thói quen mà không biết mình làm đúng hay sai tư thế; trong khi con cái bận rộn đi làm không thể thường xuyên quan sát, "
        "nhắc nhở. Xuất phát từ thực tế chăm sóc người thân trong gia đình, nhóm MedTech Pioneers đã phát triển dự án MotionIQ — ứng dụng công nghệ AI thị giác "
        "trên điện thoại để trở thành người bạn đồng hành hỗ trợ theo dõi vận động, đếm nhịp và đưa ra phản hồi cơ bản cho người cao tuổi ngay tại nhà."
    )

    doc.add_heading("1.2. Sứ mệnh, Tầm nhìn và Hệ giá trị cốt lõi", level=2)
    doc.add_paragraph(
        "• Sứ mệnh (Mission): 'Bình dân hóa dịch vụ hỗ trợ tập luyện vận động chất lượng đến từng hộ gia đình Việt Nam' — mang lại khả năng vận động tự chủ, "
        "giảm thiểu nguy cơ té ngã cho người già và giúp con cái yên tâm hơn khi đi làm xa.\n"
        "• Tầm nhìn (Vision): Trở thành nền tảng số hỗ trợ theo dõi vận động cá nhân phổ biến tại Việt Nam vào năm 2027.\n"
        "• Hệ giá trị cốt lõi (Core Values):\n"
        "  1. An toàn & Dựa trên dữ liệu (Evidence-based): Mọi bài tập đều dựa trên các bài vận động chức năng chuẩn hóa từ các bộ dữ liệu chuyển động công khai đã được nghiên cứu và sử dụng trước đó.\n"
        "  2. Tôn trọng quyền riêng tư (Privacy by Design): Xử lý AI 100% cục bộ trên máy người dùng, kiên quyết nói KHÔNG với việc lưu trữ hình ảnh cá nhân lên máy chủ đám mây.\n"
        "  3. Đồng cảm với tuổi già (Geriatric Empathy): Giao diện chữ lớn, tương tác một chạm, khích lệ người già bằng sự ấm áp và kiên nhẫn của linh vật Bé Nấm."
    )

    doc.add_heading("1.3. Hồ sơ năng lực đội ngũ sáng lập (Founding Team & RACI)", level=2)
    doc.add_paragraph(
        "Đội ngũ sáng lập MotionIQ (MOTIONIQ — Nhóm K19) là sự kết hợp chặt chẽ giữa các chuyên ngành Công nghệ Thông tin (An toàn thông tin), Thiết kế Đồ họa / UI-UX, "
        "Truyền thông đa phương tiện, Ngôn ngữ và Quản trị Dịch vụ tạo nên lợi thế triển khai thực tế:"
    )

    t_team = doc.add_table(rows=7, cols=4)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_team.autofit = False
    team_widths = [Inches(1.6), Inches(1.1), Inches(1.6), Inches(1.9)]
    
    team_data = [
        ("Họ và Tên", "Vai trò", "Chuyên ngành & Thế mạnh", "Trách nhiệm chính (RACI)"),
        ("Huỳnh Thị Yến Duy", "CEO (Trưởng nhóm)", "An toàn thông tin", "Chịu trách nhiệm toàn diện kĩ thuật dựng web/app. Phát triển MediaPipe Pose và quản lí dự án"),
        ("Nguyễn Hải Hà", "CTO", "An toàn thông tin", "Chịu trách nhiệm kỹ thuật tìm kiếm áp dụng các bộ dataset vào dự án"),
        ("Nguyễn Nhã Quân", "CPO", "Thiết kế Sản phẩm / UI-UX", "Nghiên cứu trải nghiệm người cao tuổi (Responsible UX), Thiết kế UI & Luồng người dùng"),
        ("Mã Phú Tín", "Thành viên", "Truyền thông đa phương tiện", "Nghiên cứu khách hàng và tiến hành lên kế hoạch truyền thông"),
        ("Đặng Vĩnh Phúc", "Thành viên", "Ngôn ngữ Anh - Trung", "Chuyển đổi ngôn ngữ và hợp tác phát triển truyền thông, khảo sát khách hàng"),
        ("Hồ Tuyết Nghi", "CMO", "Quản trị Dịch vụ", "Khảo sát người dùng, kế hoạch về kinh tế và nghiên cứu khách hàng")
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

    add_callout_box(
        doc,
        "Sự bổ trợ giữa chuyên môn Kỹ thuật AI giúp MotionIQ tương tác trực tiếp với khách hàng, cùng với đó là sử dụng MotionIQ trên thiết bị "
        "di động laptop mà không cần tốn chi phí mua các thiết bị lớn tốn nhiều chi phí để tập tại nhà.\n\n"
        "LƯU Ý QUAN TRỌNG: MotionIQ chỉ là công cụ hỗ trợ tập luyện vận động tại nhà, không thay thế chuyên viên hay thay thế bác sĩ.",
        "ĐIỂM MẠNH ĐỘI NGŨ & NGUYÊN TẮC GIỚI HẠN AN TOÀN"
    )

    # ==========================================
    # CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (CHECKPOINT 2)
    # ==========================================
    doc.add_page_break()
    h_c2 = doc.add_heading("CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (CHECKPOINT 2)", level=1)
    for r in h_c2.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("2.1. Phương pháp luận và Quy mô khảo sát thực tế (N = 50)", level=2)
    doc.add_paragraph(
        "Để xác thực giả thuyết bài toán và nhu cầu thực tế của thị trường trong giai đoạn Checkpoint 2, nhóm đã tiến hành khảo sát thực địa 50 đối tượng "
        "thông qua biểu mẫu câu hỏi trực tuyến (dữ liệu lưu trữ công khai tại Google Sheets: "
        "https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM):\n"
        "• Đối tượng trả lời khảo sát: 82.4% thuộc độ tuổi 18 - 23 tuổi và 17.6% từ 23 - 30 tuổi (đại diện cho đối tượng con cháu quan tâm chăm sóc người thân).\n"
        "• Kinh nghiệm hỗ trợ người thân: 64.7% cho biết trong 1 năm gần đây có chăm sóc hoặc hỗ trợ người thân trong sinh hoạt hoặc vận động.\n"
        "• Độ tuổi của người thân cần hỗ trợ: 31.4% từ 60–69 tuổi; 23.5% từ 70–79 tuổi; 9.8% từ 80 tuổi trở lên (tổng cộng 64.7% người thân từ 60 tuổi trở lên) "
        "và 23.5% từ 50–59 tuổi."
    )

    doc.add_heading("2.2. Kết quả phân tích dữ liệu khảo sát thực tế từ Google Sheets (N = 50)", level=2)
    t_survey = doc.add_table(rows=8, cols=3)
    t_survey.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_survey.autofit = False
    surv_widths = [Inches(3.2), Inches(1.2), Inches(1.8)]
    
    surv_data = [
        ("Nội dung khảo sát thực tế (Dữ liệu thực N = 50)", "Tỷ lệ thực tế", "Hàm ý phát triển MotionIQ"),
        ("Con cái không thể thường xuyên quan sát, sửa động tác cho người thân", "68.6%", "Người già thường phải tập một mình, rất cần AI theo dõi."),
        ("Người thân tập luyện hàng ngày hoặc 3-5 lần/tuần", "51.0%", "Nhu cầu tập luyện là liên tục, cần công cụ thường trực tại nhà."),
        ("Khó khăn lớn nhất: Không biết tập đúng/sai, không có phản hồi và cảnh báo", "82.4%", "AI phải có chức năng đếm nhịp và sửa lỗi tư thế tức thì."),
        ("3 yếu tố quan trọng nhất: Dễ sử dụng, Báo đúng/sai, Hướng dẫn sửa động tác", "88.2%", "Bắt buộc thiết kế Geriatric UI: Chữ to, nút to, 1-chạm."),
        ("Mức độ phù hợp của MotionIQ với nhu cầu (Đánh giá mức 4 - 5 sao)", "66.7%", "Mô hình giải pháp giải quyết đúng nhu cầu của đa số gia đình."),
        ("Sẵn sàng cho người thân dùng thử MotionIQ (Đánh giá mức 4 - 5 sao)", "82.4%", "Tỷ lệ chấp nhận dùng thử và chuyển đổi tiềm năng rất cao."),
        ("Chấp nhận chi trả mức phí 50.000 – 149.000 VNĐ/tháng", "64.7%", "Mức giá thuê bao tháng 49.000 – 79.000 VNĐ là hoàn toàn tối ưu.")
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

    doc.add_paragraph(
        "\nKhi khảo sát về điều lo ngại nhất khi sử dụng camera và AI (Câu 14 trong bảng khảo sát):\n"
        "1. Lo ngại về quyền riêng tư và hình ảnh (được 45% người tham gia đề cập).\n"
        "2. Người lớn tuổi khó thao tác thiết bị công nghệ (50%).\n"
        "3. AI có thể nhận diện không chính xác do chuyển động người già bị chậm hoặc run tay chân (40%).\n\n"
        "Chính kết quả khảo sát thực tế này là cơ sở vững chắc để nhóm thiết kế kiến trúc kỹ thuật của MotionIQ:\n"
        "• Xóa bỏ lo ngại riêng tư bằng kiến trúc 100% On-Device AI: Video chỉ xử lý cục bộ trên RAM, không truyền hình ảnh lên máy chủ.\n"
        "• Xóa bỏ lo ngại khó dùng bằng Geriatric UI: Phông chữ to >= 18px, nút bấm lớn >= 56px, trợ lý Bé Nấm nói tiếng Việt rõ ràng.\n"
        "• Cải thiện độ chính xác bằng Bộ lọc One-Euro Filter: Triệt tiêu rung tay chân sinh lý khi theo dõi chuyển động."
    )

    doc.add_heading("2.3. Chân dung khách hàng mục tiêu & Bản đồ thấu cảm (Empathy Map)", level=2)
    doc.add_paragraph(
        "Mô hình khách hàng của MotionIQ có đặc tính kép (Dual-Customer Profile): Người sử dụng trực tiếp (Người cao tuổi) và Người ra quyết định chi trả (Con cái):\n"
        "• Persona 1 — Người dùng trực tiếp: Bác Nguyễn Văn An, 68 tuổi, hưu trí tại TP. Cần Thơ. Bác có nhu cầu rèn luyện cơ chân và khớp gối hàng ngày để đi lại "
        "vững vàng hơn. Bác mắt kém, sợ làm phiền con cái, cảm thấy chán nản khi phải tập các động tác lặp lại một mình mà không biết đúng hay sai.\n"
        "• Persona 2 — Người chi trả: Chị Thu Hằng, 36 tuổi, nhân viên văn phòng. Chị quan tâm đến sức khỏe cha mẹ nhưng bận rộn công việc, luôn bất an không biết "
        "ở nhà ba tập luyện ra sao. Chị sẵn sàng bỏ ra một khoản chi phí nhỏ hàng tháng (dưới 100.000 VNĐ) để có ứng dụng hỗ trợ ba tập luyện đều đặn và an tâm hơn."
    )

    doc.add_heading("2.4. Phân tích đối thủ cạnh tranh & Lợi thế định vị (Competitive Analysis)", level=2)
    t_comp = doc.add_table(rows=5, cols=4)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp.autofit = False
    comp_widths = [Inches(1.6), Inches(1.5), Inches(1.5), Inches(1.6)]
    
    comp_data = [
        ("Giải pháp cạnh tranh", "Ưu điểm", "Hạn chế thực tế", "Lợi thế định vị của MotionIQ"),
        ("Tự tập theo YouTube / Tivi", "Hoàn toàn miễn phí, phong phú", "Không có tương tác, không sửa sai tư thế, dễ tập sai", "AI nhận diện tư thế, đếm nhịp và phản hồi âm thanh tức thì"),
        ("Thuê huấn luyện viên tại nhà", "Theo sát 1:1, động viên tốt", "Chi phí rất cao (200k-400k/buổi, 2-4tr/tháng), khó duy trì", "Chi phí rất rẻ (49k-79k/tháng), chủ động tập mọi lúc"),
        ("CLB Thể dục dưỡng sinh", "Có cộng đồng giao lưu vui vẻ", "Người già yếu chân tay khó tự đi lại, phụ thuộc thời tiết", "Tập an toàn ngay tại phòng khách gia đình"),
        ("App thể dục quốc tế (Freeletics...)", "Giao diện hiện đại, tính năng nhiều", "Tiếng Anh, bài tập nặng cho thanh niên, phí đắt (>150k/tháng)", "Bản địa hóa 100% tiếng Việt, tối ưu động tác nhẹ nhàng cho người già")
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
    # CHƯƠNG 3: MÔ HÌNH KINH DOANH & PHÁT TRIỂN NGUYÊN MẪU MVP (CHECKPOINT 3)
    # ==========================================
    doc.add_page_break()
    h_c3 = doc.add_heading("CHƯƠNG 3: MÔ HÌNH KINH DOANH & NGUYÊN MẪU MVP (CHECKPOINT 3)", level=1)
    for r in h_c3.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("3.1. Khung Mô hình Kinh doanh 9 Khối (Business Model Canvas)", level=2)
    doc.add_paragraph(
        "Mô hình kinh doanh của MotionIQ được tối ưu hóa theo 9 khối chuẩn Osterwalder, phù hợp với năng lực triển khai thực tế của dự án sinh viên:\n"
        "1. Khách hàng mục tiêu (Customer Segments): Con cái 25–40 tuổi quan tâm đến cha mẹ; Người cao tuổi có nhu cầu vận động tại nhà.\n"
        "2. Tuyên ngôn giá trị (Value Propositions): Hỗ trợ tập luyện vận động dễ dàng tại nhà; Chi phí hợp lý (49.000 – 79.000 VNĐ/tháng); Bảo mật hình ảnh với On-Device AI; Giao diện thân thiện tối đa với người già.\n"
        "3. Kênh phân phối (Channels): Mạng xã hội (TikTok, Facebook Fanpage); Zalo; Giới thiệu trực tiếp qua các câu lạc bộ người cao tuổi địa phương.\n"
        "4. Quan hệ khách hàng (Customer Relationships): Linh vật Bé Nấm tạo cảm giác thân thiết; Hệ thống nhắc nhở tập luyện đều đặn; Hỗ trợ kỹ thuật qua Zalo.\n"
        "5. Dòng doanh thu (Revenue Streams): Mô hình Freemium (bài tập cơ bản miễn phí) + Thuê bao gói Early Access (49.000 đ/tháng) và gói Tiêu chuẩn (79.000 đ/tháng).\n"
        "6. Hoạt động cốt lõi (Key Activities): Nâng cấp thuật toán nhận diện tư thế; Thiết kế trải nghiệm Geriatric UI; Sản xuất nội dung truyền thông mạng xã hội; Hỗ trợ khách hàng dùng thử.\n"
        "7. Nguồn lực cốt lõi (Key Resources): Mã nguồn ứng dụng web/mobile; Thuật toán lọc nhiễu One-Euro Filter; Đội ngũ sinh viên đa ngành; Bộ nhận diện Bé Nấm.\n"
        "8. Đối tác chính (Key Partners): Câu lạc bộ hưu trí, hội người cao tuổi địa phương; Giảng viên hướng dẫn môn học; Các cộng đồng chăm sóc gia đình trên mạng xã hội.\n"
        "9. Cơ cấu chi phí (Cost Structure): Chi phí máy chủ lưu trữ nhẹ; Chi phí quảng cáo Facebook/TikTok có chọn lọc; Chi phí in ấn tài liệu QR Code giới thiệu."
    )

    doc.add_heading("3.2. Kiến trúc giải pháp kỹ thuật & Thuật toán 100% On-Device AI", level=2)
    doc.add_paragraph(
        "• Xử lý thị giác thời gian thực trên thiết bị: Ứng dụng tích hợp MediaPipe BlazePose tối ưu bằng WebAssembly, phát hiện 33 điểm mốc chuyển động cơ thể "
        "với tốc độ 25 - 30 khung hình/giây (FPS) ngay trên trình duyệt di động hoặc laptop mà không cần máy chủ GPU đắt tiền.\n"
        "• Bộ lọc khử rung One-Euro Filter: Người cao tuổi thường có độ run tay chân nhất định khi vận động chậm. Thuật toán One-Euro Filter tự động thích ứng "
        "để khử rung ở tốc độ thấp nhưng không gây trễ ở tốc độ cao, giúp các chỉ số góc khớp hiển thị mượt mà, chính xác.\n"
        "• Bảo vệ quyền riêng tư người dùng: Mọi khung hình từ camera điện thoại chỉ được xử lý tạm thời trên bộ nhớ RAM của thiết bị và lập tức hủy bỏ sau khi trích xuất góc. "
        "Không có bất kỳ hình ảnh riêng tư nào được lưu trữ hoặc tải lên máy chủ."
    )

    doc.add_heading("3.3. 4 Bài tập vận động chức năng chuẩn hóa", level=2)
    doc.add_paragraph(
        "Dựa trên các bài tập chuyển động chức năng phổ biến trong các bộ dữ liệu công khai (UI-PRMD và KIMORE), MotionIQ tích hợp 4 bài tập cơ bản, an toàn cho người già:\n"
        "1. Bài Sit-to-Stand (Ngồi xuống - Đứng lên — UI-PRMD m05): Đo góc gập gối (90° - 125°), hỗ trợ cơ đùi và khả năng đứng lên độc lập.\n"
        "2. Bài Squat chức năng (UI-PRMD m01): Kiểm tra trục đầu gối và giữ lưng thẳng, tăng cường sức mạnh cơ chi dưới.\n"
        "3. Bài Shoulder Abduction (Dạng khớp vai — UI-PRMD m04): Đo góc dạng cánh tay (0° - 180°), giúp dẻo dai khớp vai và vùng tay trên.\n"
        "4. Bài Side Leg Raise (Nâng chân sang bên — KIMORE): Hỗ trợ nhóm cơ giữ thăng bằng chống chới với khi đi lại."
    )

    doc.add_heading("3.4. Kết quả 5 buổi thử nghiệm nguyên mẫu MVP thực tế", level=2)
    t_mvp = doc.add_table(rows=4, cols=3)
    t_mvp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_mvp.autofit = False
    mvp_widths = [Inches(2.5), Inches(1.8), Inches(1.9)]
    
    mvp_data = [
        ("Chỉ số đo lường thực nghiệm", "Kết quả thực tế", "Ghi chú đánh giá"),
        ("Độ chính xác đo góc vận động (ROM)", "94.6%", "So sánh với góc đo đối chiếu chuẩn"),
        ("Độ trễ phản hồi thuật toán (Latency)", "38 ms / frame", "Đạt chuẩn thời gian thực, âm thanh đếm nhịp không bị chậm"),
        ("Điểm đánh giá khả dụng hệ thống SUS", "84.5 / 100 điểm", "Người lớn tuổi thao tác thuận tiện, hài lòng với giao diện")
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
    # CHƯƠNG 4: KẾ HOẠCH TRUYỀN THÔNG & PHÁT TRIỂN DOANH THU
    # ==========================================
    doc.add_page_break()
    h_c4 = doc.add_heading("CHƯƠNG 4: KẾ HOẠCH TRUYỀN THÔNG & PHÁT TRIỂN DOANH THU", level=1)
    for r in h_c4.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("4.1. Mục tiêu truyền thông trong 04 tháng", level=2)
    doc.add_paragraph(
        "Trong 04 tháng triển khai, nhóm tập trung xây dựng nhận diện thương hiệu MotionIQ, tiếp cận khách hàng tiềm năng, thúc đẩy trải nghiệm sản phẩm "
        "và chuyển đổi người dùng thành khách hàng trả phí. Do MotionIQ là dự án sinh viên, nhóm ưu tiên các hoạt động truyền thông trực tuyến, tận dụng "
        "nguồn lực sẵn có và triển khai quảng cáo có chọn lọc nhằm tối ưu ngân sách.\n\n"
        "Các mục tiêu cụ thể:\n"
        "• Xây dựng hình ảnh thương hiệu MotionIQ trên các nền tảng mạng xã hội.\n"
        "• Tiếp cận nhóm khách hàng có nhu cầu hỗ trợ cha mẹ, người thân tập luyện tại nhà.\n"
        "• Thu hút khách hàng tham gia trải nghiệm và đóng góp ý kiến hoàn thiện sản phẩm.\n"
        "• Hình thành nhóm khách hàng trả phí đầu tiên và tạo doanh thu từ dịch vụ."
    )

    doc.add_heading("4.2. Khách hàng mục tiêu & Thông điệp truyền thông", level=2)
    doc.add_paragraph(
        "• Khách hàng mục tiêu chính: Con/cháu trong độ tuổi 25–40, có khả năng sử dụng smartphone và quan tâm đến việc hỗ trợ, theo dõi quá trình tập luyện của cha mẹ tại nhà.\n"
        "• Người sử dụng trực tiếp: Người cao tuổi có nhu cầu tập luyện vận động, ưu tiên sản phẩm dễ thao tác, giao diện đơn giản và hướng dẫn rõ ràng.\n"
        "• Định vị truyền thông: MotionIQ là nền tảng AI hỗ trợ theo dõi vận động tại nhà thông qua camera smartphone, giúp nhận diện tư thế, đếm số lần tập và đưa ra phản hồi cơ bản.\n"
        "• Thông điệp chính: 'MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn.'"
    )

    doc.add_heading("4.3. Kênh và Phương thức truyền thông", level=2)
    t_channels = doc.add_table(rows=5, cols=2)
    t_channels.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_channels.autofit = False
    ch_widths = [Inches(1.8), Inches(4.4)]
    
    ch_data = [
        ("Kênh truyền thông", "Phương thức triển khai thực tế"),
        ("TikTok", "Sản xuất video ngắn giới thiệu sản phẩm, các tình huống đời thường trong gia đình và demo tính năng đếm nhịp bằng AI."),
        ("Facebook", "Xây dựng Fanpage, đăng bài chia sẻ kiến thức vận động tuổi già, thông tin sản phẩm và phản hồi của người dùng trải nghiệm."),
        ("Zalo", "Tư vấn 1:1, gửi video hướng dẫn sử dụng, chăm sóc khách hàng và hỗ trợ đăng ký gói trải nghiệm."),
        ("Trực tiếp (Cộng đồng)", "Giới thiệu sản phẩm, tổ chức các buổi trải nghiệm tại câu lạc bộ người cao tuổi và hội đồng hương địa phương.")
    ]

    for r_idx, row in enumerate(t_channels.rows):
        for c_idx, val in enumerate(ch_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = ch_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("4.4. Lộ trình triển khai truyền thông trong 04 tháng", level=2)
    t_plan = doc.add_table(rows=5, cols=3)
    t_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_plan.autofit = False
    plan_widths = [Inches(1.8), Inches(2.8), Inches(1.6)]
    
    plan_data = [
        ("Thời gian triển khai", "Hoạt động chính", "Mục tiêu đạt được"),
        ("Tháng 1: Xây dựng nhận diện", "Hoàn thiện Fanpage, kênh TikTok, bộ nhận diện Bé Nấm; sản xuất video giới thiệu và đăng tải nội dung cơ bản.", "Tạo nhận diện thương hiệu ban đầu và giúp khách hàng biết đến MotionIQ."),
        ("Tháng 2: Tiếp cận khách hàng", "Đăng video tính năng, chia sẻ vấn đề tập luyện tại nhà, quảng bá trên mạng xã hội và thu thập đăng ký trải nghiệm.", "Tăng độ tiếp cận, thu hút 150–180 khách hàng tiềm năng."),
        ("Tháng 3: Trải nghiệm & Niềm tin", "Tổ chức trải nghiệm miễn phí, hướng dẫn sử dụng, thu thập phản hồi, đăng video demo thực tế và khảo sát mức giá.", "Chứng minh giá trị sản phẩm, tạo dựng sự tin tưởng cho 40–50 người dùng."),
        ("Tháng 4: Chuyển đổi & Doanh thu", "Ra mắt gói dịch vụ trả phí, tư vấn gói ưu đãi, chăm sóc khách hàng và triển khai chương trình giới thiệu người dùng mới.", "Chuyển đổi 15–20 khách hàng trả phí đầu tiên, tạo dòng tiền thực tế.")
    ]

    for r_idx, row in enumerate(t_plan.rows):
        for c_idx, val in enumerate(plan_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = plan_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("4.5. Chiến lược định giá dựa trên Giá trị Khách hàng & Cạnh tranh", level=2)
    doc.add_paragraph(
        "Thay vì áp dụng các phương pháp định giá startup quá lớn chưa có cơ sở thực tế, nhóm lựa chọn phương pháp Định giá dựa trên Giá trị Khách hàng "
        "(Customer Value-Based Pricing) kết hợp So sánh Đối thủ Cạnh tranh (Competition-Based Pricing):\n\n"
        "1. So với giá trị tạo ra cho khách hàng: Dựa trên khảo sát thực tế (Câu 16), có tới 64.7% người dùng đồng ý chi trả mức từ 50.000 – 149.000 VNĐ/tháng. "
        "Mức phí dưới 100.000 VNĐ/tháng chỉ tương đương giá của 1-2 bữa ăn sáng nhưng đổi lại con cái nhận được sự an tâm và cha mẹ có người bạn đồng hành tập luyện mỗi ngày.\n"
        "2. So với đối thủ cạnh tranh: Chi phí thuê chuyên viên tập tại nhà (200.000 - 400.000 đ/buổi) hoặc các ứng dụng nước ngoài (>150.000 đ/tháng), mức giá của MotionIQ "
        "rẻ hơn từ 60% đến 95%, tạo ưu thế tiếp cận tuyệt vời.\n\n"
        "• Gói MotionIQ Early Access (Thử nghiệm tháng 4): 49.000 VNĐ/tháng (áp dụng ưu đãi cho nhóm người dùng trải nghiệm đầu tiên).\n"
        "• Gói MotionIQ Standard (Chính thức): 79.000 VNĐ/tháng hoặc gói tiết kiệm 790.000 VNĐ/năm.\n\n"
        "Dự kiến doanh thu ban đầu từ nhóm khách hàng thử nghiệm:"
    )

    t_rev = doc.add_table(rows=4, cols=2)
    t_rev.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_rev.autofit = False
    rev_widths = [Inches(3.1), Inches(3.1)]
    
    rev_data = [
        ("Số lượng khách hàng trả phí", "Doanh thu tháng dự kiến (Gói 49.000 đ)"),
        ("10 khách hàng", "490.000 VNĐ"),
        ("15 khách hàng", "735.000 VNĐ"),
        ("20 khách hàng", "980.000 VNĐ")
    ]

    for r_idx, row in enumerate(t_rev.rows):
        for c_idx, val in enumerate(rev_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = rev_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("4.6. Dự toán ngân sách truyền thông 10.000.000 VNĐ", level=2)
    doc.add_paragraph(
        "Với tổng ngân sách sinh viên 10.000.000 VNĐ trong 04 tháng, nhóm phân bổ chi phí có trọng tâm cho các hoạt động quảng bá, sản xuất nội dung, "
        "tổ chức trải nghiệm và tiếp cận khách hàng nhằm tối ưu tỷ lệ chuyển đổi:"
    )

    t_budget = doc.add_table(rows=8, cols=2)
    t_budget.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_budget.autofit = False
    bud_widths = [Inches(3.8), Inches(2.4)]
    
    bud_data = [
        ("Hạng mục dự toán chi phí trong 04 tháng", "Chi phí dự kiến (VNĐ)"),
        ("Sản xuất nội dung truyền thông (hình ảnh, video)", "3.000.000 VNĐ"),
        ("Quảng cáo chọn lọc trên Facebook và TikTok", "3.000.000 VNĐ"),
        ("Tổ chức hoạt động trải nghiệm sản phẩm trực tiếp", "2.000.000 VNĐ"),
        ("Chi phí đi lại và liên hệ khách hàng", "700.000 VNĐ"),
        ("In ấn mã QR Code và tài liệu giới thiệu", "300.000 VNĐ"),
        ("Chi phí dự phòng phát sinh", "1.000.000 VNĐ"),
        ("TỔNG CỘNG NGÂN SÁCH TRUYỀN THÔNG", "10.000.000 VNĐ")
    ]

    for r_idx, row in enumerate(t_budget.rows):
        for c_idx, val in enumerate(bud_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = bud_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "EAE0D5")
            elif r_idx == 7:
                run.font.bold = True
                set_cell_background(cell, "F2EAE1")
            else:
                set_cell_background(cell, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_heading("4.7. Chỉ tiêu đánh giá hiệu quả truyền thông (KPIs sau 04 tháng)", level=2)
    t_kpi = doc.add_table(rows=6, cols=2)
    t_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_kpi.autofit = False
    kpi_widths = [Inches(3.8), Inches(2.4)]
    
    kpi_data = [
        ("Chỉ tiêu đo lường hiệu quả", "Mục tiêu cụ thể sau 04 tháng"),
        ("Lượt tiếp cận trên mạng xã hội (Reach)", "13.000 – 15.000 lượt"),
        ("Khách hàng tiềm năng để lại thông tin (Leads)", "150 – 180 khách hàng"),
        ("Số người đăng ký tham gia trải nghiệm dùng thử", "40 – 50 người"),
        ("Số người hoàn thành trọn vẹn quy trình trải nghiệm", "30 – 35 người"),
        ("Số khách hàng chuyển đổi sang gói trả phí", "15 – 20 khách hàng")
    ]

    for r_idx, row in enumerate(t_kpi.rows):
        for c_idx, val in enumerate(kpi_data[r_idx]):
            cell = row.cells[c_idx]
            cell.width = kpi_widths[c_idx]
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
    # CHƯƠNG 5: QUẢN TRỊ RỦI RO & DUY TRÌ BỀN VỮNG
    # ==========================================
    doc.add_page_break()
    h_c5 = doc.add_heading("CHƯƠNG 5: QUẢN TRỊ RỦI RO & DUY TRÌ BỀN VỮNG", level=1)
    for r in h_c5.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(140, 47, 30)

    doc.add_heading("5.1. Nhận diện rủi ro thực tế & Biện pháp giảm thiểu", level=2)
    doc.add_paragraph(
        "• Rủi ro 1: Người cao tuổi khó thao tác với camera điện thoại khi ở một mình.\n"
        "  ➔ Biện pháp: Nhóm thiết kế hướng dẫn bằng video hoạt hình ngắn có giọng đọc tiếng Việt rõ ràng, cung cấp tài liệu in có mã QR trực quan; "
        "đồng thời hỗ trợ con cái thiết lập sẵn góc đặt điện thoại cố định tại nhà.\n\n"
        "• Rủi ro 2: Khách hàng lo ngại về độ an toàn khi tự tập luyện.\n"
        "  ➔ Biện pháp: MotionIQ luôn hiển thị thông báo an toàn trước mỗi bài tập (yêu cầu tập gần ghế có tựa, không tập khi thấy chóng mặt); "
        "và tuyên bố minh bạch rằng sản phẩm chỉ đóng vai trò hỗ trợ tập luyện thể chất, không thay thế chẩn đoán hay điều trị y khoa.\n\n"
        "• Rủi ro 3: Tỷ lệ duy trì tập luyện giảm dần sau thời gian đầu hăng hái.\n"
        "  ➔ Biện pháp: Áp dụng cơ chế tích điểm ngày tập (Streak), linh vật Bé Nấm gửi lời khen động viên và gửi báo cáo tóm tắt tuần qua Zalo "
        "để con cái cùng theo dõi và khen ngợi cha mẹ."
    )

    doc.add_heading("5.2. Kế hoạch duy trì và phát triển giai đoạn tiếp theo", level=2)
    doc.add_paragraph(
        "Sau khi hoàn thành mục tiêu 04 tháng đầu tiên với 15–20 khách hàng trả phí, nhóm sẽ tái đầu tư doanh thu để tiếp tục hoàn thiện sản phẩm:\n"
        "• Tối ưu hóa thuật toán nhận diện để hoạt động ổn định hơn trên các dòng smartphone cấu hình thấp.\n"
        "• Bổ sung thêm các bài tập vận động nhẹ nhàng cho khớp cổ tay và khớp cổ chân.\n"
        "• Tích hợp Zalo Mini App để người dùng có thể mở ứng dụng ngay trong Zalo mà không cần cài đặt phức tạp."
    )

    # ==========================================
    # KẾT LUẬN
    # ==========================================
    doc.add_heading("KẾT LUẬN", level=1)
    doc.add_paragraph(
        "Kế hoạch của dự án MotionIQ tập trung vào việc giải quyết bài toán thực tế của các gia đình có người cao tuổi: Giúp cha mẹ duy trì thói quen "
        "tập luyện vận động dễ dàng hơn và giúp con cái an tâm hơn dù bận rộn công việc.\n\n"
        "Bằng cách tiếp cận trung thực, khiêm tốn nhưng bài bản, dựa trên kết quả khảo sát thực tế 50 đối tượng và kế hoạch truyền thông 04 tháng "
        "với ngân sách tinh gọn 10.000.000 VNĐ, MotionIQ hướng đến mục tiêu chứng minh giá trị sản phẩm từ trải nghiệm người dùng thực, hình thành nhóm "
        "khách hàng trung thành ban đầu và từng bước xây dựng một dự án khởi nghiệp sinh viên bền vững, giàu tính nhân văn."
    )

    # Save to disk
    out_dir = r"c:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq"
    out_path = os.path.join(out_dir, "BaoCao_ToanDien_MotionIQ_EXE101.docx")
    doc.save(out_path)
    print(f"Successfully generated refined DOCX report at: {out_path}")

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
