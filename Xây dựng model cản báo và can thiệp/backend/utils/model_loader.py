"""
Hàm load mô hình Machine Learning
"""

import joblib
import os
from pathlib import Path

# Đường dẫn tới mô hình
MODEL_PATH = Path(__file__).parent.parent / "mo_hinh_du_doan.pkl"

# Cache mô hình trong memory để tránh load nhiều lần
_model = None


def load_model():
    """
    Load mô hình Random Forest từ file .pkl
    
    Returns:
        sklearn RandomForestClassifier model
    """
    global _model
    
    if _model is not None:
        return _model
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Mô hình không tìm thấy tại: {MODEL_PATH}")
    
    _model = joblib.load(MODEL_PATH)
    return _model


def get_model_info():
    """
    Lấy thông tin về mô hình
    
    Returns:
        dict chứa thông tin mô hình
    """
    model = load_model()
    
    return {
        'model_type': type(model).__name__,
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'classes': list(model.classes_),
        'n_features': model.n_features_in_,
        'feature_names': ['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']
    }
