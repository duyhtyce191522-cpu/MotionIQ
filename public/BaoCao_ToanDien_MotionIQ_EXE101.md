BỘ GIÁO DỤC VÀ ĐÀO TẠO
TRƯỜNG ĐẠI HỌC FPT CẦN THƠ

———————————————***———————————————

BÁO CÁO TỔNG KẾT DỰ ÁN KHỞI NGHIỆP (FINAL REPORT)
HỌC PHẦN: EXE101 — TRẢI NGHIỆM KHỞI NGHIỆP

MOTIONIQ — NỀN TẢNG TRỢ LÝ AI HỖ TRỢ THEO DÕI TẬP LUYỆN VẬN ĐỘNG TẠI NHÀ CHO NGƯỜI CAO TUỔI
(100% ON-DEVICE AI)

"MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn."
(Hợp nhất: Checkpoint 1 • Checkpoint 2 • Checkpoint 3 • Kế hoạch tài chính & truyền thông phát triển doanh thu)


| Giảng viên hướng dẫn: | Thầy Trần Ngọc Sơn |
| --- | --- |
| Tên nhóm sinh viên: | MOTIONIQ — Nhóm K19 |
| Trưởng nhóm (CEO): | Huỳnh Thị Yến Duy — MSSV: CE191522 |
| Thành viên nhóm: | Nguyễn Hải Hà (CTO) • Nguyễn Nhã Quân (CPO) Mã Phú Tín • Đặng Vĩnh Phúc • Hồ Tuyết Nghi (CMO) |
| Website Demo MVP: | https://motion-iq-five.vercel.app |
| Thực nghiệm & Khảo sát: | 50 phiếu khảo sát thực tế • 5 buổi thử nghiệm nguyên mẫu |

TP. CẦN THƠ, THÁNG 11 NĂM 2026


# LỜI CẢM ƠN

Nhóm thực hiện dự án MotionIQ xin gửi lời tri ân sâu sắc và lòng biết ơn chân thành nhất đến Thầy Trần Ngọc Sơn, người đã tận tâm truyền đạt kiến thức khởi nghiệp đổi mới sáng tạo, phương pháp tư duy mô hình kinh doanh và kiên nhẫn định hướng, góp ý chuyên môn quý báu qua từng cột mốc Checkpoint 1, Checkpoint 2 và Checkpoint 3 của học phần EXE101 (Trải nghiệm khởi nghiệp).

Nhóm cũng xin chân thành cảm ơn các cô bác lớn tuổi và người thân đã nhiệt tình tham gia 50 phiếu khảo sát thực địa cũng như 5 buổi thử nghiệm trực tiếp nguyên mẫu ứng dụng. Những đóng góp thực tế từ người dùng chính là kim chỉ nam giúp nhóm hoàn thiện sản phẩm MotionIQ hữu ích và nhân văn nhất.


# TÓM TẮT DỰ ÁN (EXECUTIVE SUMMARY)

MotionIQ là giải pháp công nghệ ứng dụng Trí tuệ Nhân tạo thị giác máy tính chạy trực tiếp trên thiết bị di động (100% On-Device AI), hỗ trợ người cao tuổi theo dõi quá trình tập luyện vận động và rèn luyện thăng bằng tại nhà thông qua camera smartphone hoặc laptop mà không cần đầu tư thêm các thiết bị cảm biến phần cứng tốn kém.

Bằng cách kết hợp linh vật trợ lý ảo 'Bé Nấm' với lời nhắc nhở đếm nhịp bằng tiếng Việt, mô hình nhận diện tư thế dựa trên các bộ dữ liệu chuyển động mẫu đã công bố (UI-PRMD, KIMORE, EHE) và bộ lọc khử nhiễu One-Euro Filter, MotionIQ giúp người lớn tuổi duy trì thói quen vận động đúng tư thế, đếm số lần tập và đưa ra phản hồi cơ bản. Kết quả khảo sát thực tế trên 50 đối tượng cho thấy hơn 68% con cái gặp khó khăn khi trực tiếp quan sát cha mẹ tập luyện, và 82.4% sẵn sàng cho người thân dùng thử ứng dụng. Thử nghiệm thực tế qua 5 buổi đạt chỉ số đo góc vận động (ROM) đạt 94.6% so với góc đo đối chiếu và điểm khả dụng hệ thống SUS đạt 84.5/100 (Mức xuất sắc).

Về chiến lược kinh doanh và tài chính, nhóm áp dụng phương pháp định giá dựa trên giá trị khách hàng và so sánh đối thủ cạnh tranh với gói dùng thử Early Access 49.000 VNĐ/tháng, kết hợp kế hoạch truyền thông 04 tháng tinh gọn với ngân sách sinh viên 10.000.000 VNĐ. Phân tích điểm hòa vốn cho thấy với 26 khách hàng trả phí gói Early Access hoặc 15 khách hàng gói Standard, dự án sẽ tự bù đắp đủ chi phí vận hành cố định hàng tháng (1.000.000 VNĐ/tháng).


## DANH MỤC TỪ VIẾT TẮT


| Từ viết tắt | Thuật ngữ Tiếng Anh | Ý nghĩa Tiếng Việt |
| --- | --- | --- |
| AI | Artificial Intelligence | Trí tuệ Nhân tạo |
| BMC | Business Model Canvas | Khung Mô hình Kinh doanh 9 Khối |
| ROM | Range of Motion | Biên độ góc vận động của khớp |
| CAC | Customer Acquisition Cost | Chi phí thu hút một khách hàng mới |
| MRR | Monthly Recurring Revenue | Doanh thu định kỳ hằng tháng |
| SUS | System Usability Scale | Thang đo Độ khả dụng Hệ thống (Chuẩn quốc tế) |
| On-Device AI | On-Device Artificial Intelligence | Trí tuệ nhân tạo xử lý trực tiếp trên thiết bị |


# DANH MỤC BẢNG BIỂU

Danh sách các bảng biểu tổng hợp dữ liệu thực nghiệm, tài chính và kế hoạch trong báo cáo:

Bảng 1.1: Hồ sơ phân công trách nhiệm & Chương đảm nhiệm (RACI Matrix)	Trang 6

Bảng 2.1: Tổng hợp kết quả phân tích dữ liệu khảo sát thực tế (N = 50)	Trang 7

