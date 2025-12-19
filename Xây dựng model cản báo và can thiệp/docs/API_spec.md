# API Documentation

## Tổng quan

API Backend được xây dựng bằng FastAPI để xử lý các yêu cầu dự đoán từ Frontend.

## Base URL

```
http://localhost:8000
```

## Authentication

Hiện tại API không yêu cầu authentication. Để sản xuất, bạn nên thêm API Key hoặc JWT.

## Response Format

Tất cả responses là JSON với format chung:

```json
{
  "success": true/false,
  "data": {...},
  "error": "error message (if success=false)"
}
```

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Mô tả**: Kiểm tra sức khỏe API và mô hình

**Response** (200 OK):
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Hệ thống đang chạy bình thường"
}
```

**Error** (500 Internal Server Error):
```json
{
  "status": "error",
  "message": "Error message"
}
```

---

### 2. Model Info

**Endpoint**: `GET /model-info`

**Mô tả**: Lấy thông tin chi tiết về mô hình

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "model_type": "RandomForestClassifier",
    "n_estimators": 200,
    "max_depth": 10,
    "classes": ["Xuat_sac", "Khá", "Trung_binh", "Yếu"],
    "n_features": 3,
    "feature_names": ["diem_qua_trinh", "diem_giua_ky", "diem_cuoi_ky"]
  }
}
```

---

### 3. Categories

**Endpoint**: `GET /categories`

**Mô tả**: Lấy danh sách các phân loại rủi ro

**Response** (200 OK):
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

### 4. Predict

**Endpoint**: `POST /predict`

**Mô tả**: Dự đoán mức độ rủi ro từ file upload

**Parameters**:
- `file` (required, Form Data): File CSV hoặc Excel

**Content-Type**: `multipart/form-data`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@data.csv"
```

**Request Body** (CSV):
```csv
ma_sv,diem_qua_trinh,diem_giua_ky,diem_cuoi_ky
SV001,8.5,8.0,8.2
SV002,7.5,7.8,7.5
SV003,4.5,4.0,4.8
```

**Response** (200 OK):
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
    },
    {
      "ma_sv": "SV002",
      "du_doan": "Yếu",
      "mo_ta": "Nguy cơ cao - Yếu"
    }
  ]
}
```

**Error** (400 Bad Request):
```json
{
  "success": false,
  "error": "Thiếu cột: diem_giua_ky"
}
```

**Error** (500 Internal Server Error):
```json
{
  "success": false,
  "error": "Lỗi xử lý: ..."
}
```

---

### 5. Batch Predict

**Endpoint**: `POST /predict-batch`

**Mô tả**: Dự đoán từ nhiều file cùng lúc

**Parameters**:
- `files` (required, Form Data): Multiple CSV/Excel files

**Example Request**:
```bash
curl -X POST "http://localhost:8000/predict-batch" \
  -F "files=@data1.csv" \
  -F "files=@data2.csv"
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Dự đoán thành công cho 80 sinh viên",
  "total_students": 80,
  "data": [...]
}
```

---

## Data Validation

### Input Validation

- **Cột bắt buộc**: `ma_sv`, `diem_qua_trinh`, `diem_giua_ky`, `diem_cuoi_ky`
- **Kiểu dữ liệu**:
  - `ma_sv`: String
  - `diem_*`: Float/Numeric
- **Khoảng giá trị**: Điểm phải từ 0-10
- **Giá trị thiếu**: Không cho phép

### Error Messages

| Error | Nguyên nhân | Giải pháp |
|-------|-----------|----------|
| "Thiếu cột: ..." | File không có cột yêu cầu | Kiểm tra tên cột |
| "... có giá trị thiếu" | Có ô trống | Điền đầy đủ dữ liệu |
| "... phải là số" | Kiểu dữ liệu sai | Đảm bảo là số |
| "... từ 0 đến 10" | Giá trị ngoài khoảng | Kiểm tra điểm số |

---

## Rate Limiting

Hiện tại không có rate limiting. Để sản xuất, nên thêm:
- 100 requests/minute per IP
- Token-based limiting

---

## CORS

API cho phép requests từ tất cả origins (`*`).

**Recommended** cho sản xuất:
```python
allow_origins=["https://yourdomain.com"]
```

---

## Performance

- **Max file size**: 50MB (mặc định)
- **Timeout**: 300 seconds
- **Concurrent requests**: Unlimited (khuyến cáo thêm queue)

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Thành công |
| 400 | Bad Request - Lỗi input |
| 422 | Validation Error - Lỗi validation |
| 500 | Internal Server Error - Lỗi server |

---

## Examples

### Python

```python
import requests

# Upload file
with open('data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/predict',
        files=files
    )

print(response.json())
```

### JavaScript

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(data);
```

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data.csv" \
  -H "accept: application/json"
```

---

## Swagger UI

API tự động sinh Swagger UI:

```
http://localhost:8000/docs
```

---

## Changelog

### v1.0.0 (Initial Release)
- ✓ Endpoint /predict
- ✓ Endpoint /predict-batch
- ✓ Model info endpoint
- ✓ Health check
- ✓ CORS support
