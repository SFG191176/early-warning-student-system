/* ============ GLOBAL CONFIG ============ */

// API Base URL
const API_BASE_URL = 'http://localhost:8000';

// Risk descriptions and colors
const RISK_CATEGORIES = {
    'Xuat_sac': { description: 'An toàn - Xuất sắc', badge: 'badge-safe' },
    'Khá': { description: 'An toàn - Khá', badge: 'badge-safe' },
    'Trung_binh': { description: 'Nguy cơ vừa - Trung bình', badge: 'badge-medium' },
    'Yếu': { description: 'Nguy cơ cao - Yếu', badge: 'badge-high' }
};

/* ============ DOM ELEMENTS ============ */

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const predictBtn = document.getElementById('predictBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsContainer = document.getElementById('resultsContainer');
const emptyState = document.getElementById('emptyState');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const statusContainer = document.getElementById('statusContainer');
const statusBox = document.getElementById('statusBox');
const tableBody = document.getElementById('tableBody');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');

let selectedFile = null;
let lastResults = null;

/* ============ EVENT LISTENERS ============ */

// File input change
fileInput.addEventListener('change', handleFileSelect);

// Drag and drop
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);

// Predict button
predictBtn.addEventListener('click', handlePrediction);

// Download button
downloadBtn.addEventListener('click', downloadResults);

// Reset button
resetBtn.addEventListener('click', resetForm);

/* ============ FILE HANDLING ============ */

function handleFileSelect(event) {
    const files = event.target.files;
    if (files.length > 0) {
        selectedFile = files[0];
        updateFileInfo();
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        selectedFile = files[0];
        updateFileInfo();
        fileInput.files = files;
    }
}

function updateFileInfo() {
    if (selectedFile) {
        fileName.textContent = selectedFile.name;
        fileSize.textContent = formatFileSize(selectedFile.size);
        fileInfo.style.display = 'block';
        predictBtn.disabled = false;
        
        // Clear previous results
        hideResults();
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/* ============ PREDICTION ============ */

async function handlePrediction() {
    if (!selectedFile) {
        showError('Vui lòng chọn file');
        return;
    }

    // Validate file extension
    const validExtensions = ['.csv', '.xlsx', '.xls'];
    const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        showError('File không hợp lệ. Vui lòng chọn file CSV hoặc Excel.');
        return;
    }

    // Show loading
    predictBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    hideResults();
    hideError();

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.error || 'Lỗi không xác định');
        }

        if (data.success) {
            lastResults = data;
            displayResults(data.data);
            showStatus('success', `✓ Dự đoán thành công cho ${data.total_students} sinh viên`);
        } else {
            throw new Error(data.error || 'Lỗi không xác định');
        }

    } catch (error) {
        console.error('Error:', error);
        let errorMsg = error.message || 'Lỗi không xác định';
        
        // Cải thiện thông báo lỗi
        if (errorMsg.includes('không thể đọc file')) {
            errorMsg = '❌ Không thể đọc file. Hãy tải file mẫu để kiểm tra format!';
        } else if (errorMsg.includes('phải là số')) {
            errorMsg = '❌ Lỗi dữ liệu: Các cột điểm phải chứa số (0-10). Hãy kiểm tra lại dữ liệu!';
        } else if (errorMsg.includes('Thiếu cột')) {
            errorMsg = '❌ ' + errorMsg + '. Hãy tải file mẫu để xem format đúng!';
        }
        
        showError(errorMsg);
    } finally {
        loadingSpinner.style.display = 'none';
        predictBtn.disabled = false;
    }
}

/* ============ DISPLAY RESULTS ============ */

function displayResults(results) {
    if (!results || results.length === 0) {
        showError('Không có kết quả dự đoán');
        return;
    }

    // Kiểm tra xem có cột tên không
    const hasName = results.length > 0 && results[0].ho_ten;
    const thName = document.getElementById('th-name');
    if (hasName && thName) {
        thName.style.display = 'table-cell';
    } else if (thName) {
        thName.style.display = 'none';
    }

    // Count risks
    let riskCount = {
        high: 0,
        medium: 0,
        low: 0
    };

    // Clear table
    tableBody.innerHTML = '';

    // Populate table
    results.forEach(result => {
        const prediction = result.du_doan;
        const category = RISK_CATEGORIES[prediction] || { description: prediction, badge: 'badge-safe' };
        
        // Count risk levels
        if (prediction === 'Yếu') riskCount.high++;
        else if (prediction === 'Trung_binh') riskCount.medium++;
        else riskCount.low++;

        const row = document.createElement('tr');
        
        // Kiểm tra xem có cột tên không
        let nameCell = '';
        if (result.ho_ten) {
            nameCell = `<td>${result.ho_ten}</td>`;
        }
        
        row.innerHTML = `
            <td><strong>${result.ma_sv}</strong></td>
            ${nameCell}
            <td>${prediction}</td>
            <td>${result.mo_ta}</td>
            <td><span class="risk-badge ${category.badge}">${category.badge === 'badge-high' ? '⚠️' : category.badge === 'badge-medium' ? '⚡' : '✓'} ${category.description}</span></td>
        `;
        tableBody.appendChild(row);
    });

    // Update stats
    document.getElementById('totalStudents').textContent = results.length;
    document.getElementById('riskHigh').textContent = riskCount.high;
    document.getElementById('riskMedium').textContent = riskCount.medium;
    document.getElementById('riskLow').textContent = riskCount.low;

    // Show results
    emptyState.style.display = 'none';
    resultsContainer.style.display = 'block';
}

function showStatus(type, message) {
    statusBox.className = `status-box ${type}`;
    statusBox.innerHTML = message;
    statusContainer.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        statusContainer.style.display = 'none';
    }, 5000);
}

function hideResults() {
    resultsContainer.style.display = 'none';
    emptyState.style.display = 'block';
}

function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    
    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideError() {
    errorContainer.style.display = 'none';
}

/* ============ DOWNLOAD & EXPORT ============ */

function downloadResults() {
    if (!lastResults || !lastResults.data) {
        showError('Không có dữ liệu để tải xuống');
        return;
    }

    const data = lastResults.data;
    
    // Create CSV content
    const headers = ['Mã SV', 'Dự đoán', 'Mô tả'];
    const csvContent = [
        headers.join(','),
        ...data.map(row => `"${row.ma_sv}","${row.du_doan}","${row.mo_ta}"`)
    ].join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `du_doan_${new Date().toISOString().slice(0, 10)}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showStatus('success', '✓ Tệp đã được tải xuống');
}

/* ============ RESET ============ */

function resetForm() {
    selectedFile = null;
    lastResults = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    predictBtn.disabled = true;
    hideResults();
    hideError();
    statusContainer.style.display = 'none';
    tableBody.innerHTML = '';
    uploadArea.classList.remove('dragover');
}

/* ============ INITIALIZATION ============ */

window.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Frontend loaded');
    
    // Check API health
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ API is healthy');
        }
    } catch (error) {
        console.warn('⚠️ Cannot connect to API:', error);
    }
});
