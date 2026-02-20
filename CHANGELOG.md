# Changelog

本文件記錄專案的所有重要變更。

## [0.1.0] - 2026-02-20

### 專案初始化

- 從 Specify 模板建立專案骨架
- 建立 `README.md` 專案說明

### 專案治理

- 制定專案憲法 v1.0.0，確立三大核心原則：模組化架構、測試先行、簡單易用
- 定義技術約束（Python 3.11+、pytest、ruff、Windows 為主要平台）
- 新增貢獻者角色與職責、行為準則、衝突解決程序
- 建立 `.gitignore`（Python 專案規則）

### 功能規劃與設計

- 撰寫功能規格書 `specs/002-ocr-file-clipboard/spec.md`：三個 User Story（檔案載入、剪貼簿擷取、匯出文字檔）
- 完成技術研究 `research.md`：選定 RapidOCR (ONNX) + PySide6 + Pillow
- 建立資料模型 `data-model.md`：ImageSource、RecognitionSettings、RecognitionResult
- 定義模組介面合約 `contracts/module-interfaces.md`
- 建立實作計畫 `plan.md` 與任務清單 `tasks.md`（34 項任務、6 個階段）
- 建立需求品質檢查清單 `checklists/requirements.md`

### 核心功能實作

- **資料模型** (`src/models.py`)：SourceType 列舉、ImageSource、RecognitionSettings、RecognitionResult，含驗證邏輯
- **OCR 引擎** (`src/ocr_engine/engine.py`)：封裝 RapidOCR，支援繁中/簡中/英文辨識
- **檔案載入** (`src/file_io/image_loader.py`)：支援 PNG/JPG/BMP/TIFF 格式載入，支援從系統剪貼簿擷取圖片（QImage → PIL Image 轉換）
- **文字匯出** (`src/file_io/text_exporter.py`)：複製到剪貼簿、匯出為 UTF-8 文字檔
- **主視窗 GUI** (`src/gui/main_window.py`)：
  - 左側：圖片預覽、載入圖片/從剪貼簿貼上按鈕
  - 右側：語言選擇（繁中/簡中/英文）、辨識按鈕、結果顯示區、複製/匯出按鈕
  - 支援 Ctrl+V 快捷鍵貼上
  - 使用 QThread 背景執行 OCR，避免 UI 凍結
  - 完整的錯誤處理與狀態提示

### 測試

- 28 項單元測試全數通過：
  - `test_models.py`（14 項）：資料模型建構與驗證
  - `test_ocr_engine.py`（8 項）：引擎初始化、語言支援、辨識功能
  - `test_file_io.py`（6 項）：檔案載入、格式驗證
- 遵循 TDD 流程：先寫測試（Red）→ 實作（Green）

### 打包與發布

- 建立 PyInstaller 設定檔 `ocr_app.spec`，自動收集 ONNX 模型與 onnxruntime
- 建立打包腳本 `build_exe.py`，產出單一 exe（約 128MB）
- 建立 GitHub Actions 工作流 `.github/workflows/release.yml`，推送 `v*` tag 時自動建置並發布 Release
- 建立一鍵發布腳本 `release.bat`：自動遞增版本、打包、commit、tag、push