Bảng 2.2: Bảng phân tích so sánh đối thủ cạnh tranh & Lợi thế định vị MotionIQ	Trang 8

Bảng 3.1: Kết quả thử nghiệm hiệu năng nguyên mẫu MVP thực tế qua 5 buổi	Trang 10

Bảng 4.1: Ma trận kênh và phương thức truyền thông thực tế	Trang 11

Bảng 4.2: Lộ trình triển khai kế hoạch truyền thông trong 04 tháng	Trang 12

Bảng 4.3: Cơ cấu giá dịch vụ dự kiến của MotionIQ	Trang 12

Bảng 4.4: Dự toán ngân sách truyền thông 10.000.000 VNĐ trong 04 tháng	Trang 13

Bảng 4.5: Bảng chỉ tiêu đánh giá hiệu quả truyền thông (KPIs sau 04 tháng)	Trang 13

Bảng 4.6: Dự báo doanh thu tháng ban đầu theo số lượng khách hàng gói Early Access	Trang 14

Bảng 4.7: Bảng phân tích điểm hòa vốn theo các kịch bản chi phí	Trang 14

Bảng 5.1: Ma trận nhận diện rủi ro thực tế & Biện pháp giảm thiểu	Trang 15


# MỤC LỤC

(Bảng mục lục phân cấp chi tiết theo các chương và thành viên đảm nhiệm)

LỜI CẢM ƠN	2

TÓM TẮT DỰ ÁN (EXECUTIVE SUMMARY)	2

DANH MỤC TỪ VIẾT TẮT	3

DANH MỤC BẢNG BIỂU	4

CHƯƠNG 1: THIẾT LẬP DỰ ÁN & NĂNG LỰC ĐỘI NGŨ (Phụ trách: Huỳnh Thị Yến Duy)	5

1.1. Bối cảnh ra đời ý tưởng MotionIQ	5

1.2. Sứ mệnh, Tầm nhìn và Hệ giá trị cốt lõi	5

1.3. Hồ sơ năng lực đội ngũ sáng lập (Founding Team & RACI)	6

CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (Phụ trách: Nguyễn Nhã Quân, Đặng Vĩnh Phúc)	7

2.1. Phương pháp luận và Quy mô khảo sát thực tế (N = 50)	7

2.2. Kết quả phân tích dữ liệu khảo sát thực tế từ Google Sheets (N = 50)	7

2.3. Chân dung khách hàng mục tiêu & Bản đồ thấu cảm (Empathy Map)	8

2.4. Phân tích đối thủ cạnh tranh & Lợi thế định vị (Competitive Analysis)	8

CHƯƠNG 3: MÔ HÌNH KINH DOANH & NGUYÊN MẪU MVP (Phụ trách: Nguyễn Hải Hà, Nguyễn Nhã Quân)	9

3.1. Khung Mô hình Kinh doanh 9 Khối (Business Model Canvas)	9

3.2. Kiến trúc giải pháp kỹ thuật & Thuật toán 100% On-Device AI	10

3.3. 4 Bài tập vận động chức năng chuẩn hóa	10

3.4. Kết quả 5 buổi thử nghiệm nguyên mẫu MVP thực tế	10

CHƯƠNG 4: KẾ HOẠCH TRUYỀN THÔNG & PHÁT TRIỂN DOANH THU (Phụ trách: Mã Phú Tín)	11

4.1. Mục tiêu truyền thông trong 04 tháng	11

4.2. Khách hàng mục tiêu & Thông điệp truyền thông	11

4.3. Kênh và Phương thức truyền thông	11

4.4. Lộ trình triển khai truyền thông trong 04 tháng	12

4.5. Chiến lược định giá (Pricing Strategy)	12

4.6. Dự toán ngân sách và chi phí vận hành	13

4.7. Kế hoạch phát triển doanh thu & Chỉ tiêu KPIs	13

4.8. Dự báo doanh thu và Phân tích điểm hòa vốn	14

CHƯƠNG 5: QUẢN TRỊ RỦI RO & DUY TRÌ BỀN VỮNG (Phụ trách: Hồ Tuyết Nghi)	15

5.1. Nhận diện rủi ro thực tế & Biện pháp giảm thiểu	15

5.2. Kế hoạch duy trì và phát triển giai đoạn tiếp theo	15

KẾT LUẬN (Phụ trách: Huỳnh Thị Yến Duy)	16


# CHƯƠNG 1: THIẾT LẬP DỰ ÁN & NĂNG LỰC ĐỘI NGŨ (CHECKPOINT 1)

[Thành viên phụ trách biên soạn chính: Huỳnh Thị Yến Duy — CEO (Trưởng nhóm)]


## 1.1. Bối cảnh ra đời ý tưởng MotionIQ

Việt Nam hiện là một trong những quốc gia có tốc độ già hóa dân số nhanh nhất thế giới. Theo Tổng cục Thống kê, số lượng người từ 60 tuổi trở lên đã vượt 13.5 triệu người (chiếm 13.5% dân số). Cùng với quá trình lão hóa tự nhiên, người cao tuổi thường gặp các vấn đề về suy giảm sức mạnh cơ bắp, thoái hóa khớp gối, cột sống và giảm khả năng giữ thăng bằng, dẫn đến nguy cơ té ngã và hạn chế sinh hoạt hàng ngày.

Việc duy trì thói quen tập luyện vận động nhẹ nhàng tại nhà đóng vai trò quan trọng trong việc cải thiện sự dẻo dai và nâng cao thể trạng. Tuy nhiên, đa số người lớn tuổi tự tập theo thói quen mà không biết mình làm đúng hay sai tư thế; trong khi con cái bận rộn đi làm không thể thường xuyên quan sát, nhắc nhở. Xuất phát từ thực tế chăm sóc người thân trong gia đình, nhóm MedTech Pioneers đã phát triển dự án MotionIQ — ứng dụng công nghệ AI thị giác trên điện thoại để trở thành người bạn đồng hành hỗ trợ theo dõi vận động, đếm nhịp và đưa ra phản hồi cơ bản cho người cao tuổi ngay tại nhà.


## 1.2. Sứ mệnh, Tầm nhìn và Hệ giá trị cốt lõi

