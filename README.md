# 🎓 Hệ thống Cảnh báo Sinh viên Yếu

Hệ thống dự đoán sớm sinh viên có nguy cơ học yếu bằng thuật toán Machine Learning (Random Forest).

## 📋 Mục lục

1. [Tổng quan](#tổng-quan)
2. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
3. [Cài đặt](#cài-đặt)
4. [Chạy hệ thống](#chạy-hệ-thống)
5. [Sử dụng](#sử-dụng)
6. [API Documentation](#api-documentation)
7. [Triển khai](#triển-khai)

---

## 📖 Tổng quan

### Mục tiêu

- **Dự đoán sớm**: Phát hiện sinh viên có nguy cơ học yếu trong năm học tiếp theo
- **Hỗ trợ can thiệp**: Giúp giáo viên và cán bộ tư vấn có thời gian can thiệp sớm
- **Phân loại rủi ro**: Phân nhóm sinh viên theo 4 mức độ: Xuất sắc, Khá, Trung bình, Yếu

### Dữ liệu đầu vào

File CSV hoặc Excel với các cột:

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `ma_sv` | String | Mã sinh viên |
| `diem_qua_trinh` | Float (0-10) | Điểm quá trình |
| `diem_giua_ky` | Float (0-10) | Điểm giữa kỳ |
| `diem_cuoi_ky` | Float (0-10) | Điểm cuối kỳ |

### Kết quả đầu ra

```json
{
  "success": true,
  "total_students": 40,
  "data": [
    {
      "ma_sv": "SV001",
      "du_doan": "Xuat_sac",
      "mo_ta": "An toàn - Xuất sắc"
    },
    {
      "ma_sv": "SV002",
      "du_doan": "Yếu",
      "mo_ta": "Nguy cơ cao - Yếu"
    }
  ]
}
```

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────┐
│    Frontend (Web)           │
│ - HTML/CSS/JavaScript       │
│ - Upload file               │
│ - Hiển thị kết quả          │
└──────────────┬──────────────┘
               │ HTTP/CORS
┌──────────────▼──────────────┐
│    Backend API (FastAPI)    │
│ - /predict endpoint         │
│ - /health endpoint          │
│ - /model-info endpoint      │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  ML Model (Random Forest)   │
│ - mo_hinh_du_doan.pkl       │
│ - Dự đoán mức độ rủi ro     │
└─────────────────────────────┘
```

---

## 🔧 Cài đặt

### Yêu cầu

- Python 3.8+
- pip (trình quản lý package Python)

### Bước 1: Clone hoặc tải về dự án

```bash
cd "c:\Xây dựng model cản báo và can thiệp"
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

```bash
# Trên Windows
python -m venv venv
venv\Scripts\activate

# Hoặc trên macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r backend/requirements.txt
```

---

## 🚀 Chạy hệ thống

### Bước 1: Huấn luyện mô hình (lần đầu tiên)

```bash
cd model_training
python train_model.py
```

**Kết quả:**
- Mô hình được lưu tại: `backend/mo_hinh_du_doan.pkl`
- In ra các chỉ số đánh giá: Accuracy, Precision, Recall, F1-Score

### Bước 2: Chạy Backend API

```bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Kết quả:**
```
INFO:     Started server process [1234]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Bước 3: Mở Frontend

Mở file `frontend/index.html` trong trình duyệt:

```bash
# Trên Windows
start frontend/index.html

# Hoặc copy đường dẫn vào trình duyệt
file:///c:/Xây%20dựng%20model%20cản%20báo%20và%20can%20thiệp/frontend/index.html
```

---

## 📱 Sử dụng

### 1. Chuẩn bị file dữ liệu

Tạo file CSV/Excel với định dạng:

```csv
ma_sv,diem_qua_trinh,diem_giua_ky,diem_cuoi_ky
SV001,8.5,8.0,8.2
SV002,7.5,7.8,7.5
SV003,4.5,4.0,4.8
```

### 2. Upload file

1. Mở trang web Frontend
2. Kéo file vào khung upload hoặc click "Chọn file"
3. Chọn file CSV/Excel

### 3. Dự đoán

1. Click nút "🔮 Dự đoán"
2. Chờ kết quả xử lý

### 4. Xem kết quả

- Hiển thị thống kê: Tổng SV, Nguy cơ cao, Trung bình, An toàn
- Bảng chi tiết với mã SV, dự đoán, mô tả
- Tải xuống kết quả dưới dạng CSV

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. GET `/`

**Mô tả**: Thông tin về API

**Response**:
```json
{
  "message": "Hệ thống Cảnh báo Sinh viên Yếu",
  "version": "1.0.0",
  "endpoints": {...}
}
```

#### 2. GET `/health`

**Mô tả**: Kiểm tra sức khỏe API

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Hệ thống đang chạy bình thường"
}
```

#### 3. GET `/model-info`

**Mô tả**: Lấy thông tin mô hình ML

**Response**:
```json
{
  "success": true,
  "data": {
    "model_type": "RandomForestClassifier",
    "n_estimators": 200,
    "classes": ["Xuat_sac", "Khá", "Trung_binh", "Yếu"]
  }
}
```

#### 4. POST `/predict`

**Mô tả**: Dự đoán từ file upload

**Request**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@data.csv"
```

**Response**:
```json
{
  "success": true,
  "message": "Dự đoán thành công cho 40 sinh viên",
  "total_students": 40,
  "data": [
    {
      "ma_sv": "SV001",
      "du_doan": "Xuat_sac",
      "mo_ta": "An toàn - Xuất sắc"
    }
  ]
}
```

#### 5. GET `/categories`

**Mô tả**: Lấy danh sách phân loại

**Response**:
```json
{
  "success": true,
  "categories": {
    "Xuat_sac": "An toàn - Xuất sắc",
    "Khá": "An toàn - Khá",
    "Trung_binh": "Nguy cơ vừa - Trung bình",
    "Yếu": "Nguy cơ cao - Yếu"
  }
}
```

---

## 🌐 Triển khai

### Triển khai Backend

#### Option 1: PythonAnywhere

1. Đăng ký tại [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload dự án
3. Tạo Web app từ PythonAnywhere Dashboard
4. Cấu hình WSGI để chạy FastAPI

#### Option 2: Render.com

1. Push code lên GitHub
2. Đăng ký tại [Render.com](https://render.com)
3. Tạo Web Service từ GitHub repo
4. Set Build command: `pip install -r backend/requirements.txt`
5. Set Start command: `cd backend && uvicorn app:app --host 0.0.0.0 --port 8000`

#### Option 3: Railway.app

1. Push code lên GitHub
2. Kết nối GitHub với [Railway.app](https://railway.app)
3. Deploy tự động

### Triển khai Frontend

#### Option 1: Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir frontend
```

#### Option 2: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

#### Option 3: GitHub Pages

1. Push code lên GitHub
2. Vào Settings → Pages
3. Chọn Deploy from a branch
4. Chọn `main` branch và folder `frontend`

---

## 📊 Cấu trúc dự án

```
project/
├── backend/
│   ├── app.py                          # FastAPI main app
│   ├── requirements.txt                # Python dependencies
│   ├── mo_hinh_du_doan.pkl            # Trained ML model
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processing.py         # Data validation
│   │   └── model_loader.py            # Model loading
│   └── uploads/                       # Temp uploads folder
│
├── frontend/
│   ├── index.html                      # Main page
│   ├── style.css                       # Styling
│   └── script.js                       # JavaScript logic
│
├── model_training/
│   ├── train_model.py                  # Training script
│   └── data/
│       └── diem_sinh_vien.csv         # Sample training data
│
├── tests/                              # Unit tests
├── docs/
│   ├── CONTEXT.md                      # Project overview
│   └── API_spec.md                     # API documentation
│
└── README.md                           # This file
```

---

## 🧪 Testing

### Test API Health

```bash
curl http://localhost:8000/health
```

### Test Prediction

```bash
# Create test CSV
cat > test.csv << EOF
ma_sv,diem_qua_trinh,diem_giua_ky,diem_cuoi_ky
SV001,8.5,8.0,8.2
SV002,4.5,4.0,4.8
EOF

# Send to API
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.csv"
```

---

## 🐛 Xử lý sự cố

### Lỗi: "Cannot connect to API"

**Giải pháp:**
1. Kiểm tra Backend có đang chạy: `http://localhost:8000/health`
2. Kiểm tra port 8000 không bị chiếm dụng: `netstat -ano | findstr :8000`

### Lỗi: "Model not found"

**Giải pháp:**
1. Chạy lại script huấn luyện: `python model_training/train_model.py`
2. Kiểm tra file `backend/mo_hinh_du_doan.pkl` tồn tại

### Lỗi: "File format not supported"

**Giải pháp:**
1. Sử dụng file CSV hoặc Excel (.xlsx, .xls)
2. Kiểm tra cột: `ma_sv`, `diem_qua_trinh`, `diem_giua_ky`, `diem_cuoi_ky`

---

## 📈 Hiệu suất mô hình

Mô hình hiện tại sử dụng:
- **Thuật toán**: Random Forest Classifier
- **Số lượng cây (trees)**: 200
- **Độ sâu tối đa**: 10
- **Tỷ lệ test**: 20%
- **Đánh giá**: Accuracy, Precision, Recall, F1-Score

Xem kết quả chi tiết khi chạy `train_model.py`

---

## 🤝 Đóng góp

Các bước để đóng góp:

1. Fork dự án
2. Tạo branch feature: `git checkout -b feature/AmazingFeature`
3. Commit thay đổi: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Mở Pull Request

---

## 📝 License

Dự án này được cấp phép dưới MIT License.

---

## 📧 Liên hệ

Nếu bạn có câu hỏi hoặc gợi ý, vui lòng liên hệ:

- Email: support@project.com
- GitHub Issues: [Project Issues](https://github.com/yourusername/project/issues)

---

## 🎉 Cảm ơn

Cảm ơn bạn đã sử dụng hệ thống cảnh báo sinh viên yếu!

**Chúc bạn thành công trong việc hỗ trợ các sinh viên!** 🚀
