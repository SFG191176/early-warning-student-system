# context.md

## 1. Tổng quan hệ thống

Dự án xây dựng một hệ thống cảnh báo sớm cho sinh viên có nguy cơ học yếu trong các học kỳ tiếp theo. Hệ thống sử dụng mô hình học máy (Machine Learning) — cụ thể là thuật toán Random Forest — để dự đoán mức độ rủi ro của từng sinh viên dựa trên dữ liệu điểm số.

Hệ thống được chia thành 3 phần chính:

### 1. Bộ não ML (Machine Learning Model)

* Một mô hình Random Forest đã được huấn luyện.
* Lưu dưới dạng file: `mo_hinh_du_doan.pkl`.
* Input: dữ liệu điểm mới của sinh viên (CSV/Excel).
* Output: phân loại mức độ rủi ro (VD: "Nguy cơ cao", "Trung bình", "An toàn").

### 2. Backend API (Flask hoặc FastAPI)

* Vai trò: nhận file từ giao diện web → xử lý → gửi dữ liệu qua mô hình ML → trả kết quả về Frontend.
* Luôn chạy nền, khác với file `predict.py` chỉ chạy xong là tắt.
* Pipeline backend:

  1. Nhận file CSV/XLSX tải lên.
  2. Đọc file bằng pandas.
  3. Load mô hình `mo_hinh_du_doan.pkl`.
  4. Chạy dự đoán.
  5. Trả kết quả dạng JSON cho Frontend.

### 3. Frontend (HTML + JavaScript)

* Một trang web đơn giản.
* Thành phần gồm:

  * Nút "Tải lên tệp Excel/CSV".
  * Nút "Dự đoán".
  * Khu vực hiển thị kết quả.
* Chức năng:

  1. Cho phép giáo viên chọn file điểm.
  2. Gửi file sang Backend qua API.
  3. Hiển thị kết quả dự đoán trả về.

---

## 2. Mục tiêu dự án

* Xây dựng mô hình cảnh báo sớm giúp giáo viên phát hiện sinh viên có nguy cơ học yếu trong năm học tiếp theo.
* Dữ liệu đầu vào: điểm quá trình, điểm giữa kỳ, điểm cuối kỳ.
* Mô hình: Random Forest Classifier.
* Dự đoán: phân nhóm sinh viên theo mức độ rủi ro.
* Ứng dụng: giúp can thiệp sớm để hỗ trợ sinh viên.

---

## 3. Quy trình làm dự án (từ cơ bản nhất)

### Bước 1: Chuẩn bị dữ liệu

* Thu thập dữ liệu điểm của sinh viên.
* Các cột dữ liệu mẫu:

  * `ma_sv`
  * `diem_qua_trinh`
  * `diem_giua_ky`
  * `diem_cuoi_ky`
  * `ket_qua_nam_sau` (label: khá, trung bình, yếu...)
* Làm sạch dữ liệu:

  * Xử lý giá trị thiếu.
  * Chuẩn hóa kiểu dữ liệu.
  * Loại bỏ dữ liệu sai/lỗi.

### Bước 2: Huấn luyện mô hình ML

* Chia dữ liệu train/test.
* Dùng RandomForestClassifier.
* Đánh giá mô hình:

  * Accuracy, Precision, Recall.
* Lưu mô hình:

  ```python
  import joblib
  joblib.dump(model, 'mo_hinh_du_doan.pkl')
  ```

### Bước 3: Xây dựng Backend API (Flask/FastAPI)

* Tạo một server đơn giản:

  * Endpoint `/predict` để nhận file.
  * Đọc file bằng pandas.
  * Load mô hình `.pkl`.
  * Trả dự đoán dạng JSON.

### Bước 4: Xây dựng Frontend Web

* HTML đơn giản có input file + nút gửi.
* JavaScript dùng `fetch()` gửi file tới API.
* Nhận và hiển thị kết quả.

### Bước 5: Triển khai

* Deploy Backend trên:

  * PythonAnywhere
  * Render
  * Vercel (qua serverless FastAPI)
  * VPS
* Deploy Frontend trên:

  * Netlify
  * Vercel
  * Hosting đơn giản

---

## 4. Công nghệ cần dùng

### 1. Machine Learning

* Python
* pandas
* numpy
* scikit-learn
* joblib (lưu mô hình)

### 2. Backend

* Flask **hoặc** FastAPI
* Uvicorn (nếu dùng FastAPI)
* pandas (đọc file tải lên)

### 3. Frontend

* HTML
* CSS (có thể dùng Tailwind hoặc Bootstrap)
* JavaScript (fetch API)

### 4. Triển khai

* Server chạy Python 3
* Hosting miễn phí hoặc VPS

---

## 5. Luồng hoạt động của hệ thống

1. Giáo viên mở trang web.
2. Tải lên file điểm: `diem_moi.csv`.
3. Frontend gửi file đến Backend API.
4. Backend xử lý + chạy mô hình `.pkl`.
5. Backend trả JSON: `{ "svA": "Nguy cơ cao", ... }`.
6. Frontend hiển thị kết quả.

---

## 6. Kết luận

File "context.md" này mô tả toàn bộ hệ thống: mục tiêu, kiến trúc, công nghệ, luồng xử lý và cách triển khai. Có thể dùng để cung cấp cho bất kỳ AI nào nhằm hiểu tổng quan dự án một cách rõ ràng và thống nhất.

---

