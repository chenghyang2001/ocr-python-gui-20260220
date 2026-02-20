# Quickstart: OCR 圖片文字辨識桌面應用程式

**Date**: 2026-02-20
**Feature**: 002-ocr-file-clipboard

## 前置需求

- Python 3.11+
- pip（Python 套件管理器）

## 安裝

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境（Windows）
.venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

## 執行

```bash
# 啟動 GUI 應用程式
python -m src.main
```

## 基本使用

### 從檔案辨識
1. 點擊「載入圖片」按鈕
2. 選擇一張圖片檔案（PNG/JPG/BMP/TIFF）
3. 選擇辨識語言
4. 點擊「辨識」
5. 在結果區域查看辨識文字

### 從剪貼簿辨識
1. 在其他應用程式中截圖（如 Win+Shift+S）
2. 切換到本應用程式
3. 點擊「從剪貼簿貼上」或按 Ctrl+V
4. 選擇辨識語言
5. 點擊「辨識」

### 結果操作
- 點擊「複製」→ 全部結果複製到剪貼簿
- 選取文字後 Ctrl+C → 複製選取部分
- 點擊「匯出」→ 儲存為 .txt 檔案

## 開發

```bash
# 執行測試
pytest

# Lint 檢查
ruff check src/ tests/

# 格式化
ruff format src/ tests/
```

## 專案結構

```text
src/
├── main.py              # 應用程式入口
├── ocr_engine/          # OCR 引擎模組
│   ├── __init__.py
│   └── engine.py
├── file_io/             # 檔案 I/O 模組
│   ├── __init__.py
│   ├── image_loader.py
│   └── text_exporter.py
└── gui/                 # GUI 介面模組
    ├── __init__.py
    └── main_window.py

tests/
├── unit/
│   ├── test_ocr_engine.py
│   └── test_file_io.py
└── integration/
    └── test_gui_workflow.py
```
