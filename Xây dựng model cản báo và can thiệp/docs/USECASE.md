# 📋 Use Case Specification - Hệ thống Cảnh báo Sinh viên Yếu

## 👥 Actors (Người tham gia)

1. **Giáo viên/Cố vấn học tập** - Người dùng chính
2. **Quản lý khoa/Bộ phận** - Người quản lý
3. **Hệ thống ML** - Backend xử lý dự đoán

---

## 📌 Use Case 1: Dự đoán Sinh viên Yếu (Main Flow)

### 1.1 Thông tin chung
- **Tên**: Dự đoán sinh viên có nguy cơ học yếu
- **Actor chính**: Giáo viên/Cố vấn học tập
- **Tiền điều kiện**: 
  - Hệ thống đang chạy
  - Có file dữ liệu sinh viên (CSV/Excel)
- **Kết quả mong đợi**: Danh sách sinh viên với phân loại rủi ro

### 1.2 Quy trình (Happy Path)

#### **Bước 1: Mở ứng dụng**
```
Giáo viên:
├─ Mở trình duyệt web
├─ Nhập URL: http://localhost:8000/frontend/index.html
└─ → Giao diện web hiển thị thành công
    ├─ Tiêu đề: "🎓 Hệ thống Cảnh báo Sinh viên Yếu"
    ├─ Khung upload file
    ├─ Nút "Chọn file"
    └─ Nút "🔮 Dự đoán"
```

#### **Bước 2: Chuẩn bị dữ liệu**
```
Giáo viên:
├─ Tạo/Chuẩn bị file CSV hoặc Excel
│  └─ Định dạng cần có:
│     ├─ Cột 1: ma_sv (mã sinh viên) - String
│     ├─ Cột 2: ho_ten (tên) - String [Optional]
│     ├─ Cột 3: diem_qua_trinh (0-10) - Number
│     ├─ Cột 4: diem_giua_ky (0-10) - Number
│     └─ Cột 5: diem_cuoi_ky (0-10) - Number
│
├─ Ví dụ dữ liệu:
│  ┌──────────┬──────────────────┬────────┬───────────┬──────────┐
│  │ ma_sv    │ ho_ten           │ dqt    │ dgk       │ dck      │
│  ├──────────┼──────────────────┼────────┼───────────┼──────────┤
│  │ SV001    │ Nguyễn Văn A     │ 9.0    │ 8.5       │ 9.0      │
│  │ SV002    │ Trần Thị B       │ 4.0    │ 3.5       │ 3.8      │
│  │ SV003    │ Lê Văn C         │ 7.5    │ 7.8       │ 7.2      │
│  └──────────┴──────────────────┴────────┴───────────┴──────────┘
│
└─ Lưu file với tên: "diem_sinh_vien.csv"
```

#### **Bước 3: Upload file**
```
Giáo viên:
├─ Tùy chọn A: Kéo thả (Drag & Drop)
│  └─ Kéo file vào khung upload
│     └─ → File được chọn tự động
│
└─ Tùy chọn B: Click chọn file
   ├─ Click nút "Chọn file"
   ├─ Cửa sổ file browser mở
   ├─ Chọn file CSV/Excel
   └─ Click "Mở" → File được chọn
```

**Kết quả hiển thị:**
```
Giao diện frontend:
├─ Tên file: "diem_sinh_vien.csv"
├─ Kích thước: "45.2 KB"
└─ Trạng thái: "Sẵn sàng dự đoán"
```

#### **Bước 4: Chạy dự đoán**
```
Giáo viên:
├─ Click nút "🔮 Dự đoán"
│
Hệ thống (Backend):
├─ Nhận file từ frontend
├─ Validate dữ liệu:
│  ├─ Kiểm tra có đủ cột: ma_sv, diem_qua_trinh, diem_giua_ky, diem_cuoi_ky
│  ├─ Kiểm tra điểm số nằm trong khoảng 0-10
│  └─ Kiểm tra không có giá trị thiếu
│
├─ Chuẩn bị dữ liệu:
│  ├─ Trích xuất 3 cột điểm: [9.0, 8.5, 9.0]
│  └─ Convert thành feature vector
│
├─ Chạy mô hình Random Forest:
│  ├─ Input: [9.0, 8.5, 9.0]
│  ├─ Model.predict() → Output
│  └─ Kết quả: "Xuat_sac" (với confidence cao)
│
└─ Trả về JSON response
```