• Sứ mệnh (Mission): 'Bình dân hóa dịch vụ hỗ trợ tập luyện vận động chất lượng đến từng hộ gia đình Việt Nam' — mang lại khả năng vận động tự chủ, giảm thiểu nguy cơ té ngã cho người già và giúp con cái yên tâm hơn khi đi làm xa.
• Tầm nhìn (Vision): Trở thành nền tảng số hỗ trợ theo dõi vận động cá nhân phổ biến tại Việt Nam vào năm 2027.
• Hệ giá trị cốt lõi (Core Values):
  1. An toàn & Dựa trên dữ liệu (Evidence-based): Mọi bài tập đều dựa trên các bài vận động chức năng chuẩn hóa từ các bộ dữ liệu chuyển động công khai đã được nghiên cứu và sử dụng trước đó.
  2. Tôn trọng quyền riêng tư (Privacy by Design): Xử lý AI 100% cục bộ trên máy người dùng, kiên quyết nói KHÔNG với việc lưu trữ hình ảnh cá nhân lên máy chủ đám mây.
  3. Đồng cảm với tuổi già (Geriatric Empathy): Giao diện chữ lớn, tương tác một chạm, khích lệ người già bằng sự ấm áp và kiên nhẫn của linh vật Bé Nấm.

## 1.3. Hồ sơ năng lực đội ngũ sáng lập (Founding Team & RACI)

Đội ngũ sáng lập MotionIQ (MOTIONIQ — Nhóm K19) là sự kết hợp chặt chẽ giữa các chuyên ngành Công nghệ Thông tin (An toàn thông tin), Thiết kế Đồ họa / UI-UX, Truyền thông đa phương tiện, Ngôn ngữ và Quản trị Dịch vụ tạo nên lợi thế triển khai thực tế:


| Họ và Tên | Vai trò | Chuyên ngành | Chương đảm nhiệm trong Báo cáo | Trách nhiệm chính (RACI) |
| --- | --- | --- | --- | --- |
| Huỳnh Thị Yến Duy | CEO (Trưởng nhóm) | An toàn thông tin | Chương 1 (Toàn bộ), Mở đầu, Kết luận & Soát xét chung | Chịu trách nhiệm toàn diện kĩ thuật dựng web/app. Phát triển MediaPipe Pose và quản lí dự án |
| Nguyễn Nhã Quân | CPO | Thiết kế UI-UX | Chương 2 (Mục 2.1, 2.2: Khảo sát) & Chương 3 (Mục 3.4: Thử nghiệm MVP) | Phân tích dữ liệu khảo sát Google Sheets, thiết kế Geriatric UI và thử nghiệm MVP (ROM 94.6%, SUS 84.5) |
| Đặng Vĩnh Phúc | Thành viên | Ngôn ngữ | Chương 2 (Mục 2.3 & 2.4: Khách hàng & 4 Đối thủ) | Nghiên cứu đối thủ cạnh tranh, chuyển đổi ngôn ngữ và kết nối cộng đồng Cần Thơ |
| Nguyễn Hải Hà | CTO | An toàn thông tin | Chương 3 (Mục 3.2: On-Device AI & Mục 3.3: 4 Bài tập) | Chịu trách nhiệm kỹ thuật AI, bộ dataset chuẩn, thuật toán khử rung One-Euro và bảo mật RAM |
| Mã Phú Tín | Thành viên | Truyền thông | Chương 4 (Toàn bộ Mục 4.1 – 4.8: Kế hoạch truyền thông & Tài chính) | Lên kế hoạch truyền thông đa kênh TikTok/FB, định giá 49k, ngân sách 10 triệu, KPIs & Điểm hòa vốn |
| Hồ Tuyết Nghi | CMO | Quản trị Dịch vụ | Chương 5 (Toàn bộ Mục 5.1 & 5.2: Quản trị rủi ro & Duy trì bền vững) | Quản trị rủi ro thực tế, kế hoạch mở rộng Zalo Mini App và định hướng dịch vụ bền vững |


| 📌 ĐIỂM MẠNH ĐỘI NGŨ & NGUYÊN TẮC GIỚI HẠN AN TOÀN Sự bổ trợ giữa chuyên môn Kỹ thuật AI giúp MotionIQ tương tác trực tiếp với khách hàng, cùng với đó là sử dụng MotionIQ trên thiết bị di động laptop mà không cần tốn chi phí mua các thiết bị lớn tốn nhiều chi phí để tập tại nhà.  LƯU Ý QUAN TRỌNG: MotionIQ chỉ là công cụ hỗ trợ tập luyện vận động tại nhà, không thay thế chuyên viên hay thay thế bác sĩ. |
| --- |


# CHƯƠNG 2: NGHIÊN CỨU THỊ TRƯỜNG & KHẢO SÁT THỰC ĐỊA (CHECKPOINT 2)

[Thành viên phụ trách biên soạn: Nguyễn Nhã Quân (Mục 2.1, 2.2) & Đặng Vĩnh Phúc (Mục 2.3, 2.4)]


## 2.1. Phương pháp luận và Quy mô khảo sát thực tế (N = 50)

Để xác thực giả thuyết bài toán và nhu cầu thực tế của thị trường trong giai đoạn Checkpoint 2, nhóm đã tiến hành khảo sát thực địa 50 đối tượng thông qua biểu mẫu câu hỏi trực tuyến (dữ liệu lưu trữ công khai tại Google Sheets: https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM):
• Đối tượng trả lời khảo sát: 82.4% thuộc độ tuổi 18 - 23 tuổi và 17.6% từ 23 - 30 tuổi (đại diện cho đối tượng con cháu quan tâm chăm sóc người thân).
• Kinh nghiệm hỗ trợ người thân: 64.7% cho biết trong 1 năm gần đây có chăm sóc hoặc hỗ trợ người thân trong sinh hoạt hoặc vận động.
• Độ tuổi của người thân cần hỗ trợ: 31.4% từ 60–69 tuổi; 23.5% từ 70–79 tuổi; 9.8% từ 80 tuổi trở lên (tổng cộng 64.7% người thân từ 60 tuổi trở lên) và 23.5% từ 50–59 tuổi.


## 2.2. Kết quả phân tích dữ liệu khảo sát thực tế từ Google Sheets (N = 50)


