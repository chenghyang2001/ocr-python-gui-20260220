# Research: OCR 圖片文字辨識桌面應用程式

**Date**: 2026-02-20
**Feature**: 002-ocr-file-clipboard

## OCR 引擎選擇

### Decision: RapidOCR (rapidocr-onnxruntime)

**Rationale**:
- 使用 PaddleOCR 模型（ONNX 格式），中文辨識準確率業界領先
- 繁體中文、簡體中文、英文均有優秀支援
- 安裝僅需 `pip install rapidocr-onnxruntime`，無外部二進位依賴
- 體積約 50-70MB（含模型），記憶體使用約 300-600MB
- onnxruntime 在 Windows 上相容性經廣泛驗證
- Apache 2.0 授權，商用友善

**Alternatives considered**:

| 方案 | 優點 | 排除原因 |
|------|------|---------|
| PaddleOCR | 辨識最強、社群最大 | PaddlePaddle 框架 1.5GB+，過於龐大 |
| EasyOCR | API 最簡單 | 中文準確率略遜、PyTorch 依賴也重 |
| Tesseract | 成熟穩定、體積最小 | 中文辨識明顯落後深度學習方案 |

## GUI 框架選擇

### Decision: PySide6

**Rationale**:
- 剪貼簿支援最完整：`QClipboard.image()` 一行讀取圖片，無需額外套件
- 多線程最成熟：`QThread` + 信號槽機制保障 UI 不凍結（FR-005）
- 圖片顯示：`QPixmap.scaled()` 原生支援等比縮放預覽
- 文字選取/複製：`QTextEdit` 內建支援（FR-006、FR-007）
- LGPL v3 授權，免費可商用
- Windows 原生外觀良好

**Alternatives considered**:

| 方案 | 優點 | 排除原因 |
|------|------|---------|
| tkinter | 零安裝、學習曲線最低 | 剪貼簿圖片讀取需 Pillow 組合，多線程需手動管理 |
| PyQt6 | 同 PySide6 功能 | GPL 授權，商用需付費 |
| wxPython | 原生外觀最佳 | 剪貼簿 API 繁瑣，社群資源較少 |
| DearPyGui | 輕量、GPU 加速 | 無原生剪貼簿支援，外觀非傳統桌面風格 |

## 圖片格式轉換

### Decision: Pillow

**Rationale**:
- PySide6 QImage 與 RapidOCR 之間的圖片格式橋樑
- 支援 PNG、JPG、BMP、TIFF 所有需求格式（FR-001）
- 剪貼簿圖片（QImage）→ numpy array → RapidOCR 的轉換路徑
- 檔案載入圖片的格式驗證

## 最終技術棧

| 元件 | 選擇 | 版本 |
|------|------|------|
| 語言 | Python | 3.11+ |
| GUI 框架 | PySide6 | 6.x |
| OCR 引擎 | rapidocr-onnxruntime | latest |
| 圖片處理 | Pillow | latest |
| 測試框架 | pytest | latest |
| Lint/格式化 | ruff | latest |
