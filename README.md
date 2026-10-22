# MotionIQ — AI Elderly Home Exercise & Rehabilitation Platform 🏃‍♂️

> **Nền tảng hỗ trợ tập vận động và phục hồi chức năng tại nhà cho người cao tuổi bằng Trí tuệ Nhân tạo (Edge AI Pose Estimation).**

[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Privacy-First](https://img.shields.io/badge/Privacy-100%25%20On--Device-success?style=flat-square)](#)
[![Datasets](https://img.shields.io/badge/Clinical%20Datasets-EHE%20%7C%20KIMORE%20%7C%20UI--PRMD-orange?style=flat-square)](#)

---

## 📌 Điểm nổi bật (Core Highlights)

- 🔒 **Bảo mật tuyệt đối (100% On-Device AI)**: Phân tích tư thế chạy hoàn toàn trên trình duyệt thông qua WebAssembly & WebGL. **Không gửi bất kỳ hình ảnh hay video nào lên server.**
- 🔬 **Chuẩn hóa Động học Y sinh theo 3 Dataset Công khai**:
  1. **EHE (Elderly Home Exercise)**: 869 lần lặp từ 25 người cao tuổi (Kinect v2), tránh thiên vị dữ liệu người trẻ.
  2. **KIMORE (Clinical Benchmark)**: 78 đối tượng (người khỏe mạnh & rối loạn vận động) có điểm đánh giá lâm sàng.
  3. **UI-PRMD (Rehabilitation Dataset)**: 10 bài tập phục hồi chức năng chuẩn PDDL 1.0 với cặp chuyển động đúng/sai đối sánh.
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

## 🏋️‍♂️ Danh mục Bài tập Chuẩn hóa

| Bài tập | Mã ID | Nguồn Dataset tương ứng | Nhóm vận động & Tiêu chí lâm sàng |
| :--- | :--- | :--- | :--- |
| **Đứng lên – Ngồi xuống** | `sit-to-stand` | **UI-PRMD** *(m05)* & **KIMORE** *(Es4)* | Tăng cường cơ tứ đầu đùi, cải thiện chức năng chi dưới và thăng bằng |
| **Squat** | `squat` | **UI-PRMD** *(m01)*, **KIMORE** *(Es5)* & **EHE** | Tăng sức mạnh cơ mông và đùi; kiểm soát góc gập gối (90°–125°) |
| **Nâng tay** | `shoulder-raise` | **EHE** *(LA)*, **KIMORE** *(Es1)* & **UI-PRMD** *(m07)* | Mở rộng tầm vận động khớp vai (ROM) chi trên, hỗ trợ tư thế cột sống ngực |
| **Giạng chân sang bên** | `side-leg-raise` | **UI-PRMD** *(m06 - Active Straight Leg Raise)* | Tăng cường cơ mông nhỡ (gluteus medius), chống té ngã khi đi lại |

*(Lưu ý: Các bài tập không thuộc 3 dataset trên như bài Nhón gót chân - `calf-raise` đã được loại bỏ hoàn toàn khỏi hệ thống).*

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
- Dữ liệu nghiên cứu EHE tuân thủ giấy phép CC BY-NC 4.0; KIMORE & UI-PRMD phục vụ nghiên cứu và đánh giá chuyển động phục hồi chức năng.