| Nội dung khảo sát thực tế (Dữ liệu thực N = 50) | Tỷ lệ thực tế | Hàm ý phát triển MotionIQ |
| --- | --- | --- |
| Con cái không thể thường xuyên quan sát, sửa động tác cho người thân | 68.6% | Người già thường phải tập một mình, rất cần AI theo dõi. |
| Người thân tập luyện hàng ngày hoặc 3-5 lần/tuần | 51.0% | Nhu cầu tập luyện là liên tục, cần công cụ thường trực tại nhà. |
| Khó khăn lớn nhất: Không biết tập đúng/sai, không có phản hồi và cảnh báo | 82.4% | AI phải có chức năng đếm nhịp và sửa lỗi tư thế tức thì. |
| 3 yếu tố quan trọng nhất: Dễ sử dụng, Báo đúng/sai, Hướng dẫn sửa động tác | 88.2% | Bắt buộc thiết kế Geriatric UI: Chữ to, nút to, 1-chạm. |
| Mức độ phù hợp của MotionIQ với nhu cầu (Đánh giá mức 4 - 5 sao) | 66.7% | Mô hình giải pháp giải quyết đúng nhu cầu của đa số gia đình. |
| Sẵn sàng cho người thân dùng thử MotionIQ (Đánh giá mức 4 - 5 sao) | 82.4% | Tỷ lệ chấp nhận dùng thử và chuyển đổi tiềm năng rất cao. |
| Chấp nhận chi trả mức phí 50.000 – 149.000 VNĐ/tháng | 64.7% | Mức giá thuê bao tháng 49.000 – 79.000 VNĐ là hoàn toàn tối ưu. |

Khi khảo sát về điều lo ngại nhất khi sử dụng camera và AI (Câu 14 trong bảng khảo sát):
1. Lo ngại về quyền riêng tư và hình ảnh (được 45% người tham gia đề cập).
2. Người lớn tuổi khó thao tác thiết bị công nghệ (50%).
3. AI có thể nhận diện không chính xác do chuyển động người già bị chậm hoặc run tay chân (40%).

Chính kết quả khảo sát thực tế này là cơ sở vững chắc để nhóm thiết kế kiến trúc kỹ thuật của MotionIQ:
• Xóa bỏ lo ngại riêng tư bằng kiến trúc 100% On-Device AI: Video chỉ xử lý cục bộ trên RAM, không truyền hình ảnh lên máy chủ.
• Xóa bỏ lo ngại khó dùng bằng Geriatric UI: Phông chữ to >= 18px, nút bấm lớn >= 56px, trợ lý Bé Nấm nói tiếng Việt rõ ràng.
• Cải thiện độ chính xác bằng Bộ lọc One-Euro Filter: Triệt tiêu rung tay chân sinh lý khi theo dõi chuyển động.


## 2.3. Chân dung khách hàng mục tiêu & Bản đồ thấu cảm (Empathy Map)

Mô hình khách hàng của MotionIQ có đặc tính kép (Dual-Customer Profile): Người sử dụng trực tiếp (Người cao tuổi) và Người ra quyết định chi trả (Con cái):
• Persona 1 — Người dùng trực tiếp: Bác Nguyễn Văn An, 68 tuổi, hưu trí tại TP. Cần Thơ. Bác có nhu cầu rèn luyện cơ chân và khớp gối hàng ngày để đi lại vững vàng hơn. Bác mắt kém, sợ làm phiền con cái, cảm thấy chán nản khi phải tập các động tác lặp lại một mình mà không biết đúng hay sai.
• Persona 2 — Người chi trả: Chị Thu Hằng, 36 tuổi, nhân viên văn phòng. Chị quan tâm đến sức khỏe cha mẹ nhưng bận rộn công việc, luôn bất an không biết ở nhà ba tập luyện ra sao. Chị sẵn sàng bỏ ra một khoản chi phí nhỏ hàng tháng (dưới 100.000 VNĐ) để có ứng dụng hỗ trợ ba tập luyện đều đặn và an tâm hơn.


## 2.4. Phân tích đối thủ cạnh tranh & Lợi thế định vị (Competitive Analysis)


| Giải pháp cạnh tranh | Ưu điểm | Hạn chế thực tế | Lợi thế định vị của MotionIQ |
| --- | --- | --- | --- |
| Tự tập theo YouTube / Tivi | Hoàn toàn miễn phí, phong phú | Không có tương tác, không sửa sai tư thế, dễ tập sai | AI nhận diện tư thế, đếm nhịp và phản hồi âm thanh tức thì |
| Thuê huấn luyện viên tại nhà | Theo sát 1:1, động viên tốt | Chi phí rất cao (200k-400k/buổi, 2-4tr/tháng), khó duy trì | Chi phí rất rẻ (49k-79k/tháng), chủ động tập mọi lúc |
| CLB Thể dục dưỡng sinh | Có cộng đồng giao lưu vui vẻ | Người già yếu chân tay khó tự đi lại, phụ thuộc thời tiết | Tập an toàn ngay tại phòng khách gia đình |
| App thể dục quốc tế (Freeletics...) | Giao diện hiện đại, tính năng nhiều | Tiếng Anh, bài tập nặng cho thanh niên, phí đắt (>150k/tháng) | Bản địa hóa 100% tiếng Việt, tối ưu động tác nhẹ nhàng cho người già |


# CHƯƠNG 3: MÔ HÌNH KINH DOANH & NGUYÊN MẪU MVP (CHECKPOINT 3)

[Thành viên phụ trách biên soạn: Nguyễn Hải Hà (Mục 3.2, 3.3) & Nguyễn Nhã Quân (Mục 3.4)]


## 3.1. Khung Mô hình Kinh doanh 9 Khối (Business Model Canvas)

