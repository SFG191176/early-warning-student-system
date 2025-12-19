"""
Backend API FastAPI cho hệ thống dự đoán sinh viên yếu
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import pandas as pd
import os
from pathlib import Path
from io import BytesIO
import logging
from typing import List, Dict

# Import utils
from utils.model_loader import load_model, get_model_info
from utils.data_processing import (
    validate_input_data,
    prepare_features_for_prediction,
    create_response,
    process_csv_file
)

# ============ CẤU HÌNH LOGGING ============
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ STARTUP HANDLER ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager - replaces on_event decorators"""
    # Startup
    try:
        model = load_model()
        info = get_model_info()
        logger.info("✓ Model loaded successfully on startup")
        logger.info(f"✓ Model info: {info}")
    except Exception as e:
        logger.error(f"Failed to load model on startup: {str(e)}")
        raise
    
    yield
    
    # Shutdown (nếu cần)
    logger.info("Shutting down...")

# ============ KHỞI TẠO APP ============
app = FastAPI(
    title="Hệ thống Cảnh báo Sinh viên Yếu",
    description="API dự đoán mức độ rủi ro sinh viên có nguy cơ học yếu",
    version="1.0.0",
    lifespan=lifespan
)

# ============ CORS CONFIGURATION ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ ROUTES ============

@app.get("/")
async def root():
    """Endpoint root - thông tin về API"""
    return {
        "message": "Hệ thống Cảnh báo Sinh viên Yếu",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "model_info": "/model-info (GET)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health_check():
    """Kiểm tra sức khỏe API"""
    try:
        model = load_model()
        return {
            "status": "healthy",
            "model_loaded": True,
            "message": "Hệ thống đang chạy bình thường"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.get("/model-info")
async def model_info():
    """Lấy thông tin về mô hình ML"""
    try:
        info = get_model_info()
        return {
            "success": True,
            "data": info
        }
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint dự đoán mức độ rủi ro sinh viên
    
    Input: File CSV/XLSX với cột: ma_sv, diem_qua_trinh, diem_giua_ky, diem_cuoi_ky
    Output: JSON danh sách {ma_sv, du_doan, mo_ta}
    """
    try:
        # 1. Kiểm tra định dạng file
        if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="File phải là CSV hoặc Excel (.xlsx, .xls)"
            )
        
        # 2. Đọc file
        logger.info(f"Processing file: {file.filename}")
        
        if file.filename.endswith('.csv'):
            # Đọc CSV
            contents = await file.read()
            success, result = process_csv_file(contents)
            if not success:
                raise HTTPException(status_code=400, detail=result)
            df = result
        elif file.filename.endswith(('.xlsx', '.xls')):
            # Đọc Excel
            contents = await file.read()
            try:
                df = pd.read_excel(BytesIO(contents))
                if df.empty:
                    raise HTTPException(
                        status_code=400,
                        detail="File Excel trống hoặc không hợp lệ"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Lỗi khi đọc file Excel: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="File phải là CSV hoặc Excel (.xlsx, .xls)"
            )
        
        # 3. Kiểm tra dữ liệu
        is_valid, error_msg = validate_input_data(df)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 4. Chuẩn bị features
        X = prepare_features_for_prediction(df)
        
        # 5. Load model và dự đoán
        model = load_model()
        predictions = model.predict(X)
        
        # 6. Tạo response
        results = create_response(df, predictions)
        
        logger.info(f"✓ Successfully predicted for {len(results)} students")
        
        return {
            "success": True,
            "message": f"Dự đoán thành công cho {len(results)} sinh viên",
            "total_students": len(results),
            "data": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")


@app.post("/predict-batch")
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    Endpoint dự đoán hàng loạt từ nhiều file
    """
    try:
        all_results = []
        
        for file in files:
            contents = await file.read()
            success, result = process_csv_file(contents)
            
            if not success:
                logger.warning(f"Skipped file {file.filename}: {result}")
                continue
            
            df = result
            
            is_valid, error_msg = validate_input_data(df)
            if not is_valid:
                logger.warning(f"Skipped file {file.filename}: {error_msg}")
                continue
            
            X = prepare_features_for_prediction(df)
            model = load_model()
            predictions = model.predict(X)
            results = create_response(df, predictions)
            
            all_results.extend(results)
        
        return {
            "success": True,
            "message": f"Dự đoán thành công cho {len(all_results)} sinh viên",
            "total_students": len(all_results),
            "data": all_results
        }
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")


@app.get("/categories")
async def get_categories():
    """Lấy danh sách các loại phân loại"""
    return {
        "success": True,
        "categories": {
            "Xuat_sac": "An toàn - Xuất sắc",
            "Khá": "An toàn - Khá",
            "Trung_binh": "Nguy cơ vừa - Trung bình",
            "Yếu": "Nguy cơ cao - Yếu"
        }
    }


# ============ ERROR HANDLERS ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler cho HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )




if __name__ == "__main__":
    import uvicorn
    
    # Development server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