## 7. Sơ đồ kiến trúc hệ thống (Architecture Diagram)

```
+------------------+         +----------------------+         +---------------------------+
|  Giao diện Web   | ----->  |  Backend API Flask   | ----->  |  Mô hình ML (.pkl file)  |
| (HTML/JS Upload) |         |  /predict endpoint   |         | Random Forest Prediction |
+------------------+         +----------------------+         +---------------------------+
         |                             |                                  |
         |                             v                                  |
         |                    Xử lý dữ liệu (pandas)                      |
         |                             |                                  |
         |                             v                                  |
         |                     Trả kết quả JSON <--------------------------+
         v
Hiển thị cảnh báo
```

---

## 8. Ví dụ mã nguồn huấn luyện mô hình Random Forest

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Đọc dữ liệu
df = pd.read_csv('diem_sinh_vien.csv')

# 2. Chọn features và label
X = df[['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']]
y = df['ket_qua_nam_sau']

# 3. Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 5. Kiểm tra
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# 6. Lưu mô hình
joblib.dump(model, 'mo_hinh_du_doan.pkl')
```

---

## 9. Mẫu Backend API (Flask)

```python
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load('mo_hinh_du_doan.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    df = pd.read_csv(file)

    X = df[['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']]
    predictions = model.predict(X)

    results = df[['ma_sv']].copy()
    results['du_doan'] = predictions

    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 10. Mẫu Backend API (FastAPI)

```python
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib

app = FastAPI()
model = joblib.load('mo_hinh_du_doan.pkl')

@app.post('/predict')
def predict(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    X = df[['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']]
    predictions = model.predict(X)

    results = df[['ma_sv']].copy()
    results['du_doan'] = predictions

    return results.to_dict(orient='records')
```

---

## 11. Mẫu giao diện Frontend (HTML + JS)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Dự đoán sinh viên</title>
</head>
<body>
    <h2>Tải file điểm sinh viên</h2>
    <input type="file" id="fileInput">
    <button onclick="sendFile()">Dự đoán</button>

    <pre id="result"></pre>

    <script>
        async function sendFile() {
            const file = document.getElementById('fileInput').files[0];
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
```

---

## 12. Định dạng chuẩn dành cho AI khác (System Prompt Template)

```
Bạn là AI hỗ trợ phát triển hệ thống cảnh báo sớm sinh viên yếu.
Hãy tuân theo các điều sau:

1. Mục tiêu:
   - Dự đoán sinh viên có nguy cơ học yếu dựa trên điểm số.
   - Mô hình sử dụng Random Forest.

2. Cấu trúc hệ thống:
   - Frontend: HTML/JS (upload file CSV, hiển thị kết quả).
   - Backend: Flask hoặc FastAPI.
   - Machine Learning: mô hình .pkl được load và dự đoán dữ liệu mới.

3. Input cho backend:
   - File CSV gồm: ma_sv, diem_qua_trinh, diem_giua_ky, diem_cuoi_ky.

4. Output backend:
   - JSON: danh sách {ma_sv, du_doan}.

5. Khi trả lời:
   - Luôn bám theo mô tả kiến trúc này.
   - Ưu tiên câu trả lời rõ ràng, gọn, có ví dụ mã nguồn.
```

---

## 13. Cấu trúc thư mục chuẩn của dự án

Dưới đây là cấu trúc thư mục đầy đủ, rõ ràng cho dự án cảnh báo sớm sinh viên yếu bằng Random Forest. Cấu trúc này phù hợp để triển khai, bảo trì và mở rộng.

```
project/
│
├── backend/
│   ├── app.py                     # Flask/FastAPI backend
│   ├── requirements.txt           # Các thư viện Python
│   ├── mo_hinh_du_doan.pkl        # Mô hình ML đã huấn luyện
│   ├── utils/
│   │   ├── data_processing.py     # Hàm xử lý dữ liệu
│   │   └── model_loader.py        # Hàm load mô hình
│   └── uploads/                   # Lưu tạm file upload (nếu cần)
│
├── frontend/
│   ├── index.html                 # Giao diện chính
│   ├── script.js                  # Gửi file lên API
│   └── style.css                  # Giao diện (tùy chọn)
│
├── model_training/
│   ├── train_model.ipynb          # Notebook huấn luyện mô hình
│   ├── train_model.py             # File huấn luyện mô hình dạng script
│   └── data/
│       ├── diem_sinh_vien.csv     # Dữ liệu gốc
│       └── data_cleaned.csv       # Dữ liệu đã làm sạch
│
├── docs/
│   ├── context.md                 # Tài liệu mô tả hệ thống (file này)
│   └── API_spec.md                # Định nghĩa API backend
│
├── tests/
│   ├── test_api.py                # Test backend API
│   └── test_model.py              # Test mô hình ML
│
└── README.md                      # Tài liệu tổng quan dự án
```

---

## 13.1 Mô tả nhanh từng thư mục

### **backend/**

Chứa toàn bộ API, mô hình đã huấn luyện và logic xử lý.

### **frontend/**

Chứa website dùng cho giáo viên để upload file và xem kết quả.

### **model_training/**

Nơi bạn huấn luyện mô hình, lưu dataset, chạy thử nghiệm.

### **docs/**

Chứa tài liệu mô tả hệ thống, API, kiến trúc.

### **tests/**

Phần kiểm thử đảm bảo mô hình và API hoạt động đúng.

### **README.md**

Tổng quan dự án, cách chạy, cách cài đặt.