Mô hình kinh doanh của MotionIQ được tối ưu hóa theo 9 khối chuẩn Osterwalder, phù hợp với năng lực triển khai thực tế của dự án sinh viên:
1. Khách hàng mục tiêu (Customer Segments): Con cái 25–40 tuổi quan tâm đến cha mẹ; Người cao tuổi có nhu cầu vận động tại nhà.
2. Tuyên ngôn giá trị (Value Propositions): Hỗ trợ tập luyện vận động dễ dàng tại nhà; Chi phí hợp lý (49.000 – 79.000 VNĐ/tháng); Bảo mật hình ảnh với On-Device AI; Giao diện thân thiện tối đa với người già.
3. Kênh phân phối (Channels): Mạng xã hội (TikTok, Facebook Fanpage); Zalo; Giới thiệu trực tiếp qua các câu lạc bộ người cao tuổi địa phương.
4. Quan hệ khách hàng (Customer Relationships): Linh vật Bé Nấm tạo cảm giác thân thiết; Hệ thống nhắc nhở tập luyện đều đặn; Hỗ trợ kỹ thuật qua Zalo.
5. Dòng doanh thu (Revenue Streams): Mô hình Freemium (bài tập cơ bản miễn phí) + Thuê bao gói Early Access (49.000 đ/tháng) và gói Tiêu chuẩn (79.000 đ/tháng).
6. Hoạt động cốt lõi (Key Activities): Nâng cấp thuật toán nhận diện tư thế; Thiết kế trải nghiệm Geriatric UI; Sản xuất nội dung truyền thông mạng xã hội; Hỗ trợ khách hàng dùng thử.
7. Nguồn lực cốt lõi (Key Resources): Mã nguồn ứng dụng web/mobile; Thuật toán lọc nhiễu One-Euro Filter; Đội ngũ sinh viên đa ngành; Bộ nhận diện Bé Nấm.
8. Đối tác chính (Key Partners): Câu lạc bộ hưu trí, hội người cao tuổi địa phương; Giảng viên hướng dẫn môn học; Các cộng đồng chăm sóc gia đình trên mạng xã hội.
9. Cơ cấu chi phí (Cost Structure): Chi phí máy chủ lưu trữ nhẹ; Chi phí quảng cáo Facebook/TikTok có chọn lọc; Chi phí in ấn tài liệu QR Code giới thiệu.


## 3.2. Kiến trúc giải pháp kỹ thuật & Thuật toán 100% On-Device AI

• Xử lý thị giác thời gian thực trên thiết bị: Ứng dụng tích hợp MediaPipe BlazePose tối ưu bằng WebAssembly, phát hiện 33 điểm mốc chuyển động cơ thể với tốc độ 25 - 30 khung hình/giây (FPS) ngay trên trình duyệt di động hoặc laptop mà không cần máy chủ GPU đắt tiền.
• Bộ lọc khử rung One-Euro Filter: Người cao tuổi thường có độ run tay chân nhất định khi vận động chậm. Thuật toán One-Euro Filter tự động thích ứng để khử rung ở tốc độ thấp nhưng không gây trễ ở tốc độ cao, giúp các chỉ số góc khớp hiển thị mượt mà, chính xác.
• Bảo vệ quyền riêng tư người dùng: Mọi khung hình từ camera điện thoại chỉ được xử lý tạm thời trên bộ nhớ RAM của thiết bị và lập tức hủy bỏ sau khi trích xuất góc. Không có bất kỳ hình ảnh riêng tư nào được lưu trữ hoặc tải lên máy chủ.

## 3.3. 4 Bài tập vận động chức năng chuẩn hóa

Dựa trên các bài tập chuyển động chức năng phổ biến trong các bộ dữ liệu công khai (UI-PRMD và KIMORE), MotionIQ tích hợp 4 bài tập cơ bản, an toàn cho người già:
1. Bài Sit-to-Stand (Ngồi xuống - Đứng lên — UI-PRMD m05): Đo góc gập gối (90° - 125°), hỗ trợ cơ đùi và khả năng đứng lên độc lập.
2. Bài Squat chức năng (UI-PRMD m01): Kiểm tra trục đầu gối và giữ lưng thẳng, tăng cường sức mạnh cơ chi dưới.
3. Bài Shoulder Abduction (Dạng khớp vai — UI-PRMD m04): Đo góc dạng cánh tay (0° - 180°), giúp dẻo dai khớp vai và vùng tay trên.
4. Bài Side Leg Raise (Nâng chân sang bên — KIMORE): Hỗ trợ nhóm cơ giữ thăng bằng chống chới với khi đi lại.


## 3.4. Kết quả 5 buổi thử nghiệm nguyên mẫu MVP thực tế


| Chỉ số đo lường thực nghiệm | Kết quả thực tế | Ghi chú đánh giá |
| --- | --- | --- |
| Độ chính xác đo góc vận động (ROM) | 94.6% | So sánh với góc đo đối chiếu chuẩn |
| Độ trễ phản hồi thuật toán (Latency) | 38 ms / frame | Đạt chuẩn thời gian thực, âm thanh đếm nhịp không bị chậm |
| Điểm đánh giá khả dụng hệ thống SUS | 84.5 / 100 điểm | Người lớn tuổi thao tác thuận tiện, hài lòng với giao diện |


# CHƯƠNG 4: KẾ HOẠCH TRUYỀN THÔNG & PHÁT TRIỂN DOANH THU

[Thành viên phụ trách biên soạn chính: Mã Phú Tín — Growth & Media]


## 4.1. Mục tiêu truyền thông trong 04 tháng

Trong 04 tháng triển khai, nhóm tập trung xây dựng nhận diện thương hiệu MotionIQ, tiếp cận khách hàng tiềm năng, thúc đẩy trải nghiệm sản phẩm và chuyển đổi người dùng thành khách hàng trả phí. Do MotionIQ là dự án sinh viên, nhóm ưu tiên các hoạt động truyền thông trực tuyến, tận dụng nguồn lực sẵn có và triển khai quảng cáo có chọn lọc nhằm tối ưu ngân sách.

Các mục tiêu cụ thể:
• Xây dựng hình ảnh thương hiệu MotionIQ trên các nền tảng mạng xã hội.
• Tiếp cận nhóm khách hàng có nhu cầu hỗ trợ cha mẹ, người thân tập luyện tại nhà.
• Thu hút khách hàng tham gia trải nghiệm và đóng góp ý kiến hoàn thiện sản phẩm.
• Hình thành nhóm khách hàng trả phí đầu tiên và tạo doanh thu từ dịch vụ.


## 4.2. Khách hàng mục tiêu & Thông điệp truyền thông

• Khách hàng mục tiêu chính: Con/cháu trong độ tuổi 25–40, có khả năng sử dụng smartphone và quan tâm đến việc hỗ trợ, theo dõi quá trình tập luyện của cha mẹ tại nhà.
• Người sử dụng trực tiếp: Người cao tuổi có nhu cầu tập luyện vận động, ưu tiên sản phẩm dễ thao tác, giao diện đơn giản và hướng dẫn rõ ràng.
• Định vị truyền thông: MotionIQ là nền tảng AI hỗ trợ theo dõi vận động tại nhà thông qua camera smartphone, giúp nhận diện tư thế, đếm số lần tập và đưa ra phản hồi cơ bản.
• Thông điệp chính: 'MotionIQ – Tập luyện tại nhà, theo dõi chuyển động dễ dàng hơn.'