#### **Bước 5: Xem kết quả**
```
Frontend hiển thị:
├─ 📊 THỐNG KÊ (Cards)
│  ├─ Tổng sinh viên: 3
│  ├─ 🔴 Nguy cơ cao (Yếu): 1
│  ├─ 🟡 Trung bình: 1
│  └─ 🟢 An toàn (Xuất sắc + Khá): 1
│
├─ 📋 BẢNG CHI TIẾT
│  ┌──────────┬──────────────────┬──────────┬─────────────────────────────┐
│  │ Mã SV    │ Tên              │ Dự đoán  │ Mô tả                       │
│  ├──────────┼──────────────────┼──────────┼─────────────────────────────┤
│  │ SV001    │ Nguyễn Văn A     │ Xuất sắc │ ✅ An toàn - Xuất sắc       │
│  │ SV002    │ Trần Thị B       │ Yếu      │ ⚠️ Nguy cơ cao - Yếu        │
│  │ SV003    │ Lê Văn C         │ Khá      │ ✅ An toàn - Khá            │
│  └──────────┴──────────────────┴──────────┴─────────────────────────────┘
│
├─ 📥 Download kết quả
│  └─ Nút "Tải xuống CSV"
│     └─ File: "du_doan_[timestamp].csv"
│
└─ ↩️ Làm lại
   └─ Nút "Chọn file khác"
```

### 1.3 Alternative Flows (Nhánh xử lý)

#### **Alt 1: File không đúng định dạng**
```
Khi: Giáo viên upload file .txt hoặc .doc
Hệ thống:
├─ Kiểm tra extension
├─ Phát hiện không phải CSV/Excel
│
Phản hồi (Frontend):
├─ 🔴 Thông báo lỗi
├─ "❌ Lỗi: File phải là CSV hoặc Excel (.xlsx, .xls)"
└─ Gợi ý: "Vui lòng chọn file CSV hoặc Excel"
```

#### **Alt 2: File thiếu cột**
```
Khi: File CSV không có cột "diem_qua_trinh"
Hệ thống:
├─ Validate không thành công
│
Phản hồi (Frontend):
├─ 🔴 Thông báo lỗi
├─ "❌ Thiếu cột: diem_qua_trinh"
└─ Gợi ý: "File phải có cột: ma_sv, diem_qua_trinh, diem_giua_ky, diem_cuoi_ky"
```

#### **Alt 3: Giá trị điểm số không hợp lệ**
```
Khi: Cột diem_qua_trinh có giá trị âm (-5) hoặc > 10 (12)
Hệ thống:
├─ Validate khoảng giá trị
│
Phản hồi (Frontend):
├─ 🔴 Thông báo lỗi
├─ "❌ Cột 'diem_qua_trinh' phải có giá trị từ 0 đến 10"
└─ Gợi ý: "Kiểm tra lại dữ liệu"
```

#### **Alt 4: Delimiter mismatch (Dấu phân cách)**
```
Khi: File CSV dùng dấu ";" thay vì ","
File: ma_sv;ho_ten;diem_qua_trinh;...

Hệ thống:
├─ Thử các delimiter: [";", ",", "\t"]
├─ Phát hiện ";" là delimiter đúng
├─ Parse file thành công
│
Phản hồi: ✅ Xử lý bình thường
```

#### **Alt 5: Backend không hoạt động**
```
Khi: Giáo viên click dự đoán nhưng backend bị tắt
Hệ thống:
├─ Frontend gửi POST request
├─ Không nhận được response
│
Phản hồi (Frontend):
├─ 🔴 Thông báo lỗi
├─ "❌ Không thể kết nối đến server"
└─ Gợi ý: "Vui lòng kiểm tra xem backend có đang chạy không"
```

---

## 📌 Use Case 2: Download kết quả dự đoán

### 2.1 Thông tin chung
- **Tên**: Tải xuống kết quả dự đoán
- **Actor chính**: Giáo viên/Quản lý
- **Tiền điều kiện**: Đã chạy dự đoán thành công
- **Kết quả mong đợi**: File CSV chứa kết quả được lưu

