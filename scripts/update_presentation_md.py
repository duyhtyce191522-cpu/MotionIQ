import os

p_brain = r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a\PhanCong_ThuyetTrinh_MotionIQ_EXE101.md"
p_proj = r"motioniq/PhanCong_ThuyetTrinh_MotionIQ_EXE101.md"
p_pub = r"motioniq/public/PhanCong_ThuyetTrinh_MotionIQ_EXE101.md"

with open(p_brain, "r", encoding="utf-8") as f:
    text = f.read()

# Replace any occurrence of forbidden words
text = text.replace("an toàn y tế", "an toàn & định vị ứng dụng hỗ trợ")
text = text.replace("thiết bị y tế", "ứng dụng công nghệ hỗ trợ vận động")
text = text.replace("y tế", "hỗ trợ thể chất")
text = text.replace("bảo mật tuyệt đối", "bảo đảm quyền riêng tư tối đa")
text = text.replace("tuyệt đối KHÔNG", "cam kết KHÔNG")
text = text.replace("tuyệt đối", "tối đa")

# Update table of members for Tin and Nghi
old_tbl_tin = "• **CHƯƠNG 4 (Toàn bộ Mục 4.1 đến 4.7):** Kế hoạch truyền thông 4 tháng, Định giá 49k, Ngân sách 10 triệu, KPIs | **Kế hoạch truyền thông 4 tháng (TikTok/FB/Zalo/Offline), Định giá 49k, Phân bổ ngân sách 10 triệu & Bảng KPIs**"
new_tbl_tin = "• **CHƯƠNG 4 (Toàn bộ Mục 4.1 đến 4.8):** Kế hoạch tài chính, Định giá 49k, Ngân sách 10tr, CAC, Phân tích hòa vốn vận hành & toàn phần | **Kế hoạch truyền thông 4 tháng, Định giá Customer Value, Ngân sách 10tr, Phễu chuyển đổi, CAC & Điểm hòa vốn chi tiết**"
text = text.replace(old_tbl_tin, new_tbl_tin)

old_tbl_nghi = "• **CHƯƠNG 5 (Toàn bộ Mục 5.1 & 5.2):** Quản trị rủi ro thực tế & Kế hoạch duy trì phát triển bền vững (Zalo Mini App) | **Quản trị 3 rủi ro thực tế, Kế hoạch phát triển bền vững Zalo Mini App, Kêu gọi hành động (The Ask) & Kết thúc**"
new_tbl_nghi = "• **CHƯƠNG 5 (Toàn bộ Mục 5.1 & 5.2):** Quản trị 7 rủi ro thực tế & Lộ trình 3 giai đoạn phát triển bền vững (Zalo Mini App) | **Quản trị 7 rủi ro thực tế, Lộ trình 3 giai đoạn phát triển Zalo Mini App, Kêu gọi hành động (The Ask) & Kết thúc**"
text = text.replace(old_tbl_nghi, new_tbl_nghi)

tin_old = """### 5. MÃ PHÚ TÍN (Growth & Media)
* **Phần phụ trách:** **CHƯƠNG 4 (TOÀN BỘ) — KẾ HOẠCH TRUYỀN THÔNG & PHÁT TRIỂN DOANH THU**
* **Thời lượng:** ~2.5 phút
* **Chuyên ngành:** Truyền thông đa phương tiện
* **Nội dung trình bày:**
  1. **Mục 4.1 – 4.3 — Mục tiêu, Thông điệp & 4 Kênh truyền thông:**
     - Thông điệp chính: *"MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn."*
     - 4 kênh trọng tâm: Kênh video ngắn TikTok/Facebook Reels, Fanpage cộng đồng con cái chăm sóc cha mẹ, Zalo OA tư vấn 1:1, Trực tiếp tại các CLB hưu trí Cần Thơ.
  2. **Mục 4.4 — Lộ trình 4 tháng thực thi:**
     - *Tháng 1:* Xây dựng nhận diện thương hiệu & bộ linh vật Bé Nấm.
     - *Tháng 2:* Tiếp cận khách hàng, thu hút 150–180 leads quan tâm.
     - *Tháng 3:* Tổ chức dùng thử trải nghiệm thực tế cho 40–50 hộ gia đình.
     - *Tháng 4:* Ra mắt gói trả phí, kích hoạt chuyển đổi doanh thu thực tế.
  3. **Mục 4.5 — Chiến lược định giá dựa trên Giá trị Khách hàng & Cạnh tranh:**
     - Gói **Early Access: 49.000 VNĐ / tháng** (tương đương 1 bữa ăn sáng, phù hợp kết quả khảo sát 64.7% người đồng thuận mức giá <100k).
     - Gói Tiêu chuẩn: **79.000 VNĐ / tháng** (hoặc 790.000 VNĐ/năm).
  4. **Mục 4.6 & 4.7 — Ngân sách 10 triệu & Bảng KPIs:**
     - Phân bổ ngân sách sinh viên 10.000.000 VNĐ: Video nội dung (3tr), Quảng cáo chọn lọc (3tr), Trải nghiệm cộng đồng (2tr), In ấn & dự phòng (2tr).
     - KPIs sau 4 tháng: Tiếp cận 13.000 – 15.000 lượt; chuyển đổi **15 – 20 khách hàng trả phí đầu tiên**.
* **Câu chuyển giao (Hand-off):**  
  > *"Để đảm bảo dự án phát triển bền vững và kiểm soát tốt các tình huống phát sinh, bạn Hồ Tuyết Nghi — CMO sẽ trình bày về Quản trị rủi ro và định hướng tương lai."*"""