## 4.3. Kênh và Phương thức truyền thông


| Kênh truyền thông | Phương thức triển khai thực tế |
| --- | --- |
| TikTok | Sản xuất video ngắn giới thiệu sản phẩm, các tình huống đời thường trong gia đình và demo tính năng đếm nhịp bằng AI. |
| Facebook | Xây dựng Fanpage, đăng bài chia sẻ kiến thức vận động tuổi già, thông tin sản phẩm và phản hồi của người dùng trải nghiệm. |
| Zalo | Tư vấn 1:1, gửi video hướng dẫn sử dụng, chăm sóc khách hàng và hỗ trợ đăng ký gói trải nghiệm. |
| Trực tiếp (Cộng đồng) | Giới thiệu sản phẩm, tổ chức các buổi trải nghiệm tại câu lạc bộ người cao tuổi và hội đồng hương địa phương. |


## 4.4. Lộ trình triển khai truyền thông trong 04 tháng


| Thời gian triển khai | Hoạt động chính | Mục tiêu đạt được |
| --- | --- | --- |
| Tháng 1: Xây dựng nhận diện | Hoàn thiện Fanpage, kênh TikTok, bộ nhận diện Bé Nấm; sản xuất video giới thiệu và đăng tải nội dung cơ bản. | Tạo nhận diện thương hiệu ban đầu và giúp khách hàng biết đến MotionIQ. |
| Tháng 2: Tiếp cận khách hàng | Đăng video tính năng, chia sẻ vấn đề tập luyện tại nhà, quảng bá trên mạng xã hội và thu thập đăng ký trải nghiệm. | Tăng độ tiếp cận, thu hút 150–180 khách hàng tiềm năng. |
| Tháng 3: Trải nghiệm & Niềm tin | Tổ chức trải nghiệm miễn phí, hướng dẫn sử dụng, thu thập phản hồi, đăng video demo thực tế và khảo sát mức giá. | Chứng minh giá trị sản phẩm, tạo dựng sự tin tưởng cho 40–50 người dùng. |
| Tháng 4: Chuyển đổi & Doanh thu | Ra mắt gói dịch vụ trả phí, tư vấn gói ưu đãi, chăm sóc khách hàng và triển khai chương trình giới thiệu người dùng mới. | Chuyển đổi 15–20 khách hàng trả phí đầu tiên, tạo dòng tiền thực tế. |


## 4.5. Chiến lược định giá (Pricing Strategy)

MotionIQ áp dụng phương pháp định giá dựa trên giá trị khách hàng (Customer Value-Based Pricing) kết hợp định giá theo đối thủ cạnh tranh (Competition-Based Pricing), đồng thời sử dụng định giá dựa trên chi phí (Cost-Based Pricing) để đánh giá khả năng hòa vốn:

• Dựa trên khách hàng: Theo khảo sát ban đầu trên 50 đối tượng, có tới 64.7% phản hồi chấp nhận khoảng giá 50.000 – 149.000 VNĐ/tháng. Nhóm đề xuất mức phí dưới 100.000 VNĐ/tháng, phù hợp với định hướng tiếp cận con cháu có nhu cầu chăm sóc cha mẹ lớn tuổi.
• Dựa trên đối thủ: Kênh YouTube cung cấp video miễn phí nhưng không phản hồi trực tiếp theo chuyển động người xem. Kỹ thuật viên/huấn luyện viên đến nhà có thể hướng dẫn chuyên sâu nhưng phát sinh chi phí rất cao theo từng buổi (200.000 – 400.000 đ/buổi). MotionIQ kết hợp sự tiện lợi, phản hồi tự động bằng AI và mức phí cực kỳ dễ tiếp cận.
• Dựa trên chi phí: Giá bán đảm bảo khả năng bù đắp chi phí vận hành máy chủ và hướng đến lợi nhuận khi số lượng thuê bao tăng trưởng.

Bảng cơ cấu giá dịch vụ dự kiến của MotionIQ:


| Gói dịch vụ | Giá bán niêm yết | Đặc quyền & Quyền lợi sử dụng |
| --- | --- | --- |
| MotionIQ Free | Miễn phí | Trải nghiệm bài tập cơ bản, đếm số lần tập bằng AI |
| MotionIQ Early Access | 49.000 VNĐ / tháng | Áp dụng cho 20 khách hàng đầu tiên, mở khóa bài tập nâng cao |
| MotionIQ Standard | 79.000 VNĐ / tháng | Đầy đủ bài tập mở rộng, lưu lịch sử, báo cáo tiến độ tuần |
| MotionIQ Annual | 790.000 VNĐ / năm | Tiết kiệm 2 tháng phí thuê bao, hỗ trợ kỹ thuật ưu tiên |


## 4.6. Dự toán ngân sách và chi phí vận hành

Để hiện thực hóa kế hoạch tiếp cận thị trường trong 04 tháng, nhóm dự toán ngân sách truyền thông sinh viên tinh gọn 10.000.000 VNĐ kết hợp phân tích chi phí vận hành hệ thống:


| Hạng mục ngân sách truyền thông 04 tháng | Chi phí dự kiến (VNĐ) |
| --- | --- |
| Sản xuất nội dung truyền thông (hình ảnh, video) | 3.000.000 VNĐ |
| Quảng cáo chọn lọc trên Facebook và TikTok | 3.000.000 VNĐ |
| Tổ chức hoạt động trải nghiệm sản phẩm trực tiếp | 2.000.000 VNĐ |
| Chi phí đi lại và liên hệ khách hàng | 700.000 VNĐ |
| In ấn mã QR Code và tài liệu giới thiệu | 300.000 VNĐ |
| Chi phí dự phòng phát sinh | 1.000.000 VNĐ |
| TỔNG CỘNG NGÂN SÁCH TRUYỀN THÔNG | 10.000.000 VNĐ |