### 2.2 Quy trình
```
Giáo viên:
├─ Sau khi xem kết quả dự đoán
├─ Click nút "📥 Tải xuống CSV"
│
Hệ thống:
├─ Tạo file CSV từ kết quả hiện tại
├─ Tên file: "du_doan_[timestamp].csv"
│  └─ Ví dụ: "du_doan_2025-12-12_14-30-45.csv"
│
├─ Nội dung file:
│  ┌──────────┬──────────────────┬──────────┬─────────────────────────────┐
│  │ ma_sv    │ ho_ten           │ du_doan  │ mo_ta                       │
│  ├──────────┼──────────────────┼──────────┼─────────────────────────────┤
│  │ SV001    │ Nguyễn Văn A     │ Xuất sắc │ An toàn - Xuất sắc          │
│  │ SV002    │ Trần Thị B       │ Yếu      │ Nguy cơ cao - Yếu           │
│  │ SV003    │ Lê Văn C         │ Khá      │ An toàn - Khá               │
│  └──────────┴──────────────────┴──────────┴─────────────────────────────┘
│
└─ Browser tự động tải file xuống
   └─ Đường dẫn: C:\Users\[User]\Downloads\du_doan_*.csv
```

---

## 📌 Use Case 3: Xem thông tin hệ thống

### 3.1 Mô tả
```
Actor: Quản lý hoặc người phát triển
├─ Muốn biết hệ thống đang chạy đúng không
├─ Muốn biết mô hình ML có những thông tin gì
│
Cách làm:
├─ Truy cập: http://localhost:8000/health
│  └─ Trả về: {"status": "healthy", "model_loaded": true}
│
└─ Truy cập: http://localhost:8000/model-info
   └─ Trả về: 
      {
        "model_type": "RandomForestClassifier",
        "n_estimators": 200,
        "max_depth": 10,
        "classes": ["Xuất sắc", "Khá", "Trung bình", "Yếu"],
        "features": ["diem_qua_trinh", "diem_giua_ky", "diem_cuoi_ky"]
      }
```

---

## 🎯 User Story (Tóm tắt dành cho lập trình viên)

### Story 1: Giáo viên muốn dự đoán sinh viên yếu
```
Là một giáo viên,
Tôi muốn upload file dữ liệu sinh viên,
Để có thể nhanh chóng xác định sinh viên có nguy cơ học yếu
Và có thời gian can thiệp sớm.

Tiêu chí chấp nhận:
✅ File CSV/Excel có thể upload thành công
✅ Kết quả dự đoán hiển thị trong < 2 giây
✅ Kết quả hiển thị: mã SV, tên, dự đoán, mô tả
✅ Có thể download kết quả dưới dạng CSV
✅ Thông báo lỗi rõ ràng nếu dữ liệu không hợp lệ
```

### Story 2: Quản lý muốn xem báo cáo tổng hợp
```
Là một quản lý khoa,
Tôi muốn xem thống kê tổng hợp sinh viên,
Để biết có bao nhiêu sinh viên cần can thiệp.

Tiêu chí chấp nhận:
✅ Hiển thị tổng số sinh viên
✅ Hiển thị số lượng theo từng mức độ rủi ro
✅ Hiển thị tỷ lệ phần trăm
✅ Tô màu khác nhau cho mỗi mức độ
```

### Story 3: Hỗ trợ file với tên sinh viên
```
Là một giáo viên,
Tôi muốn file upload có chứa cột tên sinh viên (ho_ten),
Để dễ dàng xác định từng sinh viên cần can thiệp.

Tiêu chí chấp nhận:
✅ Hệ thống tự động phát hiện cột ho_ten
✅ Nếu có cột ho_ten, hiển thị trong kết quả
✅ Nếu không có cột ho_ten, vẫn xử lý được
✅ Download CSV cũng bao gồm cột ho_ten (nếu có)
```

---

## 📊 Workflow Chi tiết (Sequence Diagram Text)

```
Giáo viên          Frontend          Backend         Model ML
   │                  │                  │               │
   │──(1) Mở page────>│                  │               │
   │                  │                  │               │
   │<──(2) HTML load──│                  │               │
   │                  │                  │               │
   │──(3) Upload file─>│                  │               │
   │                  │                  │               │
   │──(4) Click dự    │                  │               │
   │     đoán────────>│                  │               │
   │                  │──(5) POST request──>│            │
   │                  │                  │               │
   │                  │                  │──(6) Load model──>│
   │                  │                  │<──(7) Model ready─│
   │                  │                  │               │
   │                  │                  │──(8) Predict──>│
   │                  │                  │<─(9) Results──│
   │                  │                  │               │
   │                  │<──(10) Response──│               │
   │                  │                  │               │
   │<──(11) Display───│                  │               │
   │     results      │                  │               │
   │                  │                  │               │
   │──(12) Download───>│                  │               │
   │<──(13) CSV file──│                  │               │
   │                  │                  │               │
```