tin_new = """### 5. MÃ PHÚ TÍN (Growth & Media)
* **Phần phụ trách:** **CHƯƠNG 4 (TOÀN BỘ MỤC 4.1 ĐẾN 4.8) — KẾ HOẠCH TRUYỀN THÔNG, TÀI CHÍNH & PHÁT TRIỂN DOANH THU**
* **Thời lượng:** ~2.5 phút
* **Chuyên ngành:** Truyền thông đa phương tiện
* **Nội dung trình bày:**
  1. **Mục 4.1 – 4.4 — Chiến dịch truyền thông 4 tháng tinh gọn:**
     - Thông điệp xuyên suốt: *"MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn."*
     - 4 kênh trọng điểm: Video ngắn TikTok/Reels chạm cảm xúc con cái, Fanpage chăm sóc cha mẹ, Zalo OA tư vấn 1:1, Trực tiếp tại CLB hưu trí Cần Thơ.
     - Lộ trình 4 tháng: T1 (Nhận diện & Bé Nấm) -> T2 (Tiếp cận 150-180 leads) -> T3 (Dùng thử 40-50 gia đình) -> T4 (Kích hoạt trả phí).
  2. **Mục 4.5 — Chiến lược định giá dựa trên Giá trị Khách hàng & Cạnh tranh:**
     - Gói Miễn phí (0đ): 2 bài tập cơ bản, tiếp cận đại chúng.
     - Gói **Early Access: 49.000 VNĐ/tháng** (bằng 1 bữa sáng, đúng kết quả khảo sát 64.7% khách hàng sẵn sàng trả <100k/tháng, rẻ hơn 1/10 thuê PT hoặc phòng tập).
     - Gói Tiêu chuẩn: **79.000 VNĐ/tháng** (hoặc 790.000 VNĐ/năm).
  3. **Mục 4.6 & 4.7 — Ngân sách 10 triệu, Phễu chuyển đổi & Chỉ số CAC:**
     - Ngân sách 10.000.000 VNĐ: Video nội dung (3tr), Quảng cáo chọn lọc (3tr), Trải nghiệm cộng đồng (2tr), In ấn ấn phẩm & dự phòng (2tr).
     - Phễu 4 tầng: 13.000-15.000 tiếp cận -> 150-180 người quan tâm (1.1%) -> 40-50 dùng thử (26.7%) -> **15-20 khách hàng trả phí (37.5%)**.
     - **Chỉ số CAC:** 500.000 – 666.667 VNĐ/khách. *Giải trình thuyết phục:* Chi phí ban đầu bao gồm xây dựng thương hiệu dài hạn; khi khách hàng duy trì thuê bao (LTV đạt 600.000 – 790.000 VNĐ) thì LTV > CAC, dự án hoàn toàn có lãi.
  4. **Mục 4.8 — Dự báo doanh thu & Bảng phân tích điểm hòa vốn chi tiết:**
     - Chi phí cố định vận hành (FC): 1.000.000 VNĐ/tháng (Cloud & API); Chi phí biến đổi (VC): 10.000 VNĐ/khách/tháng.
     - **Hòa vốn vận hành (Tự nuôi sống hệ thống):** Cần **26 khách hàng gói Early Access** (49k) hoặc **15 khách hàng gói Standard** (79k). Dòng tiền MRR đủ bù 100% chi phí máy chủ mà nhóm không cần bù lỗ thêm!
     - **Hòa vốn toàn phần (Bù cả marketing 2.5tr/tháng):** Cần **90 khách hàng gói 49k** hoặc **51 khách hàng gói Standard 79k**.
* **Câu chuyển giao (Hand-off):**  
  > *"Để đảm bảo dự án kiểm soát rủi ro vận hành và có lộ trình mở rộng bài bản, em xin mời bạn Hồ Tuyết Nghi — CMO trình bày Quản trị rủi ro và Lộ trình phát triển bền vững."*"""

text = text.replace(tin_old, tin_new)