Về chi phí vận hành (Operating Cost):
Ngoài ngân sách truyền thông, MotionIQ cần tính đến chi phí duy trì website, bảo trì hệ thống, hỗ trợ khách hàng và thanh toán trực tuyến. Do chưa có dữ liệu vận hành thương mại quy mô lớn, nhóm xây dựng kịch bản chi phí giả định để phân tích tài chính:
• Chi phí cố định (Fixed Cost - FC): 1.000.000 VNĐ/tháng (duy trì hosting đám mây nhẹ, máy chủ cơ sở dữ liệu, tên miền và công cụ kỹ thuật).
• Chi phí biến đổi (Variable Cost - VC): 10.000 VNĐ/thuê bao/tháng (phí cổng thanh toán trực tuyến PayOS/Momo, phí gửi tin nhắn Zalo thông báo và băng thông phát sinh).


## 4.7. Kế hoạch phát triển doanh thu & Chỉ tiêu KPIs sau 04 tháng

MotionIQ áp dụng mô hình Freemium kết hợp Thuê bao định kỳ (Subscription), cho phép khách hàng trải nghiệm miễn phí tính năng cốt lõi trước khi quyết định nâng cấp lên gói trả phí.

Chiến lược phễu chuyển đổi 5 bước (Conversion Funnel):
1. Tiếp cận (Reach): Sử dụng Facebook, TikTok và cộng đồng chăm sóc người cao tuổi để giới thiệu sản phẩm.
2. Quan tâm (Interest): Thực hiện video minh họa tình huống đời thường và demo khả năng nhận diện chuyển động bằng AI.
3. Dùng thử (Trial): Hướng dẫn khách hàng trải nghiệm ứng dụng miễn phí, hỗ trợ trực tiếp hoặc qua Zalo.
4. Trả phí (Conversion): Giới thiệu gói Early Access 49.000 VNĐ/tháng, làm nổi bật các đặc quyền hỗ trợ riêng.
5. Duy trì (Retention): Hỗ trợ kỹ thuật kịp thời, thu thập ý kiến đóng góp và cải thiện trải nghiệm để người dùng gia hạn thuê bao.


| Chỉ tiêu đo lường hiệu quả | Mục tiêu sau 04 tháng | Ý nghĩa đánh giá |
| --- | --- | --- |
| Lượt tiếp cận mạng xã hội (Reach) | 13.000 – 15.000 lượt | Xây dựng độ nhận diện thương hiệu ban đầu |
| Khách hàng tiềm năng (Leads) | 150 – 180 khách hàng | Tỷ lệ chuyển đổi đạt ~1.1% – 1.2% từ Reach |
| Người đăng ký trải nghiệm dùng thử | 40 – 50 người | Tỷ lệ chuyển đổi đạt ~27% từ nhóm Leads |
| Người hoàn thành trọn vẹn quy trình | 30 – 35 người | Tỷ lệ hoàn thành đạt ~70% – 75% người dùng thử |
| Khách hàng chuyển đổi sang trả phí | 15 – 20 khách hàng | Tỷ lệ chuyển đổi đạt ~50% người hoàn thành |

Đánh giá chi phí thu hút khách hàng (CAC):
Với tổng ngân sách truyền thông 10.000.000 VNĐ và mục tiêu 15–20 khách hàng trả phí đầu tiên, chi phí marketing phân bổ bình quân tương đương khoảng 500.000 – 666.667 VNĐ/khách hàng. Đây là mức đầu tư ban đầu hợp lý cho giai đoạn kiểm chứng sản phẩm (Validation Phase), khi chi phí marketing đồng thời đóng vai trò xây dựng nhận diện thương hiệu và tạo dựng tệp khách hàng tiềm năng cho các giai đoạn tiếp theo.


## 4.8. Dự báo doanh thu và Phân tích điểm hòa vốn

Dự báo doanh thu ban đầu từ nhóm khách hàng sử dụng gói Early Access (49.000 VNĐ/tháng):


| Số lượng khách hàng trả phí | Doanh thu tháng dự kiến (Gói 49.000 đ) |
| --- | --- |
| 10 khách hàng | 490.000 VNĐ / tháng |
| 15 khách hàng | 735.000 VNĐ / tháng |
| 20 khách hàng | 980.000 VNĐ / tháng |

Với mục tiêu 15–20 khách hàng trả phí vào tháng thứ tư, MotionIQ dự kiến tạo ra 735.000 – 980.000 VNĐ doanh thu định kỳ hằng tháng (MRR) từ gói Early Access. Mức doanh thu này đã tiệm cận mức bù đắp chi phí vận hành máy chủ hàng tháng (1.000.000 VNĐ).

Phân tích điểm hòa vốn (Break-Even Analysis):
Điểm hòa vốn được xác định theo công thức chuẩn tài chính:
Số lượng thuê bao hòa vốn = Chi phí cố định / (Giá bán − Chi phí biến đổi trên mỗi thuê bao)

Với giả định Chi phí cố định (FC) = 1.000.000 VNĐ/tháng và Chi phí biến đổi (VC) = 10.000 VNĐ/thuê bao/tháng:


| Chỉ tiêu phân tích hòa vốn | Gói Early Access (49.000đ) | Gói Standard (79.000đ) |
| --- | --- | --- |
| Doanh thu còn lại sau chi phí biến đổi / khách (P - VC) | 39.000 VNĐ | 69.000 VNĐ |
| Số lượng khách hòa vốn vận hành hàng tháng (FC = 1.000.000đ) | 26 khách hàng | 15 khách hàng |
| Hòa vốn khi phân bổ ngân sách marketing 10 triệu trong 4 tháng | 90 khách hàng / tháng | 51 khách hàng / tháng |

Nhận định tài chính từ nhóm thực hiện:
Kết quả phân tích cho thấy, với mục tiêu ban đầu là 15–20 khách hàng trả phí ở tháng thứ tư, MotionIQ chưa thể thu hồi toàn bộ 10 triệu đồng chi phí marketing ban đầu. Điều này hoàn toàn phù hợp với quy luật thực tế của một dự án công nghệ khởi nghiệp giai đoạn đầu (Early Stage): Ngân sách 10 triệu đóng vai trò vốn đầu tư tạo dựng nhận diện thương hiệu và kiểm chứng sản phẩm.

Tuy nhiên, ở góc độ chi phí vận hành thường xuyên, chỉ cần đạt mốc 26 khách hàng gói Early Access (hoặc 15 khách hàng gói Standard), dự án đã hoàn toàn tự chủ tài chính vận hành (Operational Self-Sufficiency) mà không cần bù lỗ chi phí máy chủ hàng tháng. Đây là cơ sở vững chắc để nhóm từng bước mở rộng quy mô một cách bền vững.


