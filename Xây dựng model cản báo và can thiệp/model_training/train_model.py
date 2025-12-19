"""
Script huấn luyện mô hình Random Forest để dự đoán mức độ rủi ro sinh viên yếu
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import os
from pathlib import Path

# Đặt đường dẫn
project_root = Path(__file__).parent.parent
data_path = project_root / "model_training" / "data" / "diem_sinh_vien.csv"
model_path = project_root / "backend" / "mo_hinh_du_doan.pkl"

print("=" * 60)
print("HỆ THỐNG HUẤN LUYỆN MÔ HÌNH DỰ ĐOÁN SINH VIÊN YẾU")
print("=" * 60)

# ============ BƯỚC 1: ĐỌC VÀ KHÁM PHÁ DỮ LIỆU ============
print("\n[1/5] Đọc dữ liệu...")
df = pd.read_csv(data_path)
print(f"✓ Loaded {len(df)} hàng dữ liệu")
print(f"✓ Cột dữ liệu: {list(df.columns)}")
print(f"\nDữ liệu mẫu (5 hàng đầu):")
print(df.head())

# ============ BƯỚC 2: CHUẨN BỊ DỮ LIỆU ============
print("\n[2/5] Chuẩn bị dữ liệu...")

# Kiểm tra giá trị thiếu
print(f"Giá trị thiếu: \n{df.isnull().sum()}")

# Chọn features (X) và label (y)
feature_cols = ['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']
X = df[feature_cols].copy()
y = df['ket_qua_nam_sau'].copy()

print(f"✓ Features: {feature_cols}")
print(f"✓ Label: ket_qua_nam_sau")
print(f"✓ Phân bố các lớp:")
print(y.value_counts())

# ============ BƯỚC 3: CHIA DỮ LIỆU TRAIN/TEST ============
print("\n[3/5] Chia dữ liệu train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y
)

print(f"✓ Train set: {len(X_train)} mẫu")
print(f"✓ Test set: {len(X_test)} mẫu")

# ============ BƯỚC 4: HUẤN LUYỆN MÔ HÌNH ============
print("\n[4/5] Huấn luyện mô hình Random Forest...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train, y_train)
print("✓ Mô hình đã được huấn luyện")

# ============ BƯỚC 5: ĐÁNH GIÁ MÔ HÌNH ============
print("\n[5/5] Đánh giá mô hình...")

# Dự đoán trên train set
y_train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)

# Dự đoán trên test set
y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)

print(f"\n📊 KẾT QUẢ ĐÁNH GIÁ:")
print(f"   Train Accuracy: {train_accuracy:.4f}")
print(f"   Test Accuracy:  {test_accuracy:.4f}")
print(f"   Precision:      {precision:.4f}")
print(f"   Recall:         {recall:.4f}")
print(f"   F1-Score:       {f1:.4f}")

print(f"\n🔍 CONFUSION MATRIX:")
print(confusion_matrix(y_test, y_test_pred))

print(f"\n📋 CLASSIFICATION REPORT:")
print(classification_report(y_test, y_test_pred, zero_division=0))

# Feature importance
print(f"\n⭐ TẦM QUAN TRỌNG CÁC FEATURE:")
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance.to_string(index=False))

# ============ LƯU MÔ HÌNH ============
print(f"\n💾 Lưu mô hình...")
os.makedirs(model_path.parent, exist_ok=True)
joblib.dump(model, model_path)
print(f"✓ Mô hình đã được lưu tại: {model_path}")

print("\n" + "=" * 60)
print("✅ HOÀN THÀNH HUẤN LUYỆN MÔ HÌNH!")
print("=" * 60)
