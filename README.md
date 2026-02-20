# OCR 圖片文字辨識桌面應用程式

Python 桌面 GUI 應用程式，支援從**檔案**或**系統剪貼簿**載入圖片，進行離線 OCR 文字辨識。

## 功能

- 從檔案載入圖片（PNG/JPG/BMP/TIFF）進行 OCR 辨識
- 從系統剪貼簿直接擷取截圖進行辨識（支援 Ctrl+V）
- 支援繁體中文、簡體中文、英文辨識
- 辨識結果可複製到剪貼簿或匯出為 .txt 檔案
- 離線運作，無需網路連線

## 安裝

```bash
# 需要 Python 3.11+
pip install -r requirements.txt
```

## 使用

```bash
python -m src.main
```

### 從檔案辨識

1. 點擊「載入圖片」
2. 選擇辨識語言
3. 點擊「辨識」

### 從剪貼簿辨識

1. 在其他應用程式中截圖（如 Win+Shift+S）
2. 切換到本應用，按 Ctrl+V 或點擊「從剪貼簿貼上」
3. 點擊「辨識」

## 技術棧

- **GUI**: PySide6
- **OCR**: RapidOCR (ONNX Runtime)
- **圖片處理**: Pillow
- **測試**: pytest
- **Lint**: ruff

## 開發

```bash
# 執行測試
python -m pytest tests/

# Lint 檢查
python -m ruff check src/ tests/
```
