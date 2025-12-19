"""
Hàm xử lý dữ liệu và load mô hình
"""

import pandas as pd
import numpy as np
from io import StringIO, BytesIO
import traceback

def validate_input_data(df):
    """
    Kiểm tra dữ liệu đầu vào có đúng định dạng không
    
    Args:
        df: pandas DataFrame
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_columns = ['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']
    
    # Kiểm tra cột
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return False, f"Thiếu cột: {', '.join(missing_cols)}"
    
    # Kiểm tra giá trị thiếu
    for col in required_columns:
        if df[col].isnull().any():
            return False, f"Cột '{col}' có giá trị thiếu"
    
    # Kiểm tra kiểu dữ liệu
    for col in required_columns:
        try:
            pd.to_numeric(df[col], errors='raise')
        except:
            return False, f"Cột '{col}' phải là số"
    
    # Kiểm tra khoảng giá trị (điểm phải từ 0-10)
    for col in required_columns:
        if (df[col] < 0).any() or (df[col] > 10).any():
            return False, f"Cột '{col}' phải có giá trị từ 0 đến 10"
    
    return True, None


def prepare_features_for_prediction(df):
    """
    Chuẩn bị dữ liệu cho dự đoán
    
    Args:
        df: pandas DataFrame chứa cột điểm
        
    Returns:
        numpy array các features
    """
    feature_cols = ['diem_qua_trinh', 'diem_giua_ky', 'diem_cuoi_ky']
    X = df[feature_cols].values.astype(float)
    return X


def create_response(df, predictions):
    """
    Tạo response JSON từ dự đoán
    
    Args:
        df: DataFrame gốc (chứa ma_sv, có thể có ho_ten)
        predictions: array kết quả dự đoán
        
    Returns:
        list of dict
    """
    # Xác định mô tả mức độ rủi ro
    risk_descriptions = {
        'Xuat_sac': 'An toàn - Xuất sắc',
        'Khá': 'An toàn - Khá',
        'Trung_binh': 'Nguy cơ vừa - Trung bình',
        'Yếu': 'Nguy cơ cao - Yếu'
    }
    
    results = []
    
    # Kiểm tra xem có cột ho_ten không
    has_name = 'ho_ten' in df.columns
    
    if 'ma_sv' in df.columns:
        for idx, (ma_sv, pred) in enumerate(zip(df['ma_sv'], predictions)):
            result_item = {
                'ma_sv': str(ma_sv),
                'du_doan': str(pred),
                'mo_ta': risk_descriptions.get(str(pred), 'Không xác định')
            }
            
            # Thêm tên sinh viên nếu có
            if has_name:
                result_item['ho_ten'] = str(df.iloc[idx]['ho_ten'])
            
            results.append(result_item)
    else:
        for idx, pred in enumerate(predictions):
            result_item = {
                'student_index': idx,
                'du_doan': str(pred),
                'mo_ta': risk_descriptions.get(str(pred), 'Không xác định')
            }
            
            if has_name:
                result_item['ho_ten'] = str(df.iloc[idx]['ho_ten'])
            
            results.append(result_item)
    
    return results


def process_csv_file(file_content):
    """
    Xử lý file CSV từ upload
    
    Args:
        file_content: bytes content của file hoặc file-like object
        
    Returns:
        tuple: (success, data_or_error_message)
    """
    try:
        # Thử đọc file với encoding và delimiter khác nhau
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        delimiters = [';', ',', '\t']  # Thử semicolon trước (European format)
        
        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    # If file_content is bytes, convert to BytesIO
                    if isinstance(file_content, bytes):
                        file_obj = BytesIO(file_content)
                    else:
                        file_obj = file_content
                    
                    df = pd.read_csv(file_obj, encoding=encoding, delimiter=delimiter)
                    
                    # Nếu đọc thành công và có cột cần thiết
                    if len(df.columns) > 1:  # Phải có ít nhất 2 cột
                        return True, df
                    
                except (UnicodeDecodeError, pd.errors.ParserError, Exception):
                    # Reset file pointer nếu là file-like object
                    if hasattr(file_obj, 'seek'):
                        try:
                            file_obj.seek(0)
                        except:
                            pass
                    continue
        
        return False, "Không thể đọc file. Kiểm tra: encoding (UTF-8), delimiter (,;\\t), và định dạng file."
    
    except Exception as e:
        return False, f"Lỗi khi đọc file: {str(e)}"
