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

## 打包與發布

### 一鍵發布

執行 `release.bat` 會自動完成以下步驟：

1. 遞增 `pyproject.toml` 中的 patch 版本號（如 `0.1.0` → `0.1.1`）
2. 使用 PyInstaller 打包為單一 exe 檔案
3. Git commit、建立版本 tag、push 到遠端
4. 觸發 GitHub Actions 自動建立 Release 並附加 exe

```bash
release.bat
```

### 手動打包

```bash
pip install pyinstaller
python build_exe.py
```

產出檔案：`dist/OCR-App.exe`（約 128MB，含 OCR 模型，可獨立執行）

### 手動發布到 GitHub

```bash
git tag v1.0.0
git push origin main --tags
```

推送 `v*` tag 後，GitHub Actions 會自動在 Windows 環境打包並建立 Release。

## 開發

```bash
# 執行測試
python -m pytest tests/

# Lint 檢查
python -m ruff check src/ tests/
```
