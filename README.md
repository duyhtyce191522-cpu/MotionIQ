# MotionIQ — AI Elderly Home Exercise & Rehabilitation Platform 🏃‍♂️

> **Nền tảng hỗ trợ tập vận động và phục hồi chức năng tại nhà cho người cao tuổi bằng Trí tuệ Nhân tạo (Edge AI Pose Estimation).**

[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Privacy-First](https://img.shields.io/badge/Privacy-100%25%20On--Device-success?style=flat-square)](#)
[![Dataset](https://img.shields.io/badge/Movement%20Model-UI--PRMD-orange?style=flat-square)](#)

---

## 📌 Điểm nổi bật (Core Highlights)

- 🔒 **Bảo mật tuyệt đối (100% On-Device AI)**: Phân tích tư thế chạy hoàn toàn trên trình duyệt thông qua WebAssembly & WebGL. **Không gửi bất kỳ hình ảnh hay video nào lên server.**
- 🔬 **Model UI-PRMD chuyên biệt**: model chất lượng động tác được huấn luyện riêng cho bốn chuyển động phục hồi chức năng trong danh mục bên dưới, dùng cặp dữ liệu đúng/sai đối sánh.
- ⚡ **Pose Estimation thời gian thực (Zero-Latency)**: Kiến trúc YOLOv8/v11-Pose kết hợp bộ lọc thích ứng tần số **One-Euro Filter** khử rung vi chuyển động, tốc độ đạt 30–60 FPS ngay trên máy tính/điện thoại phổ thông.
- 👵 **Thiết kế thân thiện cho Người cao tuổi (Elderly-Centric UI/UX)**:
  - Giao diện sáng dịu, độ tương phản cao đạt chuẩn WCAG AAA.
  - Cỡ chữ lớn $\ge 18\text{px}$, nút bấm cảm ứng lớn $\ge 48\text{px}$.
  - Trợ lý đếm nhịp và hướng dẫn tư thế bằng **Giọng nói tiếng Việt tự nhiên**.
  - Hiển thị góc khớp động (Live Angle Badge) trực tiếp trên khớp gối/vai/hông.
- 🏥 **Hệ thống Phân quyền Kép (Dual-Flow Auth)**:
  - **Người cao tuổi**: Đăng nhập 1-chạm qua Avatar trực quan (👴/👵), tự động hiển thị bài tập chỉ định có biểu tượng ⭐.
  - **Bác sĩ / KTV**: Đăng nhập Admin bảo mật, chỉ định bài tập cá nhân hóa, đặt mục tiêu số lần tập/ngày và theo dõi tiến độ hồi phục.
- 🖨️ **Xuất Báo cáo Y tế (Medical Kinematics Report)**: Tích hợp sẵn tính năng xuất báo cáo lâm sàng chuẩn A4 và file PDF tổng kết y sinh.

---

## 🏋️‍♂️ Bốn bài tập UI-PRMD được hỗ trợ

| Bài tập | Mã ID | Nguồn Dataset tương ứng | Nhóm vận động & Tiêu chí lâm sàng |
| :--- | :--- | :--- | :--- |
| **Đứng lên – Ngồi xuống** | `sit-to-stand` | **UI-PRMD** *(m05)* | Tăng cường cơ tứ đầu đùi, cải thiện chức năng chi dưới và thăng bằng |
| **Squat sâu** | `squat` | **UI-PRMD** *(m01)* | Tăng sức mạnh cơ mông và đùi; kiểm soát góc gập gối |
| **Dạng vai khi đứng** | `shoulder-raise` | **UI-PRMD** *(m07 - Standing Shoulder Abduction)* | Mở rộng tầm vận động khớp vai và cánh tay |
| **Nâng chân thẳng khi đứng** | `side-leg-raise` | **UI-PRMD** *(m06 - Standing Active Straight Leg Raise)* | Luyện vận động gập hông có kiểm soát và giữ gối thẳng |

### Model tham khảo chất lượng động tác UI-PRMD

MotionIQ chỉ huấn luyện model đánh giá chất lượng trên bốn động tác `squat` (m01), `side-leg-raise` (m06), `sit-to-stand` (m05) và `shoulder-raise` (m07). Model dùng 22 khớp Kinect trong dữ liệu UI-PRMD (vị trí và góc xoay theo từng frame), sau đó chạy dự đoán cục bộ trên chuỗi khớp MediaPipe của mỗi lần tập. Bộ phát hiện pose MediaPipe không được huấn luyện lại.

Nếu dữ liệu m06 chưa có trong thư mục `scripts/uiprmd/data`, tải bổ sung các file thuộc bốn động tác được hỗ trợ rồi huấn luyện lại bằng:

```bash
python scripts/uiprmd/fetch_uiprmd.py
node scripts/uiprmd/train_quality_model.mjs
```

Lệnh huấn luyện tách riêng chủ thể 9 và 10 để kiểm tra nội bộ (40 lần tập cho mỗi bài). Kết quả hiện tại: squat 72.5%, nâng chân thẳng 97.5%, đứng lên–ngồi xuống 95% và dạng vai 97.5%. Đây chỉ là kết quả trên tập kiểm tra nhỏ, không phải xác nhận lâm sàng. Giao diện chỉ hiển thị điểm tham khảo sau mỗi lần tập; điểm này không thay thế hướng dẫn của bác sĩ và không được dùng làm chức năng an toàn.

Trước mỗi buổi tập, camera cần nhận diện toàn thân và tư thế xuất phát đúng của bài tập. Trợ lý tiếng Việt hướng dẫn vào tư thế, đếm ngược trước khi bắt đầu và đọc số lần hoàn thành.

Ảnh minh họa logo và các động tác được lưu tại `public/images/` (`motioniq-logo.png`, `sit-to-stand.png`, `squat.png`, `shoulder-raise.png`, `side-leg-raise.png`).

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript 5
- **Styling**: Vanilla CSS, Modern Design System, CSS Keyframe Animations (Glassmorphism & High Contrast)
- **AI & Pose Estimation**: YOLOv8/v11-Pose Pipeline, MediaPipe Vision Tasks
- **Xử lý tín hiệu**: One-Euro Smoothing Filter, Repetition State Machine with Hysteresis
- **Voice & Audio**: Web Speech Synthesis API (Vietnamese), Web Audio API
- **Tài liệu & Báo cáo**: [Báo cáo Tổng kết Dự án MotionIQ PDF](./Bao_Cao_Tong_Ket_MotionIQ.pdf)

---

## 🚀 Cài đặt & Khởi chạy (Getting Started)

### 1. Yêu cầu hệ thống
- **Node.js**: Phiên bản 18.17 trở lên
- **Trình duyệt**: Chrome, Edge, Safari hoặc Firefox có hỗ trợ WebRTC & WebAssembly

### 2. Cài đặt thư viện
```bash
git clone https://github.com/duyhtyce191522-cpu/MotionIQ.git
cd MotionIQ
npm install
```

### 3. Khởi chạy môi trường phát triển
```bash
npm run dev
```
Mở trình duyệt và truy cập [http://localhost:3000](http://localhost:3000).

---

## 👥 Tài khoản mặc định

- **Người cao tuổi (Bệnh nhân)**: Nhấn trực tiếp vào thẻ đại diện (ví dụ: *👴 Bác Nguyễn Văn An*, *👵 Bà Trần Thị Mai*).
- **Quản trị viên / Bác sĩ**:
  - Tên đăng nhập: `admin`
  - Mật khẩu: `admin123`

---

## 📄 Bản quyền & Tài liệu
- Tài liệu báo cáo hoàn chỉnh dự án đã được đính kèm tại file [`Bao_Cao_Tong_Ket_MotionIQ.pdf`](./Bao_Cao_Tong_Ket_MotionIQ.pdf).
- UI-PRMD phục vụ nghiên cứu và đánh giá chuyển động phục hồi chức năng; kết quả model không phải xác nhận lâm sàng.