| 📌 ĐIỂM NHẤN CHIẾN LƯỢC TÀI CHÍNH & KHẢ NĂNG TỰ CHỦ VẬN HÀNH • Bản chất chỉ số CAC vs. LTV: Chỉ số CAC ban đầu (500.000 – 666.667 VNĐ) phản ánh chi phí đầu tư thương hiệu tiếp cận 13.000 – 15.000 lượt người dùng. Với mô hình thuê bao định kỳ, Giá trị vòng đời khách hàng (LTV) đạt 588.000 – 790.000 VNĐ khi duy trì từ 12 tháng trở lên, đảm bảo LTV > CAC và mang lại lợi nhuận bền vững. • Ý nghĩa điểm hòa vốn vận hành: Mốc 26 khách hàng gói Early Access (hoặc 15 khách hàng gói Standard) là bằng chứng sống còn của dự án. Sau 04 tháng, dòng tiền định kỳ MRR xấp xỉ 1.000.000 VNĐ/tháng sẽ tự trang trải 100% chi phí hạ tầng máy chủ mà nhóm không phải bỏ tiền túi bù lỗ. |
| --- |


# CHƯƠNG 5: QUẢN TRỊ RỦI RO & DUY TRÌ BỀN VỮNG

[Thành viên phụ trách biên soạn chính: Hồ Tuyết Nghi — CMO]


## 5.1. Nhận diện rủi ro thực tế & Biện pháp giảm thiểu

Để đảm bảo dự án vận hành an toàn, minh bạch và đúng khuôn khổ pháp luật, nhóm nhận diện 7 rủi ro chính và đề xuất biện pháp xử lý cụ thể:


| Rủi ro nhận diện | Biện pháp giảm thiểu thực tế |
| --- | --- |
| Người cao tuổi khó sử dụng công nghệ | Giao diện đơn giản, chữ lớn, nút bấm dễ thao tác; giọng nói tiếng Việt rõ ràng, âm lượng lớn, có thể điều chỉnh và lặp lại hướng dẫn. |
| AI nhận diện chuyển động chưa chính xác | Tiếp tục thử nghiệm thực tế, áp dụng bộ lọc One-Euro Filter khử rung và hướng dẫn vị trí đặt camera chuẩn. |
| Khách hàng không sẵn sàng trả phí | Cung cấp bản dùng thử miễn phí, minh bạch quyền lợi bổ sung của gói trả phí và kiểm chứng mức giá hợp lý (49.000 đ). |
| Chi phí thu hút khách hàng (CAC) cao | Theo dõi sát chỉ số CAC, tập trung vào các kênh truyền thông có tỷ lệ chuyển đổi tốt và tối ưu hóa nội dung video ngắn. |
| Khách hàng ngừng sử dụng sau thời gian ngắn | Cải thiện trải nghiệm Geriatric UX, chăm sóc người dùng chu đáo và bổ sung chức năng tích điểm ngày tập (Streak). |
| Rủi ro phân loại ứng dụng hỗ trợ | Tuyên bố minh bạch MotionIQ là ứng dụng công nghệ hỗ trợ tập luyện vận động thể chất tại nhà, hoàn toàn không phải công cụ chẩn đoán chuyên sâu và không thay thế bác sĩ hoặc chuyên viên phục hồi chức năng. |
| Rủi ro bảo vệ dữ liệu cá nhân | Kiến trúc 100% On-Device AI xử lý tạm thời trên RAM rồi hủy ngay, không lưu trữ và không gửi hình ảnh cá nhân lên máy chủ. |


## 5.2. Kế hoạch duy trì và phát triển theo từng giai đoạn

Dự án được định hướng phát triển bài bản qua 3 giai đoạn cụ thể:

1. Giai đoạn 04 tháng đầu tiên (Kiểm chứng & Khởi động):
• Hoàn thiện nguyên mẫu MVP và nâng cao trải nghiệm người cao tuổi.
• Thu hút 40–50 hộ gia đình đăng ký tham gia dùng thử.
• Kiểm chứng sự sẵn sàng chi trả với gói Early Access 49.000 VNĐ/tháng.
• Đạt mốc 15–20 khách hàng trả phí đầu tiên, tạo dòng tiền thực tế.

2. Giai đoạn Tháng 5 – Tháng 6 (Ổn định & Tối ưu hóa):
• Cải thiện khả năng nhận diện chuyển động và chất lượng giọng nói hướng dẫn.
• Đánh giá tỷ lệ duy trì thuê bao (Retention Rate) của nhóm khách hàng trả phí.
• Kiểm chứng khả năng nâng cấp lên gói Standard 79.000 VNĐ/tháng.
• Cập nhật số liệu chi phí thực tế và lộ trình hòa vốn toàn phần.

3. Giai đoạn Mở rộng tiếp theo:
• Bổ sung thêm các bài tập vận động phù hợp cho cổ tay và cổ chân.
• Nâng cấp chức năng theo dõi tiến độ và báo cáo tuần gửi tự động cho con cái qua Zalo.
• Nghiên cứu tích hợp Zalo Mini App để người dùng mở ứng dụng trực tiếp không cần cài đặt.
• Xem xét mở rộng mô hình B2B sang các cơ sở chăm sóc người cao tuổi khi sản phẩm đáp ứng đầy đủ yêu cầu chuyên môn và pháp lý.


# KẾT LUẬN

[Thành viên phụ trách biên soạn: Huỳnh Thị Yến Duy — CEO (Trưởng nhóm)]

Kế hoạch của dự án MotionIQ tập trung vào việc giải quyết bài toán thực tế của các gia đình có người cao tuổi: Giúp cha mẹ duy trì thói quen tập luyện vận động dễ dàng hơn và giúp con cái an tâm hơn dù bận rộn công việc.

Bằng cách tiếp cận trung thực, khiêm tốn nhưng bài bản, dựa trên kết quả khảo sát thực tế 50 đối tượng và kế hoạch truyền thông 04 tháng với ngân sách tinh gọn 10.000.000 VNĐ, MotionIQ hướng đến mục tiêu chứng minh giá trị sản phẩm từ trải nghiệm người dùng thực, hình thành nhóm khách hàng trung thành ban đầu và từng bước xây dựng một dự án khởi nghiệp sinh viên bền vững, giàu tính nhân văn.