nghi_old = """### 6. HỒ TUYẾT NGHI (CMO — Giám đốc Tiếp thị & Dịch vụ)
* **Phần phụ trách:** **CHƯƠNG 5 (TOÀN BỘ) — QUẢN TRỊ RỦI RO & DUY TRÌ BỀN VỮNG**
* **Thời lượng:** ~2.0 phút
* **Chuyên ngành:** Quản trị Dịch vụ
* **Nội dung trình bày:**
  1. **Mục 5.1 — Nhận diện 3 rủi ro thực tế & Biện pháp giảm thiểu:**
     - *Rủi ro 1: Người lớn tuổi khó thao tác camera:* Cung cấp video hoạt hình tiếng Việt ngắn gọn, tài liệu in mã QR và hỗ trợ con cái cố định góc máy lần đầu.
     - *Rủi ro 2: Lo ngại an toàn khi tập:* Luôn hiển thị cảnh báo an toàn trước mỗi bài tập (yêu cầu tập gần ghế tựa, dừng tập nếu chóng mặt); tuyên bố minh bạch chỉ là công cụ hỗ trợ thể lực.
     - *Rủi ro 3: Nản lòng sau vài ngày tập:* Cơ chế tính chuỗi ngày tập (Streak), Bé Nấm khen ngợi và gửi báo cáo tóm tắt tuần qua Zalo để con cái cùng chúc mừng cha mẹ.
  2. **Mục 5.2 — Kế hoạch phát triển bền vững:**
     - Tái đầu tư doanh thu từ 15–20 khách trả phí đầu tiên để tối ưu thuật toán trên dòng máy cấu hình thấp.
     - Tích hợp **Zalo Mini App** giúp mở ứng dụng ngay trong Zalo không cần cài đặt.
  3. **Kết luận & Kêu gọi hành động (The Ask):**
     - Đúc kết giá trị: Giúp cha mẹ duy trì vận động nhẹ nhàng, giúp con cái an tâm làm việc.
     - Cảm ơn Thầy Trần Ngọc Sơn và Hội đồng Giám khảo, mời Hội đồng bước vào phần Q&A."""

nghi_new = """### 6. HỒ TUYẾT NGHI (CMO — Giám đốc Tiếp thị & Dịch vụ)
* **Phần phụ trách:** **CHƯƠNG 5 (TOÀN BỘ MỤC 5.1 & 5.2) — QUẢN TRỊ RỦI RO & LỘ TRÌNH PHÁT TRIỂN BỀN VỮNG**
* **Thời lượng:** ~2.0 phút
* **Chuyên ngành:** Quản trị Dịch vụ
* **Nội dung trình bày:**
  1. **Mục 5.1 — Quản trị 7 rủi ro thực tế trong triển khai:**
     - *Rủi ro thao tác người cao tuổi:* Geriatric UX chữ lớn, tương phản cao, Bé Nấm hướng dẫn giọng nói tiếng Việt to rõ.
     - *Rủi ro rung lắc nhận diện:* One-Euro Filter khử rung, kiểm tra góc máy trước khi tập.
     - *Rủi ro chuyển đổi trả phí:* Bản dùng thử miễn phí, minh bạch lợi ích, giá Early Access 49k/tháng.
     - *Rủi ro CAC cao:* Tập trung kênh chuyển đổi tự nhiên qua con cái và câu lạc bộ người cao tuổi địa phương.
     - *Rủi ro duy trì (Churn):* Tích điểm chuỗi ngày tập (Streak), báo cáo tuần gửi tự động qua Zalo cho con cái.
     - *Rủi ro định vị phân loại ứng dụng:* Tuyên bố minh bạch MotionIQ là ứng dụng hỗ trợ vận động thể chất tại nhà, không thay thế bác sĩ hay chuyên viên.
     - *Rủi ro bảo vệ dữ liệu cá nhân:* Kiến trúc 100% On-Device AI, camera xử lý trực tiếp trên RAM rồi hủy ngay, không lưu trữ ảnh trên máy chủ.
  2. **Mục 5.2 — Lộ trình 3 giai đoạn phát triển bền vững:**
     - *Giai đoạn 1 (04 tháng đầu):* Kiểm chứng MVP với 40-50 hộ gia đình, đạt 15-20 khách trả phí đầu tiên.
     - *Giai đoạn 2 (Tháng 5 - Tháng 6):* Đánh giá tỷ lệ duy trì (Retention), tối ưu hóa thuật toán và kiểm chứng gói Standard 79.000 VNĐ.
     - *Giai đoạn 3 (Mở rộng):* Tích hợp **Zalo Mini App** (mở trực tiếp không cần cài đặt), mở rộng sang viện dưỡng lão và trung tâm chăm sóc người cao tuổi.
  3. **Kết luận & Kêu gọi hành động (The Ask):**
     - Đúc kết giá trị: Giúp cha mẹ duy trì vận động nhẹ nhàng, giúp con cái an tâm làm việc.
     - Cảm ơn Thầy Trần Ngọc Sơn và Hội đồng Giám khảo, mời Hội đồng bước vào phần Q&A."""

text = text.replace(nghi_old, nghi_new)

for p in [p_brain, p_proj, p_pub]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)

print("Updated PhanCong_ThuyetTrinh_MotionIQ_EXE101.md across all destinations!")