---

## 🔍 Data Flow

### Input Data
```
CSV/Excel File
├─ Encoding: UTF-8, Latin-1, CP1252 (tự detect)
├─ Delimiter: , ; \t (tự detect)
└─ Columns:
   ├─ ma_sv: "SV001", "SV002", ...
   ├─ ho_ten: "Nguyễn Văn A", "Trần Thị B" (optional)
   ├─ diem_qua_trinh: 9.0, 4.5, 7.2, ...
   ├─ diem_giua_ky: 8.5, 3.5, 7.8, ...
   └─ diem_cuoi_ky: 9.0, 3.8, 7.2, ...
```

### Processing
```
Step 1: Validate
├─ Kiểm tra cột bắt buộc
├─ Kiểm tra kiểu dữ liệu
└─ Kiểm tra khoảng giá trị

Step 2: Extract Features
├─ Trích 3 cột điểm: [diem_qua_trinh, diem_giua_ky, diem_cuoi_ky]
└─ Normalize nếu cần

Step 3: Predict
├─ RandomForest.predict([9.0, 8.5, 9.0])
└─ Output: "Xuat_sac"

Step 4: Format Response
├─ Thêm mô tả rủi ro
├─ Thêm tên sinh viên (nếu có)
└─ Trả về JSON
```

### Output Data
```
JSON Response
├─ success: true/false
├─ message: "Dự đoán thành công cho 3 sinh viên"
├─ total_students: 3
└─ data: [
   {
     "ma_sv": "SV001",
     "ho_ten": "Nguyễn Văn A",
     "du_doan": "Xuat_sac",
     "mo_ta": "An toàn - Xuất sắc"
   },
   ...
]
```

---

## 🎨 UI/UX Elements

### Màu sắc & Badge
```
🟢 An toàn (Xuất sắc, Khá)
   └─ Badge: ✅ Xanh lá
   
🟡 Trung bình (Trung bình)
   └─ Badge: ⚠️ Vàng
   
🔴 Nguy cơ cao (Yếu)
   └─ Badge: ⛔ Đỏ
```

### Thông báo (Toast/Alert)
```
Thành công:
├─ 🟢 Màu xanh
├─ Icon: ✅
└─ Text: "Dự đoán thành công!"

Lỗi:
├─ 🔴 Màu đỏ
├─ Icon: ❌
└─ Text: "Lỗi: [mô tả chi tiết]"

Cảnh báo:
├─ 🟡 Màu vàng
├─ Icon: ⚠️
└─ Text: "Cảnh báo: [thông tin]"
```

---

## ⏱️ Performance Requirements

```
Hành động                           Thời gian mong đợi
────────────────────────────────────────────────────
Mở trang web                        < 1 giây
Upload file < 1 MB                  < 1 giây
Dự đoán 100 sinh viên              < 2 giây
Tải xuống kết quả CSV              < 1 giây
```

---

## 🔐 Security & Constraints

```
Ràng buộc:
├─ Kích thước file: max 10 MB
├─ Số lượng sinh viên: max 1000
├─ Thời gian xử lý: max 5 giây
└─ Lỗi không được crash ứng dụng

Bảo mật:
├─ Không lưu trữ dữ liệu upload
├─ Xóa file upload sau khi xử lý
└─ Chỉ xử lý dữ liệu CSV/Excel
```

---

## 📱 Compatibility

```
Browser:
├─ Chrome/Edge 90+
├─ Firefox 88+
├─ Safari 14+
└─ Mobile browsers (responsive)

File Format:
├─ CSV (.csv)
├─ Excel (.xlsx, .xls)
└─ Encoding: UTF-8, Latin-1, CP1252
```

---

## 📞 Support & Troubleshooting

```
Vấn đề                    Giải pháp
─────────────────────────────────────────────────
API không kết nối        → Restart backend
File không upload được   → Kiểm tra format file
Dự đoán chậm            → File quá lớn
Không tải được CSV      → Kiểm tra trình duyệt
```

